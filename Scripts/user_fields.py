from tkinter import *
import re

class UserFields(object):
    """
    The UserFields object creates and maintains multiple Tkinter Entry Objects.

    Dynamically generates a group of Tkinter Labels and Entrys. Has the ability collect and return the data of all Entry objects when 'get_entrys()' property is accessed
    The Calculate button that triggers a callback function to our app_controller script.

    Attributes:
        _user_entrys : a list of dictionaries detailing default values, object refrences, and how to generate GUI elements.
        _root : A Tkinter Container for GUI Elements
        _int_validation : string used by Tkinter to refrence the 'validate_int' callback method
        _level_validation : string used by Tkinter to refrence the 'validation_level' callback method
        _USER_ENTRY_DEFAULT : A dict defining default a userEntry group:
            {
            name : str, default "Default"
                Display name in GUI and keys in property getter 'self.get_entrys()'.
            default_value : int, default 0
                Value that will populate the Entry when created, and if calulate button is clicked with an empty field
            entry_object : TK.Entry, Default None
                Refrence object to the Tkinter.Entry GUI Object
            entry_text_validator : string variable name of TK registered Callback Method - "_int_validation" or "_level_validation"
                Used to assign text validation callback method in entry_object
            }
    """

    _user_entrys : dict = []
    _root : Tk = None
    _int_validation : str = None
    _level_validation : str = None
    _USER_ENTRY_DEFAULT = {
    "name" : "Default",
    "default_value" : 0,
    "entry_object" : None,
    "entry_text_validator" : "int_validation"}
    
    def __init__(self, root : Tk, user_entry_parameters : list[dict], calculate_callback ):
        """Initilize a group of GUI elements with user_entry_parameters, and a Calcualte button

        user_entry_parameters must be a Composite of USER_ENTRY_PARAMETER constant. 
        Creates elements left to right in order entered in user_entry_parameters.
        
        Args:
            root: Base Tkinter Containers for GUI elements.
                Can be Frame, or Application object.
            user_entry_parameters : list of dictionaries that are composites of USER_ENTRY_FIELDS. 
                Each dictionary will generate a unique Tkinter Label & Entry GUI Object.
            calculate_callback : Method to be assigned to the Calculate Tkinter button.
                Trigger callback function when button is clicked.
        """
        self._root = root
        # Register validation callback methods with our root Tkinter Container 
        self.int_validation = root.register(self._validate_int)
        self.level_validation = root.register(self._validate_level)

        for count, ele in enumerate(user_entry_parameters):
            # Updates default values, validates new dictionary is inhereted from _USER_ENTRY_DEFAULT
            entry_data = dict(self.USER_ENTRY_DEFAULT)
            entry_data.update(ele)
            assert len(entry_data) == len(self._USER_ENTRY_DEFAULT), "Invalid Paramters when generating UserFields at index : {0}, element : {1}".format(count, ele)

            # Instaniate Label and Entry in the next available row, and adds its object to dict
            label = Label(root, text = entry_data['name'], width = 15, bg = "white")
            label.grid(row=0, column = count, sticky = EW, padx = 1)
            entry = Entry(root, justify=CENTER, width = 15, bg="white", bd = 3)
            entry.grid(row=1, column=count, sticky=EW, padx=10, pady=2)
            entry.insert(0,entry_data['default_value'])
            entry_data['entry_object'] = entry

            # Assigns Validaiton callback function to Tkinter entry object
            entry.config(validate = "key", validatecommand = (getattr(self, entry_data['entry_text_validator']), '%P'))
            self._user_entrys.append(entry_data)

        # Create Tkinter button, and assign it with Calculate_callback method.
        calcBtn = Button(root, text = "Calculate", width=15, bg = "white", command = calculate_callback)
        calcBtn.grid(row = 0, column = len(self._user_entrys) + 1, rowspan = 2, sticky = NSEW, padx = (25,0))

    def get_entrys(self):
        """
        Returns dict of _user_entrys values. If empty sets to default values.
        
        Collects all entry values of _user_entrys, if the value has a empty text field, we populate it with the _user_entry's default value.
        and than return the values including that default value.
        """
        entrys_values = {}

        
        for user_entry in self._user_entrys:
            # Get all values from Tkitner Entry objects
            value = user_entry['entry_object'].get()
            if not value:
                # If the Entry Field is empty, set it to default, and populate field with default value
                value = user_entry['default_value']
                user_entry['entry_object'].insert(0, value)

            # Adds entry to dictionary with user_entry name as Key, and Entry Value as value.
            entrys_values.update({user_entry['name']: int(value)})
        print("Current user_entry values are :", entrys_values)
        return entrys_values
    
    @property
    def USER_ENTRY_DEFAULT(self):
        """Getter for Constant dict : _USER_ENTRY_DEFAULT"""
        return self._USER_ENTRY_DEFAULT
    
    def _validate_int(self, input):
        """Callback function that validates text is an integer
        
        This method is registered with Tkinter's root container,
        and is used inhereted USER_ENTRY_DEFAULT dict's under the key 'entry_text_validator'
        The string for this will be 'validate_int'

        Args:
            input : string that is to be validated by this method
        
        Returns:
            If input string is empty or is a made of integers
        """
        return (input.isdigit() or input == "") 
    
    def _validate_level(self, input):
        """Callback function that validates text is a supported Level integer
        
        This method is registered with Tkinter's root container,
        and is used inhereted USER_ENTRY_DEFAULT dict's under the key 'entry_text_validator'
        The string for this will be 'validate_level'

        Args:
            input : string that is to be validated by this method
        
        Returns:
            If input string empty, or an interger in range (1,+inf)
        """
        pattern = r'^[1-9][0-9]*$'
        result = re.match(pattern,input)
        return result is not None or input == ""