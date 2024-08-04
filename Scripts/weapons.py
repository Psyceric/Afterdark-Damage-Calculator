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
    if not os.path.isfile(resourcePath):
        raise Exception("Weapon CSV Unable to be located. : " + fileName)
             
    print("Sucessfully Located Weapon CSV File! Continuing...")
    
    #Open CSV, Loading each row into Weapon_List List
    with open(resourcePath, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            weapon_list.append(row)
            parse_weapon(row)

def hasTags(weapon, *keywords : str): 
    allTags = weapon['Weapon Tags'].split(', ')
    returnTags = []
    returnValue = True
    for keyword in keywords: #blunt, two-handed
        if not "Blunt" in allTags:
            #print("Unable to find tag {0} in weapon {1}".format(keyword, weapon['Weapon Name']))
            returnValue = False
            returnTags.append(keyword)
    return (returnValue, returnTags)

def parse_weapon(Weapon):
    tagDamage = 0.0
    damageModifier = 0.0
    toHitBonus = 0.0
    
    keywords = Weapon['Weapon Tags'].split(',')
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

    defaultDice = Weapon['Default Damage']

    validate_dice(defaultDice)
    WeaponStats = {}
    Weapon['_level'] = 1
    Weapon['_damageDice'] = get_damage_dice(defaultDice)
    Weapon['_tagExtraDice'] = tagDamage
    Weapon['_damageModifier'] = damageModifier
    Weapon['_toHitBonus'] = toHitBonus
    Weapon['_damagePerAttack'] = get_base_damage(defaultDice,tagDamage, damageModifier)
    Weapon['_averageSucessfulAttacks'] = get_per_turn(Weapon)
    Weapon['_DPT'] = '%.2f' % (float(Weapon['_damagePerAttack']) * float(Weapon['_averageSucessfulAttacks']))

def get_base_damage(Dice : str | tuple, diceMod : int, wepMod : int = 0):
    if type(Dice) is str : 
        damageTPL = get_damage_dice(Dice)
    else: 
        damageTPL = Dice
    dmgCalc = ((int(damageTPL[0]) + diceMod) * (float(damageTPL[1])+1) / 2) + wepMod
    return (str(dmgCalc).zfill(4))

def get_damage_dice(Dice : str): 
    return Dice.split('d')    

#Validate Damage Dice is Correct
def validate_dice(Dice: str | tuple):
    
    if type(Dice) is tuple: diceStr = (''.join(map(str, Dice)))
    else: diceStr = Dice

    #Regex that Validates number of dice of dice types {4,6,8,10,12}
    dicePattern = "^\\d{1,3}[d]([4,6,8]|]|1[0,2])$" 

    #Attmepts to Validate Dice, If not Possible Error Out
    if not (re.fullmatch(dicePattern , diceStr)) : 
        raise TypeError("Unable to Validate Default Damage for '", diceStr, "' - of type ", type(diceStr))
    #If continues, Return True
    return True

def level_weapon(Weapon : dict, level : int) -> tuple:
    defaultDamage = get_damage_dice(Weapon['Default Damage'])
    

    #How many times the Dice Face can have Leveled Up
    diceFaceMod = min(math.floor(level/2),2)
    
    #How many more Dice rolled
    diceQuantity = int(defaultDamage[0]) + level - diceFaceMod

    #Calculate Dice Face, Maximum of D12
    diceFace = min(int(defaultDamage[1]) + diceFaceMod*2,12)
    
    newDice = (diceQuantity,diceFace)
    Weapon['_level'] = level
    Weapon['_damageDice'] = newDice 
    return newDice

def get_per_atk(weapon : dict, userInfo):
    if not weapon: raise Exception("Invalid Weapon Dict - Check if Initialized")
    baseDamage = get_base_damage(weapon['_damageDice'], weapon['_tagExtraDice'])
    
    weapon['_damageModifer'] = (float(weapon['_damageModifier']) + float(userInfo['Damage Modifier']))
    
    damagePerAttack = float(baseDamage) + weapon['_damageModifier']
    return '%f' % damagePerAttack    

def get_per_turn(weapon: dict,sucessRoll = SUCCESS, curCP = 0, val = 0):
    if(GAME_DICE + weapon['_toHitBonus']) >= sucessRoll + curCP:
        temp = (GAME_DICE + weapon['_toHitBonus']-(sucessRoll + curCP))/10
        val += temp
        return get_per_turn(weapon, sucessRoll, curCP + int(weapon['CP']), val)
    else:
        return '%.1f' % val