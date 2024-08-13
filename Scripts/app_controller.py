from tkinter import Tk
from tkinter import * 
import pandas as pd
import os
from my_tkinter import Table, FilterMenu
from weapon import Weapon
from user_fields import UserFields


weapon_list = []

def generate_weapon_list(file : str):
    """From a CSV File or a file path, populate the weapons_list"""
    
    local_path = os.getcwd()
    parent_directory = os.path.abspath(os.path.join(local_path,os.pardir))
    absolute_directory = os.path.abspath(os.path.join(parent_directory,file))
    csv = pd.read_csv(absolute_directory, keep_default_na=False).to_dict(orient="records")        
    for weapon_dict in csv:
        curWep = Weapon(
        name = weapon_dict['name'],
        default_dice = weapon_dict['default_dice'],
        cp = weapon_dict['cp'],
        tags = weapon_dict['tags'].split(','),
        category = weapon_dict['category'],
        magazine_size = weapon_dict['magazine_size'],
        )
        curWep.update_weapon()
        weapon_list.append(curWep)

def update_table(filtered_list = None):
    user_entry = my_user_fields.get_userEntrys()
    print('redraw table with stats : {0}'.format(user_entry))
    for ele in weapon_list:
         ele.update_weapon(user_entry['level'], user_entry['damage_modifier'], user_entry['to_hit_bonus'], user_entry['number_of_attacks'])
    my_table.redraw_table(weapon_list, filtered_list)

def filter_update():
    filter = my_filter_menu.get_filter()
    sucess = []
    for weapon in weapon_list:
        if weapon.has_tags(filter['tags']) or not filter['tags']:
            if weapon.category in filter['categorys'] or not filter['categorys']:
                if weapon.cp in filter['cps'] or not filter['cps']:
                    sucess.append(weapon)
    update_table(sucess)
    #print("filter Updating... \n", sucess)

def table_callback():
    pass

fileName = './resources/Afterdark 1.02 Weapon Values.csv'
generate_weapon_list(fileName)
cols = weapon_list[0].to_dict() # Might be cursed

#Initilize Application
root = Tk()
root.title("Afterdark™ Damage Per Turn Calculator")
root.resizable(width=1, height=1)

top_frame = Frame(root, bg='cyan', width=450, height=50, pady=3)
center = Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)
btm_frame = Frame(root, bg='white', width=450, height=45, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=2, sticky="ew")

# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_mid = Frame(center, bg='yellow', width=250, height=190, padx=3, pady=3)
ctr_right = Frame(center, bg='green', width=150, height=190, padx=3, pady=3)

ctr_mid.grid(row=0, column=0, sticky=NSEW)
ctr_right.grid(row=0, column=1, sticky=NSEW)

my_user_fields = UserFields(top_frame, update_table)                              # - > Add more Init parameters
my_table = Table(root=ctr_mid, cols=cols,callback=table_callback)
my_table.initiate_columns(cols=cols)
my_table.draw_table(weapon_list)
my_filter_menu = FilterMenu(ctr_right, weapon_list, filter_update)




root.mainloop()