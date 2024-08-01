import csv, os, re, math

weapon_list = []

def main():
    initilizeWeaponList()


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
            case "Flexible"|"Cleaving"|"Piercing"|"Incindiary"|"Explosive":
                tagDamage += 1
            case "Blunt":
                damageModifier += 4
            case "Wieldy":
                toHitBonus += 1

    defaultDice = Weapon.get('Default Damage')
    validate_dice(defaultDice)
    Weapon['_level'] = 1
    Weapon['_damageDice'] = get_damage_dice(defaultDice)
    Weapon['_tagDamage'] = tagDamage
    Weapon['_damageModifier'] = damageModifier
    Weapon['_toHitBonus'] = toHitBonus
    #TODO: ['_damagePerAttack']
    #TODO: ['_damagePerTurn'] and create Function 
    
    # print(
    #     "{0}{1} | {2} : {3} |\tBase Damage: {4}".format(   #Prints Default Weapon Stats
    #         Weapon['Weapon Name'],                         #{0}                       |
    #         " " * (25 - len(Weapon['Weapon Name'])),       #{1}       Does Not        |
    #         Weapon['Default Damage'],                      #{2}  Include Range/Ammo   |
    #         Weapon['_tagDamage'],                          #{3}                       |
    #         Weapon['_baseDamage'])                         #{4}______________________/
    # )

def get_base_damage(Dice : str | tuple):
    if type(Dice) is str : 
        damageTPL = get_damage_dice(Dice)
    else: 
        damageTPL = Dice
    dmgCalc = (int(damageTPL[0]) * (int(damageTPL[1])+1) / 2)
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

if __name__ == "__main__":
    main()

