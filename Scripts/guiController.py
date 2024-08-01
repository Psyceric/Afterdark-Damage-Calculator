from tkinter import *
from main import *
#(Variable name, Default Value)
userVariables = [
    ("Weapon Level" , 1),
    ("To Hit Bonus" , 0), 
    ("Damage Modifier" , 0),
    ("Number of Attacks" , 0)
]
userVarEntrys = []

#Initilize Application, and frame contrainer
root = Tk()
root.title("Afterdark™ Damage Per Turn Calculator")
frame = Frame(root, bg = "white", relief=FLAT)
frame.pack(side=TOP, anchor=NW, expand=True)

#Callback function for Digits
def is_digits(input):
    if input.isdigit() or input == "":
        return True
    else:
        return False
isDigitRegister = root.register(is_digits)

#Creates Entry Fields for User Variables
for i in range(len(userVariables)):

    #Create Labels and Entries in rows
    label = Label(frame, text=userVariables[i][0], width=15, bg="white")
    entry = Entry(frame, justify=CENTER, width=15, bg="white", bd=3)
    label.grid(row=0, column=i, sticky=EW, padx=1)
    entry.grid(row=1, column=i, sticky=EW, padx=10, pady=2)


    #Assign Callback, limit entry to digits only
    entry.config(validate="key",validatecommand=(isDigitRegister,'%P'))
    entry.insert(0,userVariables[i][1])


    #Add Entry to list of Entries
    userVarEntrys.append(entry)

#Prints User Variables
def get_user_variables():
    if userVarEntrys:
        entries = []
        for i in range(len(userVarEntrys)):
            entry = userVarEntrys[i].get()
            if entry:
                entries.append(entry)
        print(entries)

#Create Calculate Button and Connecty to get_user_variables method
calcBtn = Button(frame, text="Calculate", width=15, bg="white",command=get_user_variables)
calcBtn.grid(row=0, column= len(userVariables)+1, rowspan=2, sticky=NSEW, padx=(25,0))

#Loops
root.mainloop()