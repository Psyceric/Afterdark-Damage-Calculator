import csv, os, re

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
            print(row,"\n")

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
    
        #print("{0}{1} | {2} : {3} |\tBase Damage: {4}".format(
        #Weapon['Weapon Name'],                                 #{0}
        #" " * (25 - len(Weapon['Weapon Name'])),               #{1}
        #Weapon['Damage Roll'],                                 #{2}
        #tagDamage,                                             #{3}
        #baseDamage                                             #{4}
                                                     
    Weapon['Base Damage'] = baseDamage
    Weapon['Level'] = 1
    Weapon['Damage Dice'] = get_damage_dice(Weapon['Damage Roll'])
    Weapon['Damage Modifier'] = damageModifier
    Weapon['To Hit Bonus'] = toHitBonus
    return True

def get_base_damage(Weapon):
    dmgDice = get_damage_dice(Weapon["Damage Roll"])
    dmgCalc = (int(dmgDice[0]) * (int(dmgDice[1])+1) / 2)
    return (str(dmgCalc).zfill(4))

def get_damage_dice(Dice): 
    return Dice.split('d')

def level_weapon(Weapon, level):
    Weapon["Damage Roll"]

def verify_weapon(Weapon):
    dicePattern = "^\\d{1,3}[d]([4,6,8]|]|1[0,2])$" #Regex that Validates number of dice of dice types {4,6,8,10,12}
    if not (re.fullmatch(dicePattern,Weapon['Damage Roll'])) : 
        raise TypeError("Unable to Validate Dice", Weapon['Weapon Name'])

if __name__ == "__main__":
    main()