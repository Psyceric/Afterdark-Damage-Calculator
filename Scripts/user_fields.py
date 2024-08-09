from tkinter import *

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
            {"name" : "level", "default_value" : 1},
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

            # Create Display Lable with Stat name
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