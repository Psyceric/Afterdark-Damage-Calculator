from tkinter import *
from tkinter import ttk
from functools import partial
import datetime as objDateTime
from weapon import Weapon

class MyTreeview(ttk.Treeview):
    """Upgrades Tkinter Treeview to allow header sorting functionality
    Adds multiple sort options. """
    _sort_param : tuple
    _headings : list = []
    _sort_callback = None

    def heading(self, column, sort_type : str = None, **kwargs):
        """Dynamically set headings Callback function using sort_type
        If arguments 'sort_type' exists & 'command' does not exists
        Find Function in class of sort_type 
        If it exists assing callback function to heading"""
        if sort_type and not hasattr(kwargs, 'command'):
            func = getattr(self, f"sort_by_{sort_type}", None)
            if func:
                self._headings.append((column, func, sort_type))   
                self._sort_param = (column, str, False, func, False)
                kwargs['command'] = partial(func, column, False)

        # Bind function to Right Click callback from Tkinter Treeview
        self.bind("<Button-3>", self.on_right_click)

        return super().heading(column, **kwargs)
    
    def last_sort(self):
        print(self._sort_param[4])
        if self._sort_param[4] == True:
            self.sort(self._sort_param[0], self._sort_param[1], self._sort_param[2], self._sort_param[3])
        else:
            self.sort(self._sort_param[0], remove_sort = True)

    def sort(self, column, data_type = str, reverse = False, callback = None, remove_sort : bool = False, filtered_list : list[Weapon] = []):
        """ Sorts Treeview by Column and Data Type
        Creats List of all row ID's 
        Converts to list of values in a column
        Sort list by data_type"""
        self._sort_column = column
        allRows = self.get_children('')
        sortedRows = [(self.set(row, column), row) for row in allRows]
        sortedRows.sort(key=lambda tup: data_type(tup[int(remove_sort)]), reverse=reverse)

        # Move each row to index it appears in sortedRows
        # Re-assigns callback function to header with oppsite sort order
        for index, (_, row) in enumerate(sortedRows):
            self.move(row, '', index)
        
        if remove_sort is False:
            self.heading(column, command=partial(callback, column, not reverse))
            self._sort_param = (column, data_type, reverse, callback, True)
        else:
            for heading in self._headings:
                self.heading(heading[0], command = partial(heading[1], heading[0], False))
            self._sort_param = (column, data_type, False, callback, False)
        #print("Sorting Column {0}, by data_type : {1}".format(column,data_type))
        self._sort_callback()

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

    def assign_sort_callback(self, callback):
        self._sort_callback = callback
     #
    ### End of MyTreeView Class

class Table():
    treeview = None
    style = None
    frame = None
    update_callback = None
    hidden_items = []

    def __init__(self, root: Tk, cols, bg = "grey", height = "400", relief = FLAT, callback = None):
        #Create Frame for holding Table Data
        tableFrame = Frame(root, bg = bg, relief = relief, height = height)
        tableFrame.grid(column=0, row=0)

        #Create Table Object
        self.treeview = MyTreeview(tableFrame, columns=list(cols.keys()), height= 32, selectmode=BROWSE)
        verScroll = Scrollbar(tableFrame, orient="vertical", command=self.treeview.yview, width= 30)
        verScroll.grid (row = 0, rowspan = 5, column = 8, sticky= NSEW )
        self.treeview.configure(yscrollcommand=verScroll.set)
        self.treeview.grid(row = 0, rowspan= 5, column = 0, columnspan= 7, sticky=NSEW)


        self.treeview.tag_configure('green', background="#B5CFB7") 
        self.treeview.tag_configure('yellow', background="#FAEDCE")
        self.treeview.tag_configure('orange', background="#F8C794") 
        self.treeview.tag_configure('red', background="#C7B7A3")
        self.frame = tableFrame
        self.update_callback = callback
        self.treeview.assign_sort_callback(callback=callback)

    def initiate_style(self): # Currently Broken
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

                case "situational_dice":
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
                    col_kwarg['width'] = 50
                    col_kwarg['minwidth'] = 50

                case "attack_damage":
                    head_kwarg['text'] = "Dmg Per Attack"
                    head_kwarg['sort_type'] = "float"
                    col_kwarg['width'] = 120
                    col_kwarg['minwidth'] = 80

                case"average_attacks":
                    head_kwarg['text'] = "Attacks"
                    head_kwarg['sort_type'] = "float"
                    col_kwarg['width'] = 80
                    col_kwarg['minwidth'] = 80

                case"average_damage_per_turn":
                    head_kwarg['text'] = "Dmg Per Turn"
                    head_kwarg['sort_type'] = "float"
                    col_kwarg['width'] = 80
                    col_kwarg['minwidth'] = 80
                case _:
                    print("NON AVAILABLE FOR :", ele)
            self.treeview.heading(column=ele, **head_kwarg)
            self.treeview.column(column=ele, **col_kwarg)

    def draw_table(self, weapon_list : list[Weapon]):
        #Populates Table
        for ele in weapon_list:
            dict = ele.clean_dict()
            rowArgs = {'values' : list(dict.values()),'tags' : 'white'}
            match ele.cp:
                case 1:
                    rowArgs['tags'] = 'green'
                case 2:
                    rowArgs['tags'] = 'yellow'
                case 3:
                    rowArgs['tags'] = 'orange'
            item = self.treeview.insert('', END, text=ele.name, **rowArgs)
            ele.item_identifier = item
            ele.item_index = self.treeview.index(item)

    def redraw_table(self, weapon_list : list[Weapon], filtered_list : list[Weapon] = []):
        prune = []
        redraw = []

        for ele in weapon_list:
            dict = ele.clean_dict()
            self.treeview.item(ele.item_identifier,values=list(dict.values()))
            if ele not in filtered_list:
                self.hide_item(ele.item_identifier)
            else: 
                self.unhide_item(ele.item_identifier)
        self.treeview.last_sort()    

    def hide_item(self, iid):
        d = self.treeview.get_children()
        if iid in d:
            self.treeview.detach(iid)
            self.hidden_items.append(iid)
            print("Hiding Item : ", iid)

    def unhide_item(self, iid):
        d = self.treeview.get_children()
        if iid in self.hidden_items:
            self.treeview.move(iid, '', len(d))
            self.hidden_items.remove(iid)

    def clear_table(self):
        self.treeview.delete(self.treeview.get_children())

class FilterMenu(): 
    frame : Frame
    _tags : list[str]
    _names : list[str]
    _categorys : list[str]
    _cps : list[str]
    _callback = None


    _filters = {
        "tags" : [],
        "names" : [],
        "categorys" : [],
        "cps" : []
    }

    def __init__(self, root : Tk, weapons_list : list[Weapon], filter_callback):
        filter_frame = Frame(root, bg='yellow', width=150, height=300, padx=3, pady=3, relief= FLAT)
        filter_frame.grid(row=0, column=0, sticky=NSEW)
        my_filters = Label(filter_frame, text= "Filters", justify = CENTER,  width=6, height = 1, font=("Arial", 25) )
        my_filters.grid(column=0, columnspan = 3, row=0,  sticky=EW)
        

        self.get_info(weapons_list)
        self._callback = filter_callback
        for count, ele in enumerate((self._tags, self._categorys, self._cps)):
            label = Label(filter_frame, text=ele['name'], width=ele['width'])
            label.grid(column=count, row=3, sticky=NSEW, pady = (25,0))
            
            listbox = Listbox(filter_frame, selectmode="multiple", exportselection=0, height=len(ele['values']), width=ele['width'], activestyle='none')
            listbox.config( justify=CENTER, borderwidth=3)
            for entry in ele['values']:
                listbox.insert(END, entry)

            func = getattr(self, "_update_filters")
            listbox.bind("<<ListboxSelect>>", partial(func, ele))
            listbox.grid(column=count, row=4, sticky=NSEW)
        
    def _update_filters(self, element, event : Event):
        listbox = event.widget
        res = [listbox.get(sel) for sel in listbox.curselection()]
        self._filters[str(element['name'].lower())] = res
        print(self._filters)
        self._callback()

    def get_filter(self):
        return self._filters

    def get_info(self, weapons_list : list[Weapon]):
        # Maybe do this via to_dict of wepaon
        all_tags = []
        all_categorys = []
        all_names = []
        all_cp = []

        for ele in weapons_list:
            for tag in ele.tags:
                if tag not in all_tags:
                    all_tags.append(tag)
            if ele.category not in all_categorys:
                all_categorys.append(ele.category)
            if ele.name not in all_names:
                all_names.append(ele.name)
            if ele.cp not in all_cp:
                all_cp.append(ele.cp)
        all_tags.sort()
        all_names.sort()
    
        self._tags = {
        "name" : "Tags",
        "width" : 18, 
        "values" : all_tags
        }

        self._categorys = {
        "name" : "Categorys",
        "width" : 15, 
        "values" : all_categorys
        }
        
        self._names = {
        "name" : "Names ",
        "width" : 15, 
        "values" : all_names
        }

        self._cps = {
        "name" : "CPs",
        "width" : 7, 
        "values" : all_cp
        }

