import csv, os, re, math

weapon_list = []
fileName = './resources/Afterdark 1.02 Weapon Values.csv'

def main():
    initilizeWeaponList()

def initilizeWeaponList():
    path = os.getcwd()
    parentDirectory = os.path.abspath(os.path.join(path,os.pardir))
    resourcePath = os.path.abspath(os.path.join(parentDirectory,fileName))
    print(resourcePath)
    
    with open(resourcePath, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            weapon_list.append(row)
            parse_weapon(row)
            level_weapon(row,4)     #- For testing immedietly level to 4
            print(row,"\n")         #- GET DICT TO PRINT

def parse_weapon(Weapon):
    verify_weapon(Weapon)
    baseDamage = get_base_damage(Weapon)
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
    
    # print("{0}{1} | {2} : {3} |\tBase Damage: {4}".format(   #Prints Default Weapon Stats
    # Weapon['Weapon Name'],                                   #{0}                       |
    # " " * (25 - len(Weapon['Weapon Name'])),                 #{1}       Does Not        |
    # Weapon['Default Damage'],                                #{2}  Include Range/Ammo   |
    # tagDamage,                                               #{3}                       |
    # baseDamage))                                             #{4}______________________/
                                                     
    Weapon['_baseDamage'] = baseDamage
    Weapon['_level'] = 1
    Weapon['_damageDice'] = get_damage_dice(Weapon['Default Damage'])
    Weapon['_damageModifier'] = damageModifier
    Weapon['_toHitBonus'] = toHitBonus

def get_base_damage(Weapon):
    dmgDice = get_damage_dice(Weapon['Default Damage'])
    dmgCalc = (int(dmgDice[0]) * (int(dmgDice[1])+1) / 2)
    return (str(dmgCalc).zfill(4))

def level_weapon(Weapon, level):
    defaultDamage = get_damage_dice(Weapon['Default Damage'])
    Weapon['_level'] = level
    
    diceFaceMod = min(math.floor(level/2),2)
    diceFace = math.min(int(defaultDamage[1]) + diceFaceMod*2,12)
    diceQuantityMod = level-diceFaceMod
    diceQuantity = int(defaultDamage[0]) + diceQuantityMod
    Weapon['Damage Dice'] = [diceQuantity,diceFace]

def get_damage_dice(Dice): 
    return Dice.split('d')

def verify_weapon(Weapon):
    dicePattern = "^\\d{1,3}[d]([4,6,8]|]|1[0,2])$" #Regex that Validates number of dice of dice types {4,6,8,10,12}
    if not (re.fullmatch(dicePattern,Weapon['Default Damage'])) : 
        raise TypeError("Unable to Validate Default Damage for '", Weapon['Weapon Name'],"'")

if __name__ == "__main__":
    main()

