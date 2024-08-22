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
        _previous_sort: A dict that details the previous sort that was completed, and if it should be ignored.
            {
            column: str, default "Default"
                Display name in GUI and keys in property getter 'self.get_entrys()'.
            data_type: int, default 0
                Value that will populate the Entry when created, and if calulate button is clicked with an empty field
            reversed: TK.Entry, Default None
                Refrence object to the Tkinter.Entry GUI Object
            callback: string variable name of TK registered Callback Method - "_int_validation" or "_level_validation"
                Used to assign text validation callback method in entry_object
            }
        _headings: List of tuples that has information regarding the headings  
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
    """Tkinter Treeview Wrapper for interacting with Weapons.

    Impliments ability to choose which elements of Treeview are visible,
    and redraw the treeview with new values.

    Attributes:
        treeview: Tkinter Treeview Object refrence.
        frame: Tkinter Root frame object refrence.
        hidden_items: List of row item_IDs that are hidden from the Treeview.
        COLUMN_DICT: Dict default parameters for creating columns.
            {
            sort_type: String of data_type column is being sorted by. Currently Valid - ['int', 'str', 'date', 'float'].
            text: String text value for Header display.
            anchor: String that indicates the text Justification 'c'.
            width: Int width of column in Screen Units.
            minwidth: Int Minimum Width of Column in Screen Units when dragged together in the treeview.
            stretch: Bool If column elements should take up all the space in its width, or only be as large as necessary.
            }
    """
       
    treeview = None
    frame = None
    hidden_items = []
    COLUMN_DICT = {'sort_type' : 'str' , 'text' : 'Default', 'anchor': 'c' , 'width' : 80 , 'minwidth' : 60 , 'stretch' : True}
    def __init__(self, root : Tk, cols : dict, bg : str = "grey", height : int = 400, relief = FLAT, color_tags : dict = None):
        """Initilize our Treeview wrapper, and treeview object

        Generate a table with the column parameters in the Cols list, and create it inside the root TK object
        Create color tags and assign default styling parameters.
        
        Args:
            root: Base Tkinter Containers for GUI elements.
                Can be Frame, or Application object.
            cols : dictionary with name of column and parameters for creating it.
                Key - column_name : Value - Kwargs that are an instance of column_dict.
            bg : color that will be assigned to the background.
            height: int height of the local tableFrame Object in Screen Units
            relief : Bool that indicates if elements will be connected smoothly when gaps are between the elements.
            color_dict : dict that details the creation of tags for Colors
                Key - tag_name : Value - Hex Code for Color
        """
        #Create Frame for holding Table Data.
        tableFrame = Frame(root, bg = bg, relief = relief, height = height)
        tableFrame.grid(column=0, row=0)
        self.frame = tableFrame
         
        # Creates table with column populated form 'cols'.
        self.treeview = MyTreeview(tableFrame, columns=list(cols.keys()), height= 32, selectmode=BROWSE)
        self.treeview.grid(row = 0, rowspan= 5, column = 0, columnspan= 7, sticky=NSEW)
        # Creates scrollbar, and assigns its control functions.
        ver_scroll = Scrollbar(tableFrame, orient="vertical", command=self.treeview.yview, width= 30)
        ver_scroll.grid (row = 0, rowspan = 5, column = 8, sticky= NSEW )
        self.treeview.configure(yscrollcommand=ver_scroll.set)
        # Generates tags to assign colors to rows.
        for name,color in color_tags.items():
            self.treeview.tag_configure(name, background=color)

        self.treeview.heading("#0", sort_type='str', text="Default Column")
        self.treeview.column("#0", width=0, minwidth= 0, stretch=False)
        # Create table from cols dictionary instrutions
        for ele in cols.items():
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

    def draw_table(self, weapon_list : list[Weapon]):
        """Populate table with weapons taking up each row the first time.
        
        Assign row color based on weapon_cp, and save the information regarding its place in the table with
        item_identifier and item_index.
        """
        for ele in weapon_list:
            # For each weapon, get the dict of valuess, and set the color equal to that of its CP.
            # Use KWARGS to future proof any additional attributes we would like to apply to this item.
            dict = ele.clean_dict()
            row_KWARGS = {'values' : list(dict.values()),'tags' : 'white'}
            match ele.cp:
                case 1:
                    row_KWARGS['tags'] = 'green'
                case 2:
                    row_KWARGS['tags'] = 'yellow'
                case 3:
                    row_KWARGS['tags'] = 'orange'

            # Add the weapon as a row to the table, and store that weapons treeview item information.
            item = self.treeview.insert('', END, text=ele.name, **row_KWARGS)
            ele.item_identifier = item
            ele.item_index = self.treeview.index(item)

    def redraw_table(self, weapon_list : list[Weapon], filtered_list : list[Weapon] = []):
        """Update all values of weapons in the treeview, and show only weapons in filtered_list
        
        Sorts by the previous sort type if it is available. Currently requires sending in a list of weapons as filtered_list
        """
        for ele in weapon_list:
            # Update the display of all weapon values
            dict = ele.clean_dict()
            self.treeview.item(ele.item_identifier,values=list(dict.values()))
            # If the weapon is not inside the filtered_list. Hide it from the treeview
            if filtered_list is not None:
                if ele not in filtered_list:
                    self.hide_item(ele.item_identifier)
                else: 
                    self.unhide_item(ele.item_identifier)
        # Must sort by previous sort parameters to keep order of table.
        self.treeview.last_sort()    

    def hide_item(self, item_id):
        """Hide an item_id from the treeview if it is currently visible.
        
        Save all items_ids in the hidden_items list.
        Detach the Item from the treeview. it still exists but is not visible.  
        Documnation : https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.detach        
        """
        all_items = self.treeview.get_children()
        if item_id in all_items:
            self.treeview.detach(item_id)
            self.hidden_items.append(item_id)
            print("Hiding Item : ", item_id)

    def unhide_item(self, item_id):
        """Unhide an item_id from the treeview if it is currently not visible.
        
        Reattach item to the end of the treeview. Reattach is an allias for Treeview.move(item, parent, index)
        Documenation : https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.reattach
        """
        all_items = self.treeview.get_children()
        if item_id in self.hidden_items:
            self.treeview.reattach(item_id, '', len(all_items))
            self.hidden_items.remove(item_id)

    def delete_table(self):
        """Currently un-used method that will all items in the table.
        
        Should be avoided using. Will require re-running self.draw_table with a weapon_list
        to continue functionality.
        """
        self.treeview.delete(self.treeview.get_children())

class FilterMenu():
    """Container for multiple Tkinter Objects that make filters for sorting a Table object

    Generate filter Listboxes that contain all Tags, Categorys, CP Cost. When clicked / updated trigger callback function assigned at __init__

    Attributes:
        _callback: A callback function that is triggered when you click an element in the listbox.
            This will update the _filters dict, and save the information of all selected filters.
        _filters: Dict that contains arrays of all list elements.
        _tags: Dict detailing the default values of the Tags Filter Listbox, and its values.
        _categorys: Dict detailing the default values of the Categorys Filter Listbox, and its values.
        _names: Dict detailing the default values of the names Searchbox.
        _cps: Dict detailing the default values of the CPs Filter Listbox, and its values.
    """       
    _callback = None
    _filters = {
        "tags" : [],
        "names" : [],
        "categorys" : [],
        "cps" : []
    }
    _tags = {
        "name" : "Tags",
        "width" : 18, 
        "values" : []
        }
    _categorys = {
        "name" : "Categorys",
        "width" : 15, 
        "values" : []
        }     
    _names = {
        "name" : "Names",
        "width" : 15, 
        "values" : []
        }
    _cps = {
        "name" : "CPs",
        "width" : 7, 
        "values" : []
        }

    def __init__(self, root : Tk, weapons_list : list[Weapon], filter_callback):
        """Create Tkinter elements based on inputted weapon_list, and trigger callback function when selections are made.

        Update and maintain a list of _filters when clicked based on the weapons "Tags", "Categorys", "Names", and "CPs".
        Generates Tags, Categorys, and CPs as a list_box that is selectable in the UI root frame
        
        Args:
            root: Base Tkinter Containers for GUI elements.
                Can be Frame, or Application object.
            weapons_list: List of Weapon objects that will create all the filter parameters available to the user.
            filter_callback: Callback function taht is assigned to elements in the UI when left-clicked.
        """
        filter_frame = Frame(root, bg='yellow', width=150, height=300, padx=3, pady=3, relief= FLAT)
        filter_frame.grid(row=0, column=0, sticky=NSEW)
        my_filters = Label(filter_frame, text= "Filters", justify = CENTER,  width=6, height = 1, font=("Arial", 25) )
        my_filters.grid(column=0, columnspan = 3, row=0,  sticky=EW)
        self._callback = filter_callback

        # Initilize values for all weapons. Ignoring Repeating Items.
        for ele in weapons_list:
            for tag in ele.tags:
                if tag not in self._tags['values']:
                    self._tags['values'].append(tag)
            if ele.category not in self._categorys['values']:
                self._categorys['values'].append(ele.category)
            if ele.name not in self._names['values']:
                self._names['values'].append(ele.name)
            if ele.cp not in self._cps['values']:
                self._cps['values'].append(ele.cp)
        self._tags['values'].sort()
        self._names['values'].sort()

        # Create a listbox for tags, categorys, and cps.
        for count, ele in enumerate((self._tags, self._categorys, self._cps)):
            # Create label; and listbox with height equal to the length of the values array in this element. 
            label = Label(filter_frame, text=ele['name'], width=ele['width'])
            label.grid(column=count, row=3, sticky=NSEW, pady = (25,0))
            listbox = Listbox(filter_frame, selectmode="multiple", exportselection=0, height=len(ele['values']), width=ele['width'], activestyle='none')
            listbox.config( justify=CENTER, borderwidth=3)
            
            # Add entry to listbox with that entrys name. (Blunt, Wieldy, Ranged 15/25, ...)
            for entry in ele['values']:
                listbox.insert(END, entry)

            # Assign clicking to trigger _update_filters method
            func = getattr(self, "_update_filters")
            listbox.bind("<<ListboxSelect>>", partial(func, ele))
            listbox.grid(column=count, row=4, sticky=NSEW)
        
    def _update_filters(self, element, event : Event):
        """Triggers before our callback function, and gathers the information regarding the change in filter, and keeps data in self._filters."""
        listbox = event.widget
        # Get list of all selected items in listbox.
        selected_items = [listbox.get(sel) for sel in listbox.curselection()]
        # Set dict value of the listbox's name (Tags, Categorys, CPs) equal to the new list.
        self._filters[str(element['name'].lower())] = selected_items
        # Trigger out app_controller callback function.
        self._callback()

    def get_filter(self):
        """Getter for self._filters"""
        return self._filters 
    