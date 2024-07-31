import csv, os, re

def main():
    path = os.getcwd()
    parentDirectory = os.path.abspath(os.path.join(path,os.pardir))

    fileName = './resources/Afterdark 1.02 Weapon Values.csv'
    resourcePath = os.path.abspath(os.path.join(parentDirectory,fileName))
    print(resourcePath)

    fields = []
    rows = []

    with open(resourcePath, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        weapon_list = []

        for row in csvreader:
            weapon_list.append(row)
            if parseDamageDice(row['Damage Roll']): print(row['Weapon Name'], "| Damage Validated :", row['Damage Roll'])


def parseDamageDice(Dice):
    dicePattern = "^\\d{1,3}[d]([4,6,8]|]|1[0,2])$" #Regex that Validates number of dice of dice types {4,6,8,10,12}
    if(re.fullmatch(dicePattern,Dice)) : 
        return True
    else:
        return False

if __name__ == "__main__":
    main()