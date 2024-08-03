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
    root.resizable(width=1, height=1)
    generate_user_fields(root)

    #Create Frame for holding Table Data
    tableFrame = Frame(root, bg = "grey", relief=FLAT, height= 400)
    tableFrame.pack(side=TOP, anchor=NW,expand=True)


    #Create list of all Columns without Weapon Name
    cols = list(weapons.weapon_list[0].keys())
    del cols[0]



    
    myStyle = ttk.Style()
    myStyle.theme_use('clam')
    myStyle.configure('Treeview' , rowheight=22)
    myStyle.layout('my.Treeview',
             [('Treeview.field', {'sticky': 'nswe', 'border': '1', 'children': [
                 ('Treeview.padding', {'sticky': 'nswe', 'children': [
                     ('Treeview.treearea', {'sticky': 'nswe'})
                     ]})
                 ]})
              ])
    myStyle.configure('my.Treeview.Heading', background='gray', font=('Calibri Bold', 10), relief='none')

        #Create Table Object
    table = ttk.Treeview(tableFrame, columns=cols, height= 32, selectmode=BROWSE, style='my.Treeview')
    verScroll = Scrollbar(tableFrame, orient="vertical", command= table.yview, width= 30)
    verScroll.pack(side = 'right', fill=BOTH, padx=2, pady=2)


    table.pack(side=TOP, anchor=NW, expand=True ,fill=BOTH)

    

    #Modifies "Icon Column" - Must be Named #0 when refrenced
    table.heading("#0", text=list(weapons.weapon_list[0].keys())[0]) 
    table.column("#0",width=180, minwidth= 100)

    ##Create All Available Columns
    for count, ele in enumerate(cols):
        head_kwarg = {'text' : ele}
        col_kwarg  = {'anchor': 'e', 'width' : 100, 'minwidth' : 30, 'stretch' : True}

        match ele: 
            case "Default Damage":
                head_kwarg['text'] = "Base Roll"
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 80
                col_kwarg['minwidth'] = 60
            case "CP": 
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 40
                col_kwarg['minwidth'] = 30
            case "Weapon Tags":
                col_kwarg['width'] = 300
                col_kwarg['minwidth'] = 300
            case "Magazine Size":
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 90
                col_kwarg['minwidth'] = 90
            case "Weapon Catagory":
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 120
                col_kwarg['minwidth'] = 120
            case "_level":
                head_kwarg['text'] = "Level"
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 60
                col_kwarg['minwidth'] = 40
            case "_damageDice":
                head_kwarg['text'] = "Damage Dice"
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 80
                col_kwarg['minwidth'] = 80
            case "_tagExtraDice":
                head_kwarg['text'] = "Tag Damage"
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 80
                col_kwarg['minwidth'] = 80
            case "_damageModifier":
                head_kwarg['text'] = "Damage Mod"
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 90
                col_kwarg['minwidth'] = 90
            case "_toHitBonus":
                head_kwarg['text'] = "To Hit"
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 50
                col_kwarg['minwidth'] = 50
            case "_damagePerAttack":
                head_kwarg['text'] = "Damage Per Attack"
                col_kwarg['anchor'] = 'c'
                col_kwarg['width'] = 140
                col_kwarg['minwidth'] = 115
            

        table.heading(column=ele, **head_kwarg)
        table.column(column=ele, **col_kwarg)
        #table.columnconfigure(count+1, weight=1)

    #Populates Table
    for count, ele in enumerate(weapons.weapon_list):
        _weapon = ele
        _weapon['_damageDice'] = 'd'.join(_weapon['_damageDice'])
        if weapons.hasTags(ele,"Blunt")[0] == True:
            _weapon['Default Damage'] = " + ".join((_weapon['Default Damage'], str(weapons.BLUNT_MOD)))
        if not ele['_damageModifier'] == 0:  
            _weapon['_damageDice'] = " + ".join((str(_weapon['_damageDice']), str(int(ele['_damageModifier']))))
        _weapon = list(_weapon.values())
        del _weapon[0]
        #print("item", count , " --- ", _weapon)
        
        

        #= ele['Damage Dice'][0],'d',ele['Damage Dice'][1]
        rowArgs = {'values' : _weapon,'tags' : 'red'}
        match int(ele['CP']):
            case 1:
                rowArgs['tags'] = 'green'
            case 2:
                rowArgs['tags'] = 'yellow'
            case 3:
                rowArgs['tags'] = 'orange'
        table.insert('', END, text=ele['Weapon Name'], **rowArgs)
        table.tag_configure('green', background="#B5CFB7") 
        table.tag_configure('yellow', background="#FAEDCE")
        table.tag_configure('orange', background="#F8C794") 
        table.tag_configure('red', background="#C7B7A3") 





    
    ##tree_1.delete(*tree_1.get_children()) Clear Tree View - Might be Useful LATER





    root.mainloop()

if __name__ == "__main__": 
    __init__()
