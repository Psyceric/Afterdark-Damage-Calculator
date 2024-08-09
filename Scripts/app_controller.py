from tkinter import Tk
import pandas as pd
import os
from my_tkinter import Table, MyTreeview
from weapon import Weapon
from user_fields import UserFields


weapon_list = []

def generate_weapon_list(file : str):
        """From a CSV File or a file path, populate the weapons_list"""
        
        local_path = os.getcwd()
        parent_directory = os.path.abspath(os.path.join(local_path,os.pardir))
        absolute_directory = os.path.abspath(os.path.join(parent_directory,file))
        csv = pd.read_csv(absolute_directory).to_dict(orient="records")        
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
 
def update_weapon_list(self, userInfo):
    for ele in self.weapon_list:
        ele.update_weapon(userInfo)

fileName = './resources/Afterdark 1.02 Weapon Values.csv'
generate_weapon_list(fileName)
cols = weapon_list[0].to_dict()
print(cols.keys())

#Initilize Application
root = Tk()
root.title("Afterdark™ Damage Per Turn Calculator")
root.resizable(width=1, height=1)

my_user_fields = UserFields(root = root)                              # - > Add more Init parameters
my_table = Table(root=root, cols=cols)
my_table.initiate_columns(cols=cols)
my_table.draw_table(weapon_list)

root.mainloop()