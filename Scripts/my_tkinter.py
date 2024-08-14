from tkinter import *
from tkinter import ttk
from functools import partial
import datetime as objDateTime
from weapon import Weapon

class MyTreeview(ttk.Treeview):
    """Upgrade to the Tkinter treeview, allowing for sorting of headings by data_types

    Assigning headings a sort_type allows you to click it to sort the table by those values.
    Clicking again will invert the sort. Right clicking will clear the sort, and return to original ordering.

    Attributes:
        _previous_sort : A dict that details the previous sort that was completed, and if it should be ignored.
            {
            column : str, default "Default"
                Display name in GUI and keys in property getter 'self.get_entrys()'.
            data_type : int, default 0
                Value that will populate the Entry when created, and if calulate button is clicked with an empty field
            reversed : TK.Entry, Default None
                Refrence object to the Tkinter.Entry GUI Object
            callback : string variable name of TK registered Callback Method - "_int_validation" or "_level_validation"
                Used to assign text validation callback method in entry_object
            }
        _headings : List of tuples that has information regarding the headings  
            (Column, Sort_type, Sort_Function)
    """

    _previous_sort : dict = {"column" : "#0", "data_type" : str, "reverse" : False, "callback" : None, "ignore_sort" : True}
    _headings : list = []

    def heading(self, column, sort_type : str = None, **kwargs):
        """Supports the sort_type argument to the Tkinter Treeview Heading

        Adds the argument sort_type that can be assigned must be assigned when creating a heading
        and binds callback methods to left-clicking and right-clicking the headings

        Args:
            column: string that is used by Tkinter Treeview as the iid for columns.
            sort_type: string that represents the "data_type" that is wished to be sorted by. 
                ['int', 'str', 'date', 'float'] are currently supported "sort_types"
            **kwargs: these are arguments that are default to the heading super method.
                text: text
                    The text to display in the column heading.
                image: imageName
                    Specifies an image to display to the right of the column heading.
                anchor: anchors
                    Specifies how the heading text should be aligned. One of the standard Tk anchor values.
                command: callback
                    A callback to be invoked when the heading label is pressed.
        """
        # Does our header have a sort type, and command is not already set
        if sort_type and not hasattr(kwargs, 'command'):
            # Find callback function for the sort_type requsted
            func = getattr(self, f"sort_by_{sort_type}", None)
            if func:
                # Adds heading information to list of all headings
                self._headings.append({"column" : column, "sort_type" : sort_type, "sort_func" : func})
                self._previous_sort.update({'column' : column, 'callback' : func})
                # Assign callback functions for Left-Click, and Right-Click
                kwargs['command'] = partial(func, column, False)
                self.bind("<Button-3>", self.on_right_click)

        # Creates Tkinter Header normally with our new arguments
        return super().heading(column, **kwargs)
    
    def last_sort(self):
        """Sort the Treeview by the previously sorted type, or ignore the sort
        
        If we are ignoring the previous sort, we need to sort the table at their column, and pass the argument remove_sort = true
        This will return the treeview items to their original index location.
        """
        if self._previous_sort['ignore_sort'] == True:
            self.sort(self._previous_sort["column"], remove_sort = True)
        else:
            parameters = dict(self._previous_sort)
            parameters.pop("ignore_sort")
            self.sort(**parameters)

    def sort(self, column , data_type = str, reverse = False, callback = None, remove_sort : bool = False):
        """
        Sort a column, and changes the sort direction of the header that clicked it.

        At a column, we will sort the by an entered data type associated with a "_sort_by_" function.

        Args:
            column: string that is used by Tkinter Treeview as the iid for columns.
            data_type: a type variable that we use to sort the column in "list.sort()".
            callback: associated function that will be assigned when clicking header. 
            reverse: boolean that represents if we want to return to the original treeview orientation.
        """
        rows = self.get_children('')
        column_values = [(self.set(row, column), row) for row in rows]
        
        # Sort value in column by data_type. If remove_sort = true this will return table to original orientation
        # Than move the row into its index in the sorted list
        column_values.sort(key = lambda t: data_type(t[int(remove_sort)]), reverse=reverse)
        for index, (_, row) in enumerate(column_values):
            self.move(row, '', index)

        if remove_sort is True:
            # Set all headings callback function to the default orientation (Not Reversed)
            for heading in self._headings:
                self.heading(heading['column'], command = partial(heading['sort_func'], heading['column'], False))
        else:
            # Set this columns heading command to sort in the reversed orientation
            self.heading(column, command=partial(callback, column, not reverse))
        # Save information regarding this sort to be refrenced by 'self.last_sort()', and return this sort dictionary
        self._previous_sort.update({'column' : column, "data_type" :  data_type, 'reverse' : reverse, 'callback' : callback, "ignore_sort" : remove_sort})
        return self._previous_sort

    def sort_by_int(self, column, reverse):
        """When clicking header, Sorts table by Columns integers.
        
        Args:
            column: string that is used by Tkinter Treeview as the iid for columns.
            reverse: boolean that represents if we want to return to the original treeview orientation.
        """
        self.sort(column = column, data_type = int, reverse = reverse,  callback = self.sort_by_int)
 
    def sort_by_str(self, column, reverse):
        """When clicking header, Sorts table by Columns strings.
        
        Args:
            column: string that is used by Tkinter Treeview as the iid for columns.
            reverse: boolean that represents if we want to return to the original treeview orientation.
        """
        self.sort(column = column, data_type = str, reverse = reverse,  callback = self.sort_by_str)

    def sort_by_date(self, column, reverse):
        """When clicking header, Sorts table by Columns dates.
        
        Args:
            column: string that is used by Tkinter Treeview as the iid for columns.
            reverse: boolean that represents if we want to return to the original treeview orientation.
        """        
        self.sort(column = column, data_type= objDateTime, reverse = reverse,  callback = self.sort_by_date)
        def _str_to_datetime(string): 
            """Converts String to objDateTime."""
            return objDateTime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def sort_by_float(self, column, reverse):
        """When clicking header, Sorts table by Columns floats.
                
        Args:
            column: string that is used by Tkinter Treeview as the iid for columns.
            reverse: boolean that represents if we want to return to the original treeview orientation.
        """   
        self.sort(column = column, data_type = float, reverse = reverse,  callback = self.sort_by_float)
    
    def on_right_click(self, event):
        """Triggered when right-clicking header treeview, if Header will clear the sort of the treeview
        
        Args:
            event: Tkinter treeview event 
        """
        # If the clicken area of treeview is a heading, clear the treeviews sort.
        region = self.identify_region(event.x, event.y) 
        if region == "heading":
            column = self.identify("column", event.x, event.y)
            self.sort(column = column, remove_sort=True)

class Table():    
    treeview = None
    style = None
    frame = None
    hidden_items = []
    COLUMN_DICT = {'sort_type' : 'str' , 'text' : 'Default', 'anchor': 'c' , 'width' : 80 , 'minwidth' : 60 , 'stretch' : True}

    def __init__(self, root: Tk, cols, bg = "grey", height = "400", relief = FLAT, color_tags : dict = None):
        #Create Frame for holding Table Data.
        tableFrame = Frame(root, bg = bg, relief = relief, height = height)
        tableFrame.grid(column=0, row=0)
        self.frame = tableFrame
         
        # Creates table with column populated form 'cols'.
        self.treeview = MyTreeview(tableFrame, columns=list(cols.keys()), height= 32, selectmode=BROWSE)
        self.treeview.grid(row = 0, rowspan= 5, column = 0, columnspan= 7, sticky=NSEW)
        # Creates scrollbar, and assigns its control functions.
        verScroll = Scrollbar(tableFrame, orient="vertical", command=self.treeview.yview, width= 30)
        verScroll.grid (row = 0, rowspan = 5, column = 8, sticky= NSEW )
        self.treeview.configure(yscrollcommand=verScroll.set)
        # Generates tags to assign colors to rows.
        for name,color in color_tags.items():
            self.treeview.tag_configure(name, background=color)

        # Create table from cols dictionary instrutions
        # Must be formatted as [{'Column #1 Name' : {COLUMN_DICT PARAMETER DICT}},...]
        self.treeview.heading("#0", sort_type='str', text="Default Column")
        self.treeview.column("#0", width=0, minwidth= 0, stretch=False)
        for ele in cols.items(): # For each of the dictionarys key, create a heading and column
            # Default allowed kwargs
            head_kwarg = {'sort_type' : 'str' , 'text' : ele}
            col_kwarg  = {'anchor': 'c' , 'width' : 80 , 'minwidth' : 60 , 'stretch' : True}
            
            # Update our default kwargs with our new values if applicable
            header_parameters = dict(ele[1])
            head_kwarg.update(pair for pair in header_parameters.items() if pair[0] in head_kwarg.keys())
            col_kwarg.update(pair for pair in header_parameters.items() if pair[0] in col_kwarg.keys())

            # Edit existing columns with new parameters
            self.treeview.heading(column=ele[0], **head_kwarg)
            self.treeview.column(column=ele[0], **col_kwarg)

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
        for ele in weapon_list:
            dict = ele.clean_dict()
            self.treeview.item(ele.item_identifier,values=list(dict.values()))
            if filtered_list is not None:
                if ele not in filtered_list:
                    self.hide_item(ele.item_identifier)
                else: 
                    self.unhide_item(ele.item_identifier)
        print(self.treeview._previous_sort)
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

    def delete_table(self):
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

