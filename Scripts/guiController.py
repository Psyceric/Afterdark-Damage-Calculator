from tkinter import *
from tkinter import ttk
from functools import partial
import datetime as objDateTime
import weapons

class MyTreeview(ttk.Treeview):
    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs['command'] = partial(func, column, False)
        return super().heading(column, **kwargs)

    def _sort(self, column, reverse, data_type, callback):
        l = [(self.set(k, column), k) for k in self.get_children('')]
        l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(l):
            self.move(k, '', index)
        self.heading(column, command=partial(callback, column, not reverse))

    def _sort_by_num(self, column, reverse):
        self._sort(column, reverse, int, self._sort_by_num)

    def _sort_by_name(self, column, reverse):
        self._sort(column, reverse, str, self._sort_by_name)

    def _sort_by_date(self, column, reverse):
        def _str_to_datetime(string):
            return objDateTime.strptime(string, "%Y-%m-%d %H:%M:%S")
        self._sort(column, reverse, _str_to_datetime, self._sort_by_date)
    def _sort_by_float(self, column, reverse):
        self._sort(column, reverse, float, self._sort_by_float)


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
        weapons.weapon_list[i]['_damagePerAttack'] = dmgPerAtk
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
    table = MyTreeview(tableFrame, columns=cols, height= 32, selectmode=BROWSE, style='my.Treeview')
    verScroll = Scrollbar(tableFrame, orient="vertical", command= table.yview, width= 30)
    verScroll.pack(side = 'right', fill=BOTH, padx=2, pady=2)


    table.pack(side=TOP, anchor=NW, expand=True ,fill=BOTH)

    

    #Modifies "Icon Column" - Must be Named #0 when refrenced
    table.heading("#0",sort_by='name', text=list(weapons.weapon_list[0].keys())[0]) 
    table.column("#0",width=0, minwidth= 0, stretch=False)

    ##Create All Available Columns
    for count, ele in enumerate(cols):
        #Default Row Parameters
        head_kwarg = {'sort_by' : 'name','text' : ele}
        col_kwarg  = {'anchor': 'c', 'width' : 80, 'minwidth' : 60, 'stretch' : True}
        print(ele)
        #Row Parameters
        match ele: 
            case "Weapon Name":
                col_kwarg['width'] = 240
                col_kwarg['minwidth'] = 240
            case "Default Damage":
                head_kwarg['text'] = "Base Roll"
            case "CP": 
                col_kwarg['width'] = 40
                col_kwarg['minwidth'] = 30

            case "Weapon Tags":
                col_kwarg['width'] = 300
                col_kwarg['minwidth'] = 300

            case "Magazine Size":
                col_kwarg['width'] = 90
                col_kwarg['minwidth'] = 90

            case "Weapon Catagory":
                col_kwarg['width'] = 120
                col_kwarg['minwidth'] = 120

            case "_level":
                head_kwarg['text'] = "Level"

            case "_damageDice":
                head_kwarg['text'] = "Damage Dice"
                col_kwarg['minwidth'] = 80

            case "_tagExtraDice":
                head_kwarg['text'] = "Tag Damage"
                col_kwarg['minwidth'] = 80

            case "_damageModifier":
                head_kwarg['text'] = "Damage Mod"
                head_kwarg['sort_by'] = "name"
                col_kwarg['width'] = 90
                col_kwarg['minwidth'] = 90

            case "_toHitBonus":
                head_kwarg['text'] = "To Hit"
                head_kwarg['sort_by'] = "num"
                col_kwarg['width'] = 50
                col_kwarg['minwidth'] = 50

            case "_damagePerAttack":
                head_kwarg['text'] = "Damage Per Attack"
                head_kwarg['sort_by'] = "float"
                col_kwarg['width'] = 140
                col_kwarg['minwidth'] = 115

            case"_averageSucessfulAttacks":
                head_kwarg['text'] = "Sucessful Attacks"
                head_kwarg['sort_by'] = "float"
                col_kwarg['width'] = 115
                col_kwarg['minwidth'] = 115

            case"_DPT":
                head_kwarg['text'] = "Damage Per Turn"
                head_kwarg['sort_by'] = "float"
                col_kwarg['width'] = 115
                col_kwarg['minwidth'] = 115

        table.heading(column=ele, **head_kwarg)
        table.column(column=ele, **col_kwarg)

    #Populates Table
    for count, ele in enumerate(weapons.weapon_list):
        _weapon = dict(ele)
        _weapon['_damageDice'] = 'd'.join(_weapon['_damageDice'])
        if weapons.hasTags(ele,"Blunt")[0] == True:
            _weapon['Default Damage'] = " + ".join(((_weapon['Default Damage']), str(weapons.BLUNT_MOD)))

        if not ele['_damageModifier'] == 0:  
            _weapon['_damageDice'] = " + ".join((str(_weapon['_damageDice']), str(int(ele['_damageModifier']))))
            
        _weapon['_damageModifier'] = "+" + str(int(_weapon['_damageModifier']))
        _weapon['_toHitBonus'] = "+" + str(int(_weapon['_toHitBonus']))

        
        _weapon = list(_weapon.values())


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
