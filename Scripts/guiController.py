from tkinter import *
from main import *

statLabels = ["Weapon Level","To Hit Bonus","Damage Modifier","Number of Attacks"]
defaultValues = [1,0,0,0]

def isDigits(input):
    if input.isdigit() or input == "":
        return True
    else:
        return False
    
root = Tk()
root.title("Afterdark™ Damage Per Turn Calculator")
root.geometry('550x200')
reg = root.register(isDigits)

frame = Frame(root, bg = "white", relief=FLAT)
frame.pack(side=TOP, anchor=NW, expand=True)

statEntrys = []
for i in range(len(statLabels)):
    label = Label(frame, text=statLabels[i], width=15, bg="white")
    entry = Entry(frame, justify=CENTER, width=15, bg="white", bd=3)
    label.grid(row=0, column=i, sticky=EW, padx=1)
    entry.grid(row=1, column=i, sticky=EW, padx=10, pady=2)
    entry.config(validate="key",validatecommand=(reg,'%P'))
    entry.insert(0,defaultValues[i])
    statEntrys.append(entry)
def outputTest():
    if statEntrys:
        entries = []
        for i in range(len(statEntrys)):
            entry = statEntrys[i].get()
            if entry:
                entries.append(entry)
        print(entries)

calcBtn = Button(frame, text="Calculate", width=15, bg="white",command=outputTest)
calcBtn.grid(row=0, column= 5, rowspan=2, sticky=NSEW, padx=(25,0))


# toHitLable = Label(root, text = "Additonal To Hit")
# toHitLable.grid(column=2,row=0)

# attackNumLable = Label(root, text = "Number Of Attacks")
# attackNumLable.grid(column=3,row=0)

# damageModLabel = Label(root, text = "Damage Modifier")
# damageModLabel.grid(column=4,row=0)

# root.grid_columnconfigure(5,minsize=100)

# damageModLabel = Button(root, text = "Calculate", fg="black")
# damageModLabel.grid(column=9,row=0)

root.mainloop()