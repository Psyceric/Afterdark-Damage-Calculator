from tkinter import *
from tkinter import ttk
import weapons

#(Variable name, Default Value)
userVariables = {
    "Weapon Level" : 1,
    "To Hit Bonus" : 0, 
    "Damage Modifier" : 0,
    "Number of Attacks" : 0
}
userVarEntrys = []
_userInfoFrame = None
_tableFrame = None

#Callback function for Digits
def is_digits(input):
    if input.isdigit() or input == "":
        return True
    else:
        return False
    
#Prints User Variables
def get_user_variables():
    if userVarEntrys:
        entries = dict(userVariables)
        for i in range(len(userVarEntrys)):
            entry = userVarEntrys[i].get()
            if entry:
                entries[list(entries.keys())[i]] = entry
        print(entries)

    for i in range(len(weapons.weapon_list)):
        curWeap = weapons.weapon_list[i]
        weapons.level_weapon(curWeap,int(entries['Weapon Level']))
        dmgPerAtk = weapons.get_per_atk(curWeap,entries)
        weapons.weapon_list[i]['_weaponStats']['_damagePerAttack'] = dmgPerAtk
        print("{0} | Damage Per Attack - {1}".format(curWeap['Weapon Name'],dmgPerAtk))

def generate_table(frame, table):
    None

def generate_user_fields(root):
    #Create Frame for userInfo buttons
    frame = Frame(root, bg = "white", relief=FLAT)
    frame.pack(side=TOP, anchor=NW, expand=True)
    _userInfoFrame = frame
    #Creates Entry Fields for User Variables
    for i in range(len(userVariables)):

        #Create Labels and Entries in rows
        label = Label(frame, text=list(userVariables.keys())[i], width=15, bg="white")
        entry = Entry(frame, justify=CENTER, width=15, bg="white", bd=3)
        label.grid(row=0, column=i, sticky=EW, padx=1)
        entry.grid(row=1, column=i, sticky=EW, padx=10, pady=2)

        #Assign Callback, limit entry to digits only
        isDigitRegister = root.register(is_digits)
        entry.config(validate="key",validatecommand=(isDigitRegister,'%P'))
        entry.insert(0,list(userVariables.values())[i])


        #Add Entry to list of Entries
        userVarEntrys.append(entry)

    #Create Calculate Button and Connecty to get_user_variables method
    calcBtn = Button(frame, text="Calculate", width=15, bg="white",command=get_user_variables)
    calcBtn.grid(row=0, column= len(userVariables)+1, rowspan=2, sticky=NSEW, padx=(25,0))

def merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def __init__():
    weapons.initilizeWeaponList()
    
    #Initilize Application, and frame contrainer
    root = Tk()
    root.title("Afterdark™ Damage Per Turn Calculator")
    generate_user_fields(root)

    #Create Frame for holding Table Data
    tableFrame = Frame(root, bg = "white", relief=FLAT)
    tableFrame.pack(side=TOP, anchor=NW,expand=True)
    cols = []
    combinedWeaponsList = merge(weapons.weapon_list[0] , weapons.weapon_list[0]['_weaponStats'])
    for ele in combinedWeaponsList.items():
        if not isinstance(ele[1],dict) and not ele[0] == "Weapon Name":
            cols.append(ele[0])

    table = ttk.Treeview(tableFrame, columns=cols)
    for eachcol in cols:
        table.heading(column=eachcol, text=eachcol)
        table.column(column=eachcol, width=100, minwidth=30)
        
    table.heading("#0", text="Weapon Name")
    table.column('#0', width=0, minwidth=0)

    table.pack(side=TOP, anchor=NW, expand=True ,fill=BOTH)
    
    ##tree_1.delete(*tree_1.get_children()) Clear Tree View - Might be Useful LATER





    root.mainloop()

if __name__ == "__main__":
    __init__()
