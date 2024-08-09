from tkinter import *
from tkinter import ttk
from functools import partial
import datetime as objDateTime
from weapon import Weapon

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

class Table():
    treeview = None
    style = None
    frame = None

    def __init__(self, root: Tk, cols, bg = "grey", height = "400", relief = FLAT, anchor = NW, side = TOP, expand = True):
        #Create Frame for holding Table Data
        tableFrame = Frame(root, bg = bg, relief = relief, height = height)
        tableFrame.pack(side = side, anchor = anchor,expand = expand)

        #Create Table Object
        self.treeview = MyTreeview(tableFrame, columns=list(cols.keys()), height= 32, selectmode=BROWSE)
        verScroll = Scrollbar(tableFrame, orient="vertical", command= self.treeview.yview, width= 30)
        verScroll.pack(side = 'right', fill=BOTH, padx=2, pady=2)
        self.treeview.pack(side=TOP, anchor=NW, expand=True ,fill=BOTH)

        self.treeview.tag_configure('green', background="#B5CFB7") 
        self.treeview.tag_configure('yellow', background="#FAEDCE")
        self.treeview.tag_configure('orange', background="#F8C794") 
        self.treeview.tag_configure('red', background="#C7B7A3")
        self.frame = tableFrame

    def initiate_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview' , rowheight=22)
        self.style.layout('my.Treeview',
                [('Treeview.field', {'sticky': 'nswe', 'border': '1', 'children': [
                    ('Treeview.padding', {'sticky': 'nswe', 'children': [
                        ('Treeview.treearea', {'sticky': 'nswe'})
                        ]})
                    ]})
                ])    
        self.style.configure('my.Treeview.Heading', background='gray', font=('Calibri Bold', 10), relief='none')
        return self.style

    def get_style(self):
        return self.style
    
    def get_treeview(self):
        return self.treeview()
    
    def initiate_columns(self, cols):  # HERE
        #Modifies "Icon Column" - Makes it 0 Width
        self.treeview.heading("#0", sort_type='str', text="Weapons List")
        self.treeview.column("#0", width=0, minwidth= 0, stretch=False)
    
        for count, ele in enumerate(cols.keys()): # For each of the dictionarys key, create a heading and column
            #Default Row Parameters
            head_kwarg = {'sort_type' : 'str' , 'text' : ele}
            col_kwarg  = {'anchor': 'c' , 'width' : 80 , 'minwidth' : 60 , 'stretch' : True}
            #Column Parameters
            match ele: 
                case "name":
                    head_kwarg['text'] = "Weapon Name"
                    col_kwarg['width'] = 240
                    col_kwarg['minwidth'] = 240
                case "default_dice":
                    head_kwarg['text'] = "Default Roll"
                    col_kwarg['width'] = 90
                    col_kwarg['minwidth'] = 90
                case "cp": 
                    head_kwarg['text'] = "CP"
                    col_kwarg['width'] = 40
                    col_kwarg['minwidth'] = 30

                case "tags":
                    head_kwarg['text'] = "Weapon Tags"
                    col_kwarg['width'] = 300
                    col_kwarg['minwidth'] = 300

                case "magazine_size":
                    head_kwarg['text'] = "Mag Size"
                    col_kwarg['width'] = 90
                    col_kwarg['minwidth'] = 90

                case "category":
                    head_kwarg['text'] = "Weapon Type"
                    col_kwarg['width'] = 120
                    col_kwarg['minwidth'] = 120

                case "level":
                    head_kwarg['text'] = "Level"

                case "damage_dice":
                    head_kwarg['text'] = "Damage Dice"
                    col_kwarg['minwidth'] = 80

                case "situation_dice":
                    head_kwarg['text'] = "Tag Damage"
                    col_kwarg['minwidth'] = 80

                case "damage_modifier":
                    head_kwarg['text'] = "Damage Mod"
                    col_kwarg['width'] = 90
                    col_kwarg['minwidth'] = 90

                case "damage_roll":
                    head_kwarg['text'] = "Damage Roll"
                    col_kwarg['width'] = 90
                    col_kwarg['minwidth'] = 90

                case "to_hit_bonus":
                    head_kwarg['text'] = "To Hit"
                    head_kwarg['sort_type'] = "int"
                    col_kwarg['width'] = 50
                    col_kwarg['minwidth'] = 50

                case "attack_damage":
                    head_kwarg['text'] = "Damage Per Attack"
                    head_kwarg['sort_type'] = "float"
                    col_kwarg['width'] = 140
                    col_kwarg['minwidth'] = 115

                case"average_attacks":
                    head_kwarg['text'] = "Sucessful Attacks"
                    head_kwarg['sort_type'] = "float"
                    col_kwarg['width'] = 115
                    col_kwarg['minwidth'] = 115

                case"average_damage_per_turn":
                    head_kwarg['text'] = "Damage Per Turn"
                    head_kwarg['sort_type'] = "float"
                    col_kwarg['width'] = 115
                    col_kwarg['minwidth'] = 115
                case _:
                    print("NON AVAILABLE FOR :", ele)
            self.treeview.heading(column=ele, **head_kwarg)
            self.treeview.column(column=ele, **col_kwarg)

    def draw_table(self, weapon_list : list[Weapon]):
        #Populates Table
        for count, ele in enumerate(weapon_list):
            dict = ele.to_dict()
            dict['tags'] = ",".join(dict['tags'])
            rowArgs = {'values' : list(dict.values()),'tags' : 'white'}
            match ele.cp:
                case 1:
                    rowArgs['tags'] = 'green'
                case 2:
                    rowArgs['tags'] = 'yellow'
                case 3:
                    rowArgs['tags'] = 'orange'
            self.treeview.insert('', END, text=ele.name, **rowArgs)

    def clear_table(self):
        self.treeview.delete(self.treeview.get_children())