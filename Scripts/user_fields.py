from tkinter import *
from functools import partial
import re

class UserFields(object):
    """Handles creating / updating / and gathering information from User Input Fields"""
    user_entrys = []
      
    def __init__(self, root : Tk, update_callback):
        """Generates main body of userFields, creating in root frame from Tkinter"""
        
        int_register = root.register(self.validate_int)
        level_register = root.register(self.validate_level)

        # Default values for user_entry
        USER_ENTRY_DEFAULT = {
            "id" : "default",
            "name" : "Default" ,
            "default_value" : 0,
            "current_value" : 0,
            "entry_object" : None,
            "colomn_refrence" : None,
            "entry_register" : int_register}
        
        #Array of user_entry's to be created. Parameters must be in USER_ENTRY_DEFAULT dictionary
        user_entry_parameters = [
            {"id" : "level", "name" : "Level", "default_value" : 1, "entry_register" : level_register},
            {"id" : "to_hit_bonus" , "name" : "To Hit Bonus"},
            {"id" : "damage_modifier" , "name" : "Damage Modifier"},
            {"id" : "number_of_attacks", "name" : "Number of Attacks"}
        ]

        #Dynamically creates list of user_entry
        self.user_entrys = self.generate_userEntrys(USER_ENTRY_DEFAULT,user_entry_parameters)
        
        for count, ele in enumerate(self.user_entrys):
        # Dynamically create user Entry fields, assigning values in userEntries array

            # Create Display Lable with Stat name
            label = Label(root, text=ele['name'],width=15, bg="white")
            label.grid(row=0, column=count,sticky=EW, padx=1)

            # Create userInfo entry object
            entry = Entry(root, justify=CENTER,width=15, bg="white", bd=3)
            entry.grid(row=1, column=count,sticky=EW, padx=10, pady=2)

            # Registers and assigns text validation function
            
            entry.config(validate="key",validatecommand=(ele['entry_register'],'%P'))

            #Updates user_entry information about its entryBox
            ele['entry_object'] = entry
            ele['current_value'] = entry.get()
            ele['colomn_refrence'] = count
            
            # Instantiate the Entry Box into the application
            entry.insert(0,ele['default_value'])

        #Create buttonm, and assign it to trigger update_userInfo when clicked
        #_Callback = function(update_callback, self.get_userEntrys())
        calcBtn = Button(root, text="Calculate", width=15, bg="white",command=update_callback)
        calcBtn.grid(row=0, column= len(self.user_entrys)+1, rowspan=2, sticky=NSEW, padx=(25,0))

        # Generate_filters method (self, list[str])
        # for each in list -> Create button 

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
            returnValues.append((ele['id'],int(ele['entry_object'].get())))

        # TODO : Trigger updateTable funtion (returnValues)
        print(returnValues)
        return dict(returnValues)

    def validate_int(self, input):
        """Used to validate text input in TTK.Entry"""
        print(input)
        return (input.isdigit() or input == "") 
    
    def validate_level(self, input):
        print("Level : ", input)
        pattern = r'^[1-9][0-9]*'
        result = re.match(pattern,input)
        return result is not None or input == ""
     #
    ### End of userInfo Class