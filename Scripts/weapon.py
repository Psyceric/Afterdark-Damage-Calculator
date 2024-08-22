import re, math

class Weapon():
        """
        Contains and Manipulates data regarding Afterdark Weapons.

        Generate a weapon from a dictionary of base stats that can be found inside the Afterdark Manual (AD Manual 1.02). 
        Allow you to update the weapon's damage with variables (Level, Damage Modifier, To Hit Bonus, Number of Attacks)
        The afterdark system utilized a Cumulative Pentalty system that makes it possible to do any number of attacks in a turn, with increasing difficult to each check. 
        These checks are made using a D10. If your roll is above 8 it will automaticall succeed. If your roll is above 15 you will "Critically Succeed" doubling the damage of that roll.
        Cumulative Pentaly is described in AD Manual 1.02 as:
        Cumulative Penalty: 
        "In a turn, a player can do any number of things. However, each consecutive action produces a Cumulative Penalty (CP) for any additional actions on that turn... 
        ...A character's Cumulative Penalty resets right before the start of their turn."

        This directly affect how much damage per turn a weapon is able to do, and as such we use the weapons probability of making sucessful attacks added together until their is no chance of a successful attack.
        A 2CP Weapon with an additional +3 To Hit Bonus will be rolling a 1d10+3 at 0 CP. Rolling once will have a 5/10 chance of rolling above 8. Causing a success.
        Following this roll, you will add 2CP to the CP, making the next roll be 1d10+1. This roll will have a 3/10 chance of rolling a success. We save this value additively with past rolls until we can no longer succeed.
        This results in 5/10 + 3/10 + 1/10 (1d10-1) or 9/10 average successful attacks to be made in a turn. Multiplying this by the average damage a weapon will do per attack should give us a rough estimate to the weapons DPT or Damage Per Turn.
        Attempting an attack will always be in the following formula.
        1d10 + To Hit Bonus - Current CP
        
        Be aware however this does not take into account situational modifiers to weapons such as World Affects (Smoke, Flank/Read cone bonus, ect.)
        To get around this we utilize our UserEntry menu to give more context to the caluclation regarding how we should be calculating the damage. This can be additional To Hit Modifier, increasing the 'accuracy' of our roles. 
        Damage Modifier is added as a flat value to the damage roll per instance. An example of this could be a weapon with 3d4 damage could have a damage Modifier of +3. The new damage roll would be 3d4 + 3 or 10.5 average damage. (You are unable to roll 0 on a D10)
        We are also able to specify a certain number of attacks. When 0 this will make attacks until the weapon is no longer able to make any successful attacks. When a value above 0 we will roll that many attacks. This is useful for calulating "Realistic" attack quantities.
        
        Additionally some Weapon Tags will give statistic differences to weapons, some are situational and to estimate its affect in game we give a 'situational_dice' modifier that increases the damage per attack.
        Automatic - 0.5 additional dice per attack
        Flexible, Cleaving, Piercing, Incindiary - 1.0 additional dice per attack
        Explosive - 2.0 additional dice per turn
        Blunt - +4 flat damage added per turn
        Wieldy - +1 To Hit Bonus 
        
        Weapon level will modify the weapons damage roll in an alternating pattern of an Increase to the Dice Quantitity, and Dice Face with dice face not increasing past Level 5.
        Weapons will obtain all the previous level increases. A Level 3 weapon will have 2 additional dice, and an increase in Dice Face by 1. This will take a 3d4 to a 5d6 damage rolll
        This can look like the following.

        Level - Damage Roll increase
        2 - +1 Die
        3 - Dice Type Up
        4 - +1 Die
        5 - Dice Type Up
        6+ - +1 Die

        Attributes:
            name: string that denotes the weapons name in the Afterdark book.
            default_dice: string of weapon damage roll maxing with Dice face of 12.
            cp: int that is the ammount of cumulative pentaly the weapon will accrue each attack.
            tags: list of strings containing each string that is defined in a weapon.
            category: string for the "Archetype" or category of types of weapons. (Shotguns, Swords, Polearms,...)
            magazine_size: string that is the maximum magzine size. N/A for Melee weapons.
            to_hit_bonus: int that is added when you attempt to roll a dice to deal damdage 1d10 + to_hit_bonus - CP.
            level: int that is the weapons current level.
            damage_modifier: int that is the amount of damage added flat to each damage roll (3d4 + damage_modifier ; 3d4 + 4 or 11.5 average damage. You can not roll a 0 on a Dice).
            damage_roll: string that contains the damage_roll of an average attack.
            situational_dice: float for additional dice we add to each successful attack.
            attack_damage: float of average successful attack damage (3d4 + 4 ; 11.5 average damage. You can not roll a 0 on a Dice).
            average_attacks: float detailing the combined chances repeated attacks will have. Between 0-1 for each attempt. 5/10 + 3/10 + 1/10 = 9/10 average attacks per turn.
            average_damage_per_turn: float of average_attacks multiplied by attack_damage (9/10 * 10.5 = 9.45 average damage per turn).
                Also refered to DPT in some documentaiton.
            item_identifier: Tkinter Treeview item identification number.
            item_index: Int representing the Tkinter Treeview Item row location.
            attack_limit: int limitat of amount of attacks to make per turn. 
                IF 0 - Roll until you have no chance of success.
                Else - Limit rolls after you have attempted attack_limit attacks. Will still stop if successful attacks are no longer possible.
        """
        name : str = "Default"
        default_dice  : str = "3d4"
        cp : int = 1
        tags : list[str] = ["Wieldy", "Cleaving"]
        category : str = "Swords"
        magazine_size : str = "N/A"
        to_hit_bonus : int = 0
        level : int = 1
        damage_modifier : int = 0
        damage_roll : str = "3d4"
        situational_dice : float = 0.0
        attack_damage : float = 10.0 
        average_attacks : float = 1.0
        average_damage_per_turn : float = 10.0
        item_identifier = None
        item_index = None
        attack_limit : int 

        def __init__(self, weapon_dict : dict = None, name : str = "Default", default_dice : str = "3d4", cp : int = 1, tags : list[str] = ["Wieldy", "Cleaving"], category : str = "Swords", magazine_size : str = "N/A", **kwargs):
            """
            Generates a weapon based on a weapon_dict that is read by a CSV file, or from arguments that are defaulted. 

            We will take the weapon_dict or we will generate a dict from the kwargs entered. We than will set the attribute based on the dict Key.
            We than will update generating 'basic' values (level 0, additional damage modfiier 0, additional to hit bonus 0, number of attacks 0)
            
            Args:
                weapon_dict: Dict that defines the creation of a weapon_dict. This is the same as the below entered KWARGS you can enter manually.
                name: string that denotes the weapons name in the Afterdark book.
                default_dice: string of weapon damage roll maxing with Dice face of 12.
                cp: int that is the ammount of cumulative pentaly the weapon will accrue each attack.
                tags: list of strings containing each string that is defined in a weapon.
                category: string for the "Archetype" or category of types of weapons. (Shotguns, Swords, Polearms,...)
                magazine_size: string that is the maximum magzine size. N/A for Melee weapons.
                **kwargs: All entered kwargs
            """
            _weapon_dict = weapon_dict
            if weapon_dict is None:
                _weapon_dict = kwargs
            for _key, val in _weapon_dict.items():
                setattr(self, _key, val)
            self.update_weapon()

        def __str__(self):
            """
            Return the weapons name when printed the weapon object.
            
            print(Mace) -> "Mace"
            """
            return self.name

        def validate_dice(self, value : str):
            """
            Validates that a dice string is a number of dice, Followed by d, followed by a dice face equal to 4,6,8,10,12
            
            Args:
                value : string that will attempt to be validated by DICE_PATTERN regex expression.
        
            Returns:
                Boolean if value string was validated with the DICE_PATTERN regex expression.
            """
            DICE_PATTERN = r'/\d{1,3}[d]([4,6,8]|]|1[0,2])($|[+]\d{1,2})$/m'
            result = re.finditer(DICE_PATTERN, value, re.MULTILINE) is not None
            return result

        def has_tags(self, requested_tags : list): 
            """Returns if a weapon contains all the specified tags.
            
            Args:
                requested_tags : list of strings that will be checked if contained in weapons tags list.
        
            Returns:
                Boolean that denotes if all items in requested_tags are present inside the weapons tag list.
            """
            my_tags = set(self.tags)
            requested_tags = set(requested_tags)
            
            # Returns if all requested_tags is a sub-list of all tags
            return requested_tags.intersection(my_tags) == requested_tags
 
        def update_weapon(self, user_entrys : dict):
            """Overload method to update_weapon using a dictionary of values"""
            self.update_weapon(user_entrys['level'], user_entrys['damage_modifier'], user_entrys['to_hit_bonus'], user_entrys['number_of_attacks'])

        def update_weapon(self, level : int = 1, damage_modifier : int = 0, to_hit_bonus : int = 0, number_of_attacks : int = 0):
            """
            Take a weapon, and modify their non-base values (damage_roll, situational_dice, attack_damage, average_attacks, average_damage_per_turn), and affects the damage per turn

            Add tag modifiers to the arguments, and than calculate damage. Calculation must be done in order to prevent errors

            Args:
                level: int that is the weapons new level that will be assigned.
                damage_modifier: int that is conditionally damage_modifier that will be added to this weapon.
                to_hit_bonus: int that is conditional to_hit_bonus that will be added to this weapon.
                number_of_attacks: int limitat of amount of attacks to make per turn. 
                    IF 0 - Roll until you have no chance of success.
                    Else - Limit rolls after you have attempted attack_limit attacks. Will still stop if successful attacks are no longer possible.
            """
            _weapon_level = level
            _situational_dice = 0.0
            _damage_modifier = damage_modifier
            _to_hit_bonus = to_hit_bonus
            self.attack_limit = number_of_attacks
            _blunt_mod = 4
            for tag in self.tags:
                match tag.strip():
                    case "Automatic":
                        _situational_dice += .5
                    case "Flexible"|"Cleaving"|"Piercing"|"Incindiary":
                        _situational_dice += 1
                    case "Explosive":
                        _situational_dice += 2
                    case "Blunt":
                        _damage_modifier += _blunt_mod
                    case "Wieldy":
                        _to_hit_bonus += 1

            self.level = _weapon_level
            self.situational_dice = _situational_dice
            self.damage_modifier = _damage_modifier
            self.to_hit_bonus = _to_hit_bonus
            self.average_attacks = self.get_attacks()
            self.damage_roll = self.get_damage_roll()
            self.attack_damage = self.get_attack_damage()
            self.average_damage_per_turn = self.get_average_damage_per_turn()
        
        def get_average_attacks(self, success_roll = 8, cur_cp = 0, val = 0, count = 0):
            """Recursive function that adds together the chance a weapon will succsseed an attack.

            Each itteration will add to the Cummulative Pentalty making it more difficult to succssed.
            When there is no longer a chance for a weapon to make a successful attack, return the combined value of all chances added together.
            ex. 5/10 + 3/10 + 1/10 = 9/10 average attacks per turn.
            
            Args:
                success_roll: int necessary for success. Defaults to 8, but can also be set for calculation purposes.
                cur_cp: int of accumulated CP penaltys.
                val: int current amount of combined attack probabilities.
                count: int representing amount of iterations through function.
            Return: 
                return the combined probability of all possible attacks.
            """
            if(10 + self.to_hit_bonus) >= success_roll + cur_cp - 1 and (count < self.attack_limit or self.attack_limit == 0):
                temp = (10 + self.to_hit_bonus - (success_roll + cur_cp - 1))/10
                val += temp
                return self.get_average_attacks(success_roll, cur_cp + self.cp, val, count = count + 1)
            else:
                return val

        def get_attacks(self):
            """Adds normal attack potential to 'Critical success' chance and doubles it to emulate doubling their attacks damage."""
            return self.get_average_attacks(success_roll = 8) + (2 * self.get_average_attacks(success_roll = 15))
        
        def get_damage_roll(self):
            """Take base damage_roll from a weapon, and increases the Dice Quanitity and Dice Face based on the Afterdark Ruleset
            
            Weapon level will modify the weapons damage roll in an alternating pattern of an Increase to the Dice Quantitity, and Dice Face with dice face not increasing past Level 5.
            Weapons will obtain all the previous level increases. A Level 3 weapon will have 2 additional dice, and an increase in Dice Face by 1. This will take a 3d4 to a 5d6 damage rolll
            This can look like the following.

            Level - Damage Roll increase
            2 - +1 Die
            3 - Dice Type Up
            4 - +1 Die
            5 - Dice Type Up
            6+ - +1 Die

            Return:
                returns string of increased damage roll, and damage modifier
            """
            T_dice = self.default_dice.split('d')
            face_modifier = min(math.floor(self.level/2),2)
            quantity = int(T_dice[0]) + self.level - face_modifier - 1
            face = min(int(T_dice[1]) + face_modifier * 2, 12)
            dice = 'd'.join((str(quantity) , str(face)))
            return "+".join((str(dice),str(self.damage_modifier)))

        def deconstruct_dice_roll(self, damage_roll):
            """
            Validates damage dice and returns a tuple of the dice roll and damage mod.
            
            ex. 3d4+4 -> (3,4,4)
            """
            _damage_modifier = 0
            if self.validate_dice(damage_roll):
                _damage_modifier = damage_roll.split('+')[1]
                T_dice = damage_roll.split('+')[0].split('d')
                return (int(T_dice[0]),int(T_dice[1]),int(_damage_modifier))
            
        def get_attack_damage(self):
            """Returns the average damage of a dice roll plus its weapon modifier. Dice can no equal 0, and start a 1"""
            roll = self.deconstruct_dice_roll(self.damage_roll)
            damage = (roll[0] + self.situational_dice) * ((roll[1] + 1)/2)  + roll[2]
            return damage
                
        def get_average_damage_per_turn(self):
            """Returns multiplication of attack_damage and average_attacks"""
            return self.attack_damage * self.average_attacks

        def to_dict(self):
            """Returns a dictionary of values necessary to display in a table"""
            return {
            'name' : self.name,
            'default_dice' : self.default_dice,
            'cp' : self.cp,
            'tags' : self.tags,
            'category' : self.category,
            'magazine_size' : self.magazine_size,
            'to_hit_bonus' : self.to_hit_bonus,
            'level' : self.level,
            'damage_modifier' : self.damage_modifier,
            'damage_roll' : self.damage_roll,
            'situational_dice' : self.situational_dice,
            'attack_damage' : self.attack_damage,
            'average_attacks' : self.average_attacks,
            'average_damage_per_turn' : self.average_damage_per_turn}
        
        def clean_dict(self):
            """Get dictionary, and parse to make more human readable, formatting the strings to be more human readable"""
            _dict = self.to_dict()
            _dict['tags'] = ",".join(_dict['tags'])

            dmg = self.deconstruct_dice_roll(_dict['damage_roll'])
            if dmg[2] == 0:
                _dict['damage_roll'] = "d".join((str(dmg[0]),str(dmg[1])))

            if _dict['to_hit_bonus'] == 0:
                _dict['to_hit_bonus'] = ""
            else: 
                _dict['to_hit_bonus'] = "+" + str(_dict['to_hit_bonus'])

            if _dict['damage_modifier'] == 0:
                _dict['damage_modifier'] = ""
            else: 
                _dict['damage_modifier'] = "+" + str(_dict['damage_modifier'])

            if _dict['situational_dice'] == 0:
                _dict['situational_dice'] = ""
            else:
                _dict['situational_dice'] = "%.1f" % _dict['situational_dice']
            
            _dict['attack_damage'] = "%.2f" % _dict['attack_damage']
            _dict['average_attacks'] = "%.1f" % _dict['average_attacks']
            _dict['average_damage_per_turn'] = "%.2f" % _dict['average_damage_per_turn']
            return _dict


