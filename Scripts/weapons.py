import csv, os, re, math
import pandas as pd

class Weapon():
        _WEAPON_DICTIONARY = {
            'weapon_name' : "Default",
            'default_dice' : "3d4",
            'cp' : 1,
            'weapon_tags' : ["Wieldy", "Cleaving"],
            'weapon_category' : "Swords",
            'magazine_size' : "N/A"}
        
        _WEAPON_CALC_DICTIONARY = {
            'to_hit_bonus' : 0,
            'weapon_level' : 1,
            'damage_modifier' : 0,
            'damage_roll' : "3d4",
            'tag_damage_dice' : 0.0,
            'damage_per_attack' : 10.0,
            'sucessful_attacks' : 1.0,
            'damage_per_turn' : 10.0}
        
        _dict = None
        
        def __init__(self, weapon_dict : dict):
            self.populate_weapon(weapon_dict)

        def __init__(self, 
                     weapon_name : str, 
                     default_dice : str,
                     cp : int, 
                     tags : list[str],
                     category : str, 
                     mag_size : int = None):
            """Used to create new weapon's that are not a dictionary"""

            value_dict = {'weapon_name' : weapon_name, 'default_dice' : default_dice, 'cp' : cp,
                          'weapon_tags' : tags, 'weapon_category' : category, 'magazine_size' : mag_size}
            self.populate_weapon(value_dict)

        def populate_weapon(self, weapon_dict : dict):
            default_dict = self.combine_dict(self._WEAPON_DICTIONARY_KEYS, self._WEAPON_CALC_DICTIONARY_KEYS)
            edited_dict = dict(default_dict).update(weapon_dict)
            if not self.validate_weapon_dict(edited_dict): raise Exception("Unable to Populate weapon from : {0}\n| Does your weapon_dict match the default dict data types?\n{1}".format(edited_dict,default_dict))
            
            self._dict = edited_dict
            # self.updateWeapon() - Empty Parameters = Default Settings. Passed a List of Strings = userEntry data
            # Parse and Update the weapons dictionary from the data



        def combine_dict(self, default : dict, aux : dict):
            return dict(default).update(aux)
        
        def validate_weapon_dict(self, weapon_dict : dict):
            """Make sure that a weapon_dict is populated with valid data"""
            
            STRING_VALIDATION = ['weapon_name','weapon_category']
            INT_VALIDATION = ['cp','weapon_level','damage_modifier','to_hit_bonus']
            FLOAT_VALIDATION = ['tag_damage_dice','sucessful_attacks','damage_per_attack','damage_per_turn']
            DICE_VALIDAITON = ['default_dice', 'damage_roll']
            TAGS_VALIDATION = ['weapon_tags']
            MAG_VALIDATION = ['magazine_size']

            def validate_mag(self, value : str):
                MAG_PATTERN = "/\d{1,3}|N\/A/m"
                return re.fullmatch(MAG_PATTERN, value)

            def validate_dice(self, value : str):
                DICE_PATTERN = "/\d{1,3}[d]([4,6,8]|]|1[0,2])($|[+]\d{1,2})/m"
                return re.fullmatch(DICE_PATTERN, value)
            
            for ele in weapon_dict.items():
                with ele[0] as key, ele[1] as value:
                    match key:
                        case key if key in STRING_VALIDATION:
                            if not isinstance(value, str): return False
                        case key if key in INT_VALIDATION:
                            if not isinstance(value, int): return False
                        case key if key in FLOAT_VALIDATION:
                            if not isinstance(value, float): return False
                        case key if key in DICE_VALIDAITON:
                            if not validate_dice(value): return False
                        case key if key in TAGS_VALIDATION:
                            if not isinstance(value, list[str]): return False
                        case key if key in MAG_VALIDATION:
                            if not validate_mag(value): return False
            return True
        
        def has_tags(self, *tags):
            """Determins if the weapon contains all tags specified"""
            weapon_tags = set(self.get_tags(weapon_dict))
            requested_tags = set(list(tags))
            
            # Returns if all requested_tags is a sub-list of all weapon_tags
            return requested_tags.intersection(weapon_tags) == requested_tags
        
        @property
        def weapon_tags(self, weapon_dict: dict):
            return weapon_dict['weapon_tags'].split(', ')

class WeaponList():

    __weapon_dicts = []
    BLUNT_MOD = 4
    GAME_DICE = 10
    SUCCESS = 7
    CRITICAL_SUCCESS = 14
    # FILE_NAME = './resources/Afterdark 1.02 Weapon Values.csv'
                
    def __init__(self, file : str | pd.DataFrame):
        """From a CSV File or a file path, populate the weapons_list"""

        def path_to_CSV(self, file_path : str):
            """locate a local path from root directory, and return the CSV file assocaited"""
            local_path = os.getcwd()
            parent_directory = os.path.abspath(os.path.join(local_path,os.pardir))
            absolute_directory = os.path.abspath(os.path.join(parent_directory,file_path))
            with (pd.read_csv(absolute_directory)) as csv_file:
                return csv_file
    
        csv_file = None
        if type(file) is str:
            csv_file = path_to_CSV(file)
        elif type(file) is pd.DataFrame:
            csv_file = file

        __weapon_dicts = csv_file.to_dict(orient="rectors")
        

        
            

        # WEAPON_NAME = ""
        # DEFAULT_DAMAGE = ""
        # cp = ""
        # TAGS = []
        # CATAGORY = ""
        # MAG_SIZE = 0


        # weapon_level = 1
        # tag_damage_dice = 0
        # to_hit_bonus = 0
        # succesful_attacks = 0
        # damage_per_attack = 0
        # damage_per_turn = 0

    
    
    def get_shared_tags(self, weapon_dict : dict, *tags : str):
        weapon_tags = self.get_tags(weapon_dict=weapon_dict)
        shared_tags = []

        for tag in tags:
            if tag in weapon_tags:
                shared_tags.append(tag)
        return shared_tags
    
    def parse_weapon(self, weapon_dict : dict, user_entrys : dict):
        weapon_level = user_entrys['weapon_level']
        tag_damage_dice = 0.0
        damage_modifier = user_entrys['damage_modifier']
        to_hit_bonus = user_entrys['to_hit_bonus']
        

        weapon_tags = self.get_tags(weapon_dict)
        
        for tag in weapon_tags:
            match tag:
                case "Automatic":
                    tag_damage_dice += .5
                case "Flexible"|"Cleaving"|"Piercing"|"Incindiary":
                    tag_damage_dice += 1
                case "Explosive":
                    tag_damage_dice += 2
                case "Blunt":
                    damage_modifier += self.BLUNT_MOD
                case "Wieldy":
                    to_hit_bonus += 1

                # All Dictionary Entries Methods should only require (Weapon, and userEntry)

        weapon_calc_dict = {'weapon_level' : weapon_level,
                            'tag_damage_dice' : tag_damage_dice, 'damage_modifier' : damage_modifier,
                            'to_hit_bonus' : to_hit_bonus, 'sucessful_attacks' : get_per_turn(weapon_dict),
                            'damage_per_attack' : get_base_damage(weapon_dict['default_dice'], tag_damage_dice, damage_modifier),
                            'sucessful_attacks' : get_per_turn(weapon_dict), 'damage_per_turn' : get_damage_per_turn()}
        
        weapon_dict['weapon_level'] = user_entrys['weapon_level']
        weapon_dict['tag_damage_dice'] = tag_damage_dice
        weapon_dict['damage_modifier'] = damage_modifier
        weapon_dict['to_hit_bonus'] = to_hit_bonus
        weapon_dict['sucessful_attacks'] = get_per_turn(weapon_dict)
        weapon_dict['damage_per_attack'] = get_base_damage(weapon_dict['default_dice'],tag_damage_dice, damage_modifier)
        weapon_dict['sucessful_attacks'] = get_per_turn(weapon_dict)
        weapon_dict['damage_per_turn'] = '%.2f' % (float(weapon_dict['damage_per_attack']) * float(weapon_dict['sucessful_attacks']))
### END OF WEPAON CLASS        





def get_base_damage(Dice : str | tuple, diceMod : int, wepMod : int = 0):   
    if type(Dice) is str : 
        damageTPL = get_damage_dice(Dice)
    else: 
        damageTPL = Dice
    dmgCalc = ((int(damageTPL[0]) + diceMod) * (float(damageTPL[1])+1) / 2) + wepMod
    return (str(dmgCalc).zfill(4))

def get_damage_dice(Dice : str): 
    return Dice.split('d')    

#Validate damage_dice is Correct
def validate_dice(Dice: str | tuple):


def level_weapon(Weapon : dict, weapon_level : int) -> tuple:
    defaultDamage = get_damage_dice(Weapon['default_dice'])
    

    #How many times the Dice Face can have Leveled Up
    diceFaceMod = min(math.floor(weapon_level/2),2)
    
    #How many more Dice rolled
    diceQuantity = int(defaultDamage[0]) + weapon_level - diceFaceMod

    #Calculate Dice Face, Maximum of D12
    diceFace = min(int(defaultDamage[1]) + diceFaceMod*2,12)
    
    newDice = (diceQuantity,diceFace)
    Weapon['weapon_level'] = weapon_level
    Weapon['damage_dice'] = newDice 
    return newDice

def get_per_atk(weapon : dict, userInfo):
    if weapon is None: raise Exception("Invalid Weapon Dict - Check if Initialized")
    
    baseDamage = get_base_damage(weapon['damage_dice'], weapon['tag_damage_dice'])
    
    weapon['_damageModifer'] = (float(weapon['damage_modifier']) + float(userInfo['damage_modifier']))
    
    damagePerAttack = float(baseDamage) + weapon['damage_modifier']
    return '%f' % damagePerAttack    

def get_per_turn(weapon: dict,sucessRoll = SUCCESS, curCP = 0, val = 0):
    if(GAME_DICE + weapon['to_hit_bonus']) >= sucessRoll + curCP:
        temp = (GAME_DICE + weapon['to_hit_bonus']-(sucessRoll + curCP))/10
        val += temp
        return get_per_turn(weapon, sucessRoll, curCP + int(weapon['cp']), val)
    else:
        return '%.1f' % val