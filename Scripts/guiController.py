from tkinter import *
from tkinter import ttk
from functools import partial
import datetime as objDateTime
import weapons



class MyTreeview(ttk.Treeview):
    """Upgrades Tkinter Treeview to allow header sorting functionality
    Adds multiple sort options. """

    def heading(self, column, sort_type : str = None, **kwargs):
        """Dynamically set headings Callback function using sort_type
        If arguments 'sort_type' exists & 'command' does not exists
        Find Function in class of sort_type 
        If it exists assing callback function to heading"""
        if sort_type and not hasattr(kwargs, 'command'):
            func = getattr(self, f"sort_by_{sort_type}", None)
            if func:
                kwargs['command'] = partial(func, column, False)

        # Bind function to Right Click callback from Tkinter Treeview
        self.bind("<Button-3>", self.on_right_click)        
        return super().heading(column, **kwargs)

    def sort(self, column, data_type = str, reverse = False, callback = None, remove_sort : bool = False):
        """ Sorts Treeview by Column and Data Type
        Creats List of all row ID's 
        Converts to list of values in a column
        Sort list by data_type"""
        
        allRows = self.get_children('')
        sortedRows = [(self.set(row, column), row) for row in allRows]
        sortedRows.sort(key=lambda tup: data_type(tup[int(remove_sort)]), reverse=reverse)

        # Move each row to index it appears in sortedRows
        # Re-assigns callback function to header with oppsite sort order
        for index, (_, row) in enumerate(sortedRows):
            self.move(row, '', index)

        if remove_sort is False:
            self.heading(column, command=partial(callback, column, not reverse))

    def sort_by_int(self, column, reverse):
        """When clicking header, Sorts table by Columns integers."""
        self.sort(column = column, data_type = int, reverse = reverse,  callback = self.sort_by_int)
 
    def sort_by_str(self, column, reverse):
        """When clicking header, Sorts table by Columns strings."""
        self.sort(column = column, data_type = str, reverse = reverse,  callback = self.sort_by_str)

    def sort_by_date(self, column, reverse):
        """When clicking header, Sorts table by Columns dates."""
        def _str_to_datetime(string): 
            # Used to convert string to dateTime Object
            return objDateTime.strptime(string, "%Y-%m-%d %H:%M:%S")
        self.sort(column = column, data_type= objDateTime, reverse = reverse,  callback = self.sort_by_date)

    def sort_by_float(self, column, reverse):
        """When clicking header, Sorts table by Columns floats."""
        self.sort(column = column, data_type = float, reverse = reverse,  callback = self.sort_by_float)
    
    def on_right_click(self, event):
        """When rightclicking identify if clicking header, and clear sort"""
        region = self.identify_region(event.x, event.y)
        column = self.identify("column", event.x, event.y)
        if region == "heading":
            self.sort(column = column, remove_sort=True)
     #
    ### End of MyTreeView Class

class UserFields(object):
    """Handles creating / updating / and gathering information from User Input Fields"""
    user_entrys = []
      
    def __init__(self, root : Tk):
        """Generates main body of userFields, creating in root frame from Tkinter"""
        
        # Default values for user_entry
        USER_ENTRY_DEFAULT = {
            "name" : "Default" ,
            "default_value" : 0,
            "current_value" : 0,
            "entry_object" : None,
            "colomn_refrence" : None,
            "entry_register" : self.validate_int}
        
        #Array of user_entry's to be created. Parameters must be in USER_ENTRY_DEFAULT dictionary
        user_entry_parameters = [
            {"name" : "weapon_level", "default_value" : 1},
            {"name" : "to_hit_bonus"},
            {"name" : "damage_modifier"},
            {"name" : "number_of_attacks"}
        ]

        #Dynamically creates list of user_entry
        self.user_entrys = self.generate_userEntrys(USER_ENTRY_DEFAULT,user_entry_parameters)
        

        # Tkinter Frame object to hold all elements
        frame = Frame(root, bg = "white", relief=FLAT)
        frame.pack(side=TOP, anchor=NW, expand=True)
        
        for count, ele in enumerate(self.user_entrys):
        # Dynamically create user Entry fields, assigning values in userEntries array

            # Create Display Lable with Stat Name
            label = Label(frame, text=ele['name'],width=15, bg="white")
            label.grid(row=0, column=count,sticky=EW, padx=1)

            # Create userInfo entry object
            entry = Entry(frame, justify=CENTER,width=15, bg="white", bd=3)
            entry.grid(row=1, column=count,sticky=EW, padx=10, pady=2)

            # Registers and assigns text validation function
            isDigitRegister = root.register(ele['entry_register'])
            entry.config(validate="key",validatecommand=(isDigitRegister,'%P'))

            #Updates user_entry information about its entryBox
            ele['entry_object'] = entry
            ele['current_value'] = entry.get()
            ele['colomn_refrence'] = count
            
            # Instantiate the Entry Box into the application
            entry.insert(0,ele['default_value'])


        #Create buttonm, and assign it to trigger update_userInfo when clicked
        calcBtn = Button(frame, text="Calculate", width=15, bg="white",command=self.get_userEntrys)
        calcBtn.grid(row=0, column= len(self.user_entrys)+1, rowspan=2, sticky=NSEW, padx=(25,0))

    def generate_userEntrys(self, default_parameters, _allParameters : list[dict]):
        """Creates new user entry field from list of parameters"""

        def generate_userEntry(default_parameters, parameter):
            """Creates dictionary that has changes from user_entry
            that are shared betweent he two dictionaries"""
            
            # Create Local copy, and loop through all items
            user_entry = dict(default_parameters)
            for key, value in parameter.items():
                if key in default_parameters.keys():
                    # If this item's key is shared between the two. Update local copy
                    user_entry[key] = value  

            # Return parameter list for generating user_entry      
            return user_entry

        #Generates parameter dictionary for each object in _allParameters
        allUserEntries = []
        for parameter in _allParameters:
            allUserEntries.append(generate_userEntry(default_parameters, parameter = parameter))
        return allUserEntries
    
    def get_userEntrys(self):
        """Collect all information from user_entrys
           Update internal values"""
        
        returnValues = []
        for count, ele in enumerate(self.user_entrys):
            # For ever field in user_entrys get input, and return list of all inputs    
            currVal = ele['entry_object'].get()
            #Update user_entry with new input
            ele['current_value'] = currVal
            returnValues.append((ele['name'],ele['entry_object'].get()))
     
        # TODO : Trigger updateTable funtion (returnValues)
        return returnValues

    def validate_int(self, input):
        """Used to validate text input in TTK.Entry"""
        return (input.isdigit() or input == "")
    
     #
    ### End of userInfo Class

class Table():
    __treeview = None
    __style = None
    __frame = None

    def __init__(self, root: Tk, cols, bg = "grey", height = "400", relief = FLAT, anchor = NW, side = TOP, expand = True):
        #Create Frame for holding Table Data
        tableFrame = Frame(root, bg = bg, relief = relief, height = height)
        tableFrame.pack(side = side, anchor = anchor,expand = expand)
    
        #Create Table Object
        self.__treeview = MyTreeview(tableFrame, columns=cols, height= 32, selectmode=BROWSE, style=self.__style)
        verScroll = Scrollbar(tableFrame, orient="vertical", command= self.__treeview.yview, width= 30)
        verScroll.pack(side = 'right', fill=BOTH, padx=2, pady=2)
        self.__treeview.pack(side=TOP, anchor=NW, expand=True ,fill=BOTH)
        self.__treeview.tag_configure('green', background="#B5CFB7") 
        self.__treeview.tag_configure('yellow', background="#FAEDCE")
        self.__treeview.tag_configure('orange', background="#F8C794") 
        self.__treeview.tag_configure('red', background="#C7B7A3")
        self.__frame = tableFrame

    def initiate_style(self):
        self.__style = ttk.Style()
        self.__style.theme_use('clam')
        self.__style.configure('Treeview' , rowheight=22)
        self.__style.layout('my.Treeview',
                [('Treeview.field', {'sticky': 'nswe', 'border': '1', 'children': [
                    ('Treeview.padding', {'sticky': 'nswe', 'children': [
                        ('Treeview.treearea', {'sticky': 'nswe'})
                        ]})
                    ]})
                ])    
        self.__style.configure('my.Treeview.Heading', background='gray', font=('Calibri Bold', 10), relief='none')
        return self.__style

    def get_style(self):
        return self.__style
    
    def get_treeview(self):
        return self.__treeview()
    
    def initiate_columns(self, cols):
        #Modifies "Icon Column" - Makes it 0 Width
        self.__treeview.heading("#0",sort_type='str', text=list(weapons.weapon_list[0].keys())[0])
        self.__treeview.column("#0",width=0, minwidth= 0, stretch=False)

        for count, ele in enumerate(cols):
            #Default Row Parameters
            head_kwarg = {'sort_type' : 'str','text' : ele}
            col_kwarg  = {'anchor': 'c', 'width' : 80, 'minwidth' : 60, 'stretch' : True}
            
            #Column Parameters
            match ele: 
                case "weapon_name":
                    head_kwarg['text'] = "Weapon Name"
                    col_kwarg['width'] = 240
                    col_kwarg['minwidth'] = 240
                case "default_dice":
                    head_kwarg['text'] = "Base Roll"
                    col_kwarg['width'] = 60
                    col_kwarg['minwidth'] = 50
                case "cp": 
                    col_kwarg['width'] = 40
                    col_kwarg['minwidth'] = 30

                case "weapon_tags":
                    head_kwarg['text'] = "Weapon Tags"
                    col_kwarg['width'] = 300
                    col_kwarg['minwidth'] = 300

                case "magazine_size":
                    head_kwarg['text'] = "Magazine Size"
                    col_kwarg['width'] = 90
                    col_kwarg['minwidth'] = 90

                case "weapon_category":
                    head_kwarg['text'] = "Weapon Category"
                    col_kwarg['width'] = 120
                    col_kwarg['minwidth'] = 120

                case "weapon_level":
                    head_kwarg['text'] = "Weapon Level"

                case "damage_dice":
                    head_kwarg['text'] = "Damage Dice"
                    col_kwarg['minwidth'] = 80

                case "tag_damage_dice":
                    head_kwarg['text'] = "Tag Damage"
                    col_kwarg['minwidth'] = 80

                case "damage_modifier":
                    head_kwarg['text'] = "Damage Modifier"
                    col_kwarg['width'] = 90
                    col_kwarg['minwidth'] = 90

                case "to_hit_bonus":
                    head_kwarg['text'] = "To Hit Bonus"
                    head_kwarg['sort_type'] = "int"
                    col_kwarg['width'] = 50
                    col_kwarg['minwidth'] = 50

                case "damage_per_attack":
                    head_kwarg['text'] = "Damage Per Attack"
                    head_kwarg['sort_type'] = "float"
                    col_kwarg['width'] = 140
                    col_kwarg['minwidth'] = 115

                case"sucessful_attacks":
                    head_kwarg['text'] = "Sucessful Attacks"
                    head_kwarg['sort_type'] = "float"
                    col_kwarg['width'] = 115
                    col_kwarg['minwidth'] = 115

                case"damage_per_turn":
                    head_kwarg['text'] = "Damage Per Turn"
                    head_kwarg['sort_type'] = "float"
                    col_kwarg['width'] = 115
                    col_kwarg['minwidth'] = 115

            self.__treeview.heading(column=ele, **head_kwarg)
            self.__treeview.column(column=ele, **col_kwarg)

    def draw_table(self):
        #Populates Table
        for count, ele in enumerate(weapons.weapon_list): # SIN
            _weapon = dict(ele)
            _weapon['damage_dice'] = 'd'.join(_weapon['damage_dice'])
            if weapons.hasTags(ele,"Blunt")[0] == True:
                _weapon['default_dice'] = " + ".join(((_weapon['default_dice']), str(weapons.BLUNT_MOD)))

            if not ele['damage_modifier'] == 0:  
                _weapon['damage_dice'] = " + ".join((str(_weapon['damage_dice']), str(int(ele['damage_modifier']))))
                
            _weapon['damage_modifier'] = "+" + str(int(_weapon['damage_modifier']))
            _weapon['to_hit_bonus'] = "+" + str(int(_weapon['to_hit_bonus']))

            _weapon = list(_weapon.values())


            rowArgs = {'values' : _weapon,'tags' : 'red'}
            match int(ele['cp']):
                case 1:
                    rowArgs['tags'] = 'green'
                case 2:
                    rowArgs['tags'] = 'yellow'
                case 3:
                    rowArgs['tags'] = 'orange'
            self.__.insert('', END, text=ele['weapon_name'], **rowArgs)

    def clear_table(self):
        self.__treeview.delete(self.__treeview.get_children())

#Update Weapons Based on User Data    
def update_weapon_list(self, userInfo): 
    for i in range(len(weapons.weapon_list)):

        curWeap = weapons.weapon_list[i]
        weapons.level_weapon(curWeap,int(userInfo['weapon_level']))
        dmgPerAtk = weapons.get_per_atk(curWeap,userInfo)
        weapons.weapon_list[i]['damage_per_attack'] = dmgPerAtk
        print("{0} | damage_per_attack - {1}".format(curWeap['weapon_name'],dmgPerAtk))

def __init__(self):
    weapons.initilizeWeaponList()
    cols = list(weapons.weapon_list[0].keys())           # - > Should be function from weapons class IS SIN CODE

    #Initilize Application
    root = Tk()
    root.title("Afterdark™ Damage Per Turn Calculator")
    root.resizable(width=1, height=1)
    
    UserFields(root = root)                              # - > Add more Init parameters
    Table(root=root, cols=cols)

    root.mainloop()

if __name__ == "__main__":  
    __init__()
