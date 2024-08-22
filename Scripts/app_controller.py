from tkinter import Tk
from tkinter import * 
import pandas as pd
import os
from .my_tkinter import Table, FilterMenu
from .weapon import Weapon
from .user_fields import UserFields

class AppController():
    """
    Creates and maintains applicaiton using Tkinter, creating multiple frames to contain user_fields, a table, and filter_menu

    Contains multiple callback functions that are assigned to elements inside other classes. (ex. userField calculate button, table header click, and filter_menu filter selection)

    Attributes:
        weapon_list: list of Weapon Objects that will be displaye inside our table object
    """

    weapon_list = []

    def generate_weapon_list(self, file : str):
        """From a CSV File or a file path, populate the weapons_list"""
        
        local_path = os.getcwd()
        absolute_directory = os.path.abspath(os.path.join(local_path,file))
        csv = pd.read_csv(absolute_directory, keep_default_na=False).to_dict(orient="records")        
        for weapon_dict in csv:
            weapon_dict['tags'] = weapon_dict['tags'].split(',')
            curWep = Weapon(weapon_dict = weapon_dict)
            self.weapon_list.append(curWep)

    def update_table(self, filtered_list = None):
        """Iterate through all elements in the table, and update the weapon. Than redraw table"""
        user_entry = self.my_user_fields.get_entrys()
        print('redraw table with stats : {0}'.format(user_entry))
        for ele in self.weapon_list:
            ele.update_weapon(user_entry['Level'], user_entry['Damage Modifier'], user_entry['To Hit Bonus'], user_entry['Number of Attacks'])
        self.my_table.redraw_table(self.weapon_list, filtered_list)

    def filter_update(self):
        """Callback function that is triggered when a new filter is selected in filter_menu"""
        filter = self.my_filter_menu.get_filter()
        sucess = []
        for weapon in self.weapon_list:
            if weapon.has_tags(filter['tags']) or not filter['tags']:
                if weapon.category in filter['categorys'] or not filter['categorys']:
                    if weapon.cp in filter['cps'] or not filter['cps']:
                        sucess.append(weapon)
        self.update_table(sucess)


    def main(self):
        fileName = './resources/Afterdark 1.02 Weapon Values.csv'
        self.generate_weapon_list(fileName)
        keys = self.weapon_list[0].to_dict().keys()
        cols = []
        for key in keys:
            param = {}
            match key: 
                case 'name':
                    param = {'text' : 'Weapon Name', 'width' : 200, 'minwidth' : 200}
                case 'default_dice':
                    param = {'text' : 'Default Roll', 'width' : 90, 'minwidth' : 90}
                case 'cp': 
                    param = {'text' : 'CP', 'width' : 90, 'minwidth' : 30}
                case 'tags':
                    param = {'text' : 'Weapon Tags', 'width' : 300, 'minwidth' : 300}
                case 'magazine_size':
                    param = {'text' : 'Mag Size', 'width' : 90, 'minwidth' : 90}
                case 'category':
                    param = {'text' : 'Weapon Type', 'width' : 120, 'minwidth' : 120}
                case 'level':
                    param = {'text' : 'Level'}
                case 'damage_dice':
                    param = {'text' : 'Damage dice'}
                case 'situational_dice':
                    param = {'text' : 'Tag Damage'}
                case 'damage_modifier':
                    param = {'text' : 'Damage mod'}
                case 'damage_roll' : 
                    param = {'text' : 'Damage Roll', 'width' : 90, 'minwidth' : 90}
                case 'to_hit_bonus':
                    param = {'text' : 'To Hit', 'width' : 50, 'minwidth' : 50}
                case 'attack_damage':
                    param = {'text' : "Dmg Per Attack", 'sort_type' : 'float', 'width' : 120, 'minwidth' : 80}
                case 'average_attacks':
                    param = {'text' : "Attacks", 'sort_type' : 'float', 'width' : 80, 'minwidth' : 80}
                case 'average_damage_per_turn':
                    param = {'text' : 'Dmg Per Turn', 'sort_type' : 'float', 'width' : 80, 'minwidth' : 80}
            cols.append((key, param))
        cols = dict(cols)

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

        field_parameters = [
            {"name" : "Level", "default_value" : 1, "entry_text_validator" : "level_validation"},
            {"name" : "To Hit Bonus"},
            {"name" : "Damage Modifier"},
            {"name" : "Number of Attacks"}]

        self.my_user_fields = UserFields(top_frame, field_parameters, self.update_table)
        self.color_tags = {'green' : '#B5CFB7', 'yellow' : '#FAEDCE', 'orange' : "#F8C794", 'red' : '#C7B7A3'}
        self.my_table = Table(root = ctr_mid, cols = cols, color_tags=self.color_tags)
        self.my_table.draw_table(self.weapon_list)
        self.my_filter_menu = FilterMenu(ctr_right, self.weapon_list, self.filter_update)

        root.mainloop()

if __name__ == "__main__":
    myapp = AppController()
    myapp.main()