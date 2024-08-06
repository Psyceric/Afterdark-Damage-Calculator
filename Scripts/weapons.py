import csv, os, re, math

weapon_list = []
BLUNT_MOD = 4
GAME_DICE = 10
SUCCESS = 7
CRITICAL_SUCCESS = 14

def initilizeWeaponList():
    #Get all weapons from CSV File
    fileName = './resources/Afterdark 1.02 Weapon Values.csv'
    path = os.getcwd()
    parentDirectory = os.path.abspath(os.path.join(path,os.pardir))
    resourcePath = os.path.abspath(os.path.join(parentDirectory,fileName))
    
    #Validate that resourcePath exists
    print("Attempting to Validate Weapon CSV File at :\n" , resourcePath.strip(),"\n")

    #Error out if File Path is not Valid 
    if os.path.isfile(resourcePath) is None:
        raise Exception("Weapon CSV Unable to be located. : " + fileName)
             
    print("Sucessfully Located Weapon CSV File! Continuing...")
    
    #Open CSV, Loading each row into Weapon_List List
    with open(resourcePath, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            weapon_list.append(row)
            parse_weapon(row)

def hasTags(weapon, *keywords : str): 
    allTags = weapon['weapon_tags'].split(', ')
    returnTags = []
    returnValue = True
    for keyword in keywords: #blunt, two-handed
        if "Blunt" not in allTags:
            #print("Unable to find tag {0} in weapon {1}".format(keyword, weapon['weapon_name']))
            returnValue = False
            returnTags.append(keyword)
    return (returnValue, returnTags)

def parse_weapon(Weapon):
    tagDamage = 0.0
    damageModifier = 0.0
    toHitBonus = 0.0
    
    keywords = Weapon['weapon_tags'].split(',')
    for keyword in keywords:
        _keyword = keyword.strip()
        match _keyword:
            case "Automatic":
                tagDamage += .5
            case "Flexible"|"Cleaving"|"Piercing"|"Incindiary":
                tagDamage += 1
            case "Explosive":
                tagDamage += 2
            case "Blunt":
                damageModifier += BLUNT_MOD
            case "Wieldy":
                toHitBonus += 1

    defaultDice = Weapon['default_damage']

    validate_dice(defaultDice)
    WeaponStats = {}
    Weapon['weapon_level'] = 1
    Weapon['damage_dice'] = get_damage_dice(defaultDice)
    Weapon['tag_damage_dice'] = tagDamage
    Weapon['damage_mod'] = damageModifier
    Weapon['to_hit_bonus'] = toHitBonus
    Weapon['damage_per_attack'] = get_base_damage(defaultDice,tagDamage, damageModifier)
    Weapon['sucessful_attacks'] = get_per_turn(Weapon)
    Weapon['damage_per_turn'] = '%.2f' % (float(Weapon['damage_per_attack']) * float(Weapon['sucessful_attacks']))

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
    
    if type(Dice) is tuple: diceStr = (''.join(map(str, Dice)))
    else: diceStr = Dice

    #Regex that Validates number of dice of dice types {4,6,8,10,12}
    dicePattern = "^\\d{1,3}[d]([4,6,8]|]|1[0,2])$" 

    if (re.fullmatch(dicePattern , diceStr)) is not None : 
        return False
    #If continues, Return True
    return True

def level_weapon(Weapon : dict, weapon_level : int) -> tuple:
    defaultDamage = get_damage_dice(Weapon['default_damage'])
    

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
    
    weapon['_damageModifer'] = (float(weapon['damage_mod']) + float(userInfo['damage_modifier']))
    
    damagePerAttack = float(baseDamage) + weapon['damage_mod']
    return '%f' % damagePerAttack    

def get_per_turn(weapon: dict,sucessRoll = SUCCESS, curCP = 0, val = 0):
    if(GAME_DICE + weapon['to_hit_bonus']) >= sucessRoll + curCP:
        temp = (GAME_DICE + weapon['to_hit_bonus']-(sucessRoll + curCP))/10
        val += temp
        return get_per_turn(weapon, sucessRoll, curCP + int(weapon['CP']), val)
    else:
        return '%.1f' % val