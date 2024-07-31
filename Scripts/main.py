import csv, os, re

weapon_list = []

def main():
    path = os.getcwd()
    parentDirectory = os.path.abspath(os.path.join(path,os.pardir))

    fileName = './resources/Afterdark 1.02 Weapon Values.csv'
    resourcePath = os.path.abspath(os.path.join(parentDirectory,fileName))
    print(resourcePath)
    
    with open(resourcePath, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            weapon_list.append(row)
            parseWeapon(row)
            #Automatic Weapons .5 Tag Damage
            #Flexible,Cleaving,Piercing,Incindiary,Explosive 1 Tag Damage

def parseWeapon(Weapon):
    dicePattern = "^\\d{1,3}[d]([4,6,8]|]|1[0,2])$" #Regex that Validates number of dice of dice types {4,6,8,10,12}

    if not (re.fullmatch(dicePattern,Weapon['Damage Roll'])) : 
        raise TypeError("Unable to Validate Dice", Weapon['Weapon Name'])
    keywords = Weapon['Weapon Tags'].split(',')
    tagDamage = 0.0
    for keyword in keywords:
        _keyword = keyword.strip()
        match _keyword:
            case "Automatic":
                tagDamage += .5
            case "Flexible"|"Cleaving"|"Piercing"|"Incindiary"|"Explosive":
                tagDamage += 1
    print("{0}{1} | {2} : {3}".format(
        Weapon['Weapon Name'],                      #{0}
        " " * (25 - len(Weapon['Weapon Name'])),    #{1}
        Weapon['Damage Roll'],                      #{2}
        tagDamage))                                 #{3}
    
    return True

if __name__ == "__main__":
    main()