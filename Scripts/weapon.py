import re, math

class Weapon():
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

        def __init__(self, 
                     name : str, 
                     default_dice : str,
                     cp : int, 
                     tags : list[str],
                     category : str, 
                     magazine_size : int = None):
            
            # for var in [attr for attr in dir(Weapon) if not callable(getattr(Weapon,attr)) and not attr.startswith("__")]:
            #     print(var)
            #     pass
            self.name = name
            self.default_dice = default_dice
            self.cp = cp
            self.tags = tags
            self.category = category
            self.magazine_size = magazine_size

        def validate_dice(self, value : str):
            DICE_PATTERN = r'/\d{1,3}[d]([4,6,8]|]|1[0,2])($|[+]\d{1,2})$/m'
            result = re.finditer(DICE_PATTERN, value, re.MULTILINE) is not None
            return result

        def has_tags(self, *tags): #TODO
            """Determins if the weapon contains all tags specified"""
            tags = set(self.tags)
            requested_tags = set(list(tags))
            
            # Returns if all requested_tags is a sub-list of all tags
            return requested_tags.intersection(tags) == requested_tags

        def update_weapon(self, user_entrys : dict):
            self.update_weapon(user_entrys['level'], user_entrys['damage_modifier'], user_entrys['to_hit_bonus'], user_entrys['number_of_attacks'])

        def update_weapon(self, level : int = 1, damage_modifier : int = 0, to_hit_bonus : int = 0, number_of_attacks : int = 0):
            print("{0} - {1} - {2} - {3}".format(level, damage_modifier, to_hit_bonus, number_of_attacks))
            _weapon_level = level
            _situational_dice = 0.0
            _damage_modifier = damage_modifier
            _to_hit_bonus = to_hit_bonus
            number_of_attacks = number_of_attacks
            _blunt_mod = 4

            print(self.tags)
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
            print(self.to_dict())
        
        def get_average_attacks(self, sucessRoll = 8, curCP = 0, val = 0):
            if(10 + self.to_hit_bonus) >= sucessRoll + curCP:
                temp = (10 + self.to_hit_bonus-(sucessRoll + curCP))/10
                val += temp
                return self.get_average_attacks(sucessRoll, curCP + self.cp, val)
            else:
                return val

        def get_attacks(self):  
            return self.get_average_attacks(sucessRoll = 8) + (2 * self.get_average_attacks(sucessRoll=15))
        
        def get_damage_roll(self): # TODO: Replace requests with variables
            T_dice = self.default_dice.split('d')
            dmgCalc = int(T_dice[0]) 
            face_modifier = min(math.floor(self.level/2),2)
            quantity = int(T_dice[0]) + self.level - face_modifier - 1
            face = min(int(T_dice[1]) + face_modifier * 2, 12)
            dice = 'd'.join((str(quantity) , str(face)))
            return "+".join((str(dice),str(self.damage_modifier)))

        def deconstruct_dice_roll(self, damage_roll):
            _damage_modifier = 0
            if self.validate_dice(damage_roll):
                _damage_modifier = damage_roll.split('+')[1]
                T_dice = damage_roll.split('+')[0].split('d')
                return (int(T_dice[0]),int(T_dice[1]),int(_damage_modifier))
            
        def get_attack_damage(self):
            roll = self.deconstruct_dice_roll(self.damage_roll)
            damage = (roll[0] + self.situational_dice) * ((roll[1] + 1)/2)  + roll[2]
            return damage
                
        def get_average_damage_per_turn(self):
            return self.attack_damage * self.average_attacks

        def clean_dict(self):
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

        def to_dict(self):
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
        



