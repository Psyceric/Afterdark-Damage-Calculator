from tkinter import *
from tkinter import ttk
from functools import partial
import datetime as objDateTime
import weapons



#Upgrades Treeview to handle Sorting Via Headers
class MyTreeview(ttk.Treeview):

    #Adds sort_by parameter to Headings    
    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs['command'] = partial(func, column, False)
        return super().heading(column, **kwargs)

    #Intakes column, Sorts column by data_type, and assigns reversed callback to header
    def _sort(self, column, reverse, data_type, callback):
        l = [(self.set(k, column), k) for k in self.get_children('')] #For ever row, Get their Item, and their Column
        l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(l):
            self.move(k, '', index)
        self.heading(column, command=partial(callback, column, not reverse))

    #Intakes column, and removes all sorting
    def _remove_sort(self, column):
        #Changes Logic of Sort Function to restore to original order
        l = [(self.set(k, column), k) for k in self.get_children('')]
        l.sort(key=lambda t: str(t[1]) , reverse=False)
        for index, (_, k) in enumerate(l):
            self.move(k, '', index)

    # Callback Function used by _sort
    # When clicking header of a Column, Sorts table by that Columns integers.
    def _sort_by_int(self, column, reverse):
        self._sort(column, reverse, int, self._sort_by_int)

    # Callback Function used by _sort
    # When clicking header of a Column, Sorts table by that Columns strings.
    def _sort_by_name(self, column, reverse):
        self._sort(column, reverse, str, self._sort_by_name)

    # Callback Function used by _sort
    # When clicking header of a Column, Sorts table by that Columns dates.
    def _sort_by_date(self, column, reverse):
        def _str_to_datetime(string):
            return objDateTime.strptime(string, "%Y-%m-%d %H:%M:%S")
        self._sort(column, reverse, _str_to_datetime, self._sort_by_date)

    # Callback Function used by _sort
    # When clicking header of a Column, Sorts table by that Columns floats.
    def _sort_by_float(self, column, reverse):
        self._sort(column, reverse, float, self._sort_by_float)
    
    # Callback Funciton used by _remove_sort
    # When right clicking Header, Remove sorting of table
    def _on_right_click(self, event):
        region = self.identify_region(event.x, event.y)
        region2 = self.identify("column", event.x, event.y)
        if region == "heading":
            self._remove_sort(region2)

### End of MyTreeView Class

class userInfo(object):
    userVariables = {
        "Weapon Level" : 1,
        "To Hit Bonus" : 0, 
        "Damage Modifier" : 0,
        "Number of Attacks" : 0
    }
    userEntryObjects = []

    # Creates UserInfo Fields / Entries /
    def __init__(self, root : Tk):
        if userInfo.userEntryObjects: raise Exception("User Entry Objects Array is Empty. Quitting.")
        # Creates Tkinter frame
        frame = Frame(root, bg = "white", relief=FLAT)
        frame.pack(side=TOP, anchor=NW, expand=True)

        
        
        # Creates a Lable and Entry box for Each key in userVariables
        for count, ele in enumerate(self.userVariables.items()):
            # Create Display Lable with Stat Name
            label = Label(frame, text=ele[0],width=15, bg="white")
            label.grid(row=0, column=count,sticky=EW, padx=1)

            # Create userInfo entry object
            entry = Entry(frame, justify=CENTER,width=15, bg="white", bd=3)
            entry.grid(row=1, column=count,sticky=EW, padx=10, pady=2)
            isDigitRegister = root.register(self.is_digits)
            entry.config(validate="key",validatecommand=(isDigitRegister,'%P'))

            # Instantiate the Entry Box-
            entry.insert(0,ele[1])
            self.userEntryObjects.append(entry)

        #Create Calculate Button, and assign Callback
        calcBtn = Button(frame, text="Calculate", width=15, bg="white",command=self.get_userInfo)
        calcBtn.grid(row=0, column= len(self.userVariables)+1, rowspan=2, sticky=NSEW, padx=(25,0))
    
    #Returns userInfo from all userInfo fields
    def get_userInfo(self):
        _userInfo = dict(self.userVariables)
        print('Getting userInfo')

        # Loops through all userEntryObjects, and saves the text entered into the Entry Objects
        # Returns new dictionary of all user entries
        for count, ele in enumerate(self.userEntryObjects):
            entry = ele.get()
            if entry:
                _userInfo[list(_userInfo.keys())[count]] = entry
        return _userInfo  
     
    #Callback function for Entries to verify if Text is a Digit
    def is_digits(self, input):
        return (input.isdigit() or input == "")
 #
### End of userInfo Class


#Update Weapons Based on User Data    
def update_weapon_list(userInfo):
    
    for i in range(len(weapons.weapon_list)):
        curWeap = weapons.weapon_list[i]
        weapons.level_weapon(curWeap,int(userInfo['Weapon Level']))
        dmgPerAtk = weapons.get_per_atk(curWeap,userInfo)
        weapons.weapon_list[i]['_damagePerAttack'] = dmgPerAtk
        print("{0} | Damage Per Attack - {1}".format(curWeap['Weapon Name'],dmgPerAtk))

def __init__():
    weapons.initilizeWeaponList()
    #Initilize Application, and frame contrainer
    root = Tk()
    root.title("Afterdark™ Damage Per Turn Calculator")
    root.resizable(width=1, height=1)
    userInfo(root)

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
    table.bind("<Button-3>", table._on_right_click)

    verScroll = Scrollbar(tableFrame, orient="vertical", command= table.yview, width= 30)
    verScroll.pack(side = 'right', fill=BOTH, padx=2, pady=2)
    table.pack(side=TOP, anchor=NW, expand=True ,fill=BOTH)
    table.tag_configure('green', background="#B5CFB7") 
    table.tag_configure('yellow', background="#FAEDCE")
    table.tag_configure('orange', background="#F8C794") 
    table.tag_configure('red', background="#C7B7A3")

    #Modifies "Icon Column" - Makes it 0 Width
    table.heading("#0",sort_by='name', text=list(weapons.weapon_list[0].keys())[0]) 
    table.column("#0",width=0, minwidth= 0, stretch=False)

    def generateColumns(columns):
        ##Create All Available Columns
        for count, ele in enumerate(columns):
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
                    head_kwarg['sort_by'] = "int"
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
    
    generateColumns(cols)

    def drawTable():
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
    drawTable()
    def clearTable():
        table.delete(table.get_children())

    root.mainloop()

if __name__ == "__main__":  
    __init__()
