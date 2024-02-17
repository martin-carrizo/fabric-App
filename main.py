from kivymd.app import MDApp
from kivymd.uix.card import (MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox)
from kivymd.uix.button import (MDIconButton, MDRectangleFlatButton)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import (OneLineListItem, OneLineAvatarIconListItem)

from kivy.clock import Clock
from kivy.metrics import dp
from uuid import uuid4

import sqlite3
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (Table, TableStyle)
#TODO reorganizar el codigo para darle mas coherencia
#TODO revisar si puedo bloquear los botones cuando se desliza de costado
#TODO ponerle el _ donde haga falta


class ListGridLayout(MDBoxLayout):
    """This class provides a flexible way to build lists with the following features:
        - Optional infinite scrolling
        - Maximum and minimum number of elements
        - Database access for data retrieval

    Attributes:
        max_fabric (int): Maximum number of elements allowed (default: 4).
        min_fabric (int): Minimum number of elements allowed (default: 0).
        db_path (str): Path to the database file (default: 'fabric_db.db').
        index_db_quantity_buttons (dict): Mapping from keyword to database field index.
        reverse (bool): Flag indicating whether to sort in reverse order (default: False).
    """
    def __init__(self):
        self.plus = None 
        self.max_fabric = 4
        self.min_fabric = 0
        self.db_path = 'fabric_db.db'
        self.index_db_quantity_buttons = {
            'fname': 7,
            'no_stock': 6,
            'Fab_count': 5,
            'r_large': 4,
            'r_small': 3,
            'large': 2,
            'medium': 1,
            'small': 0
            }
        self.reverse = False
              

        super(ListGridLayout, self).__init__() #call grid layout constructor
        Clock.schedule_once(lambda dt: self.load_data(), 0) #load data on app launch
    
    
    def options_menu(self, button):
        """main option menu"""
        menu_list = [
        {
            "viewclass": "OneLineListItem",
            "text": 'Settings',
            "on_release": self.set_max_quantity_dialog 
        },
        {   
            "viewclass": "OneLineListItem",
            "text": 'Export',
            "on_release": self.export_to_pdf_dialog 
        },
        {   
            "viewclass": "OneLineListItem",
            "text": 'Reset list',
            "on_release": self.delete_dialog 
        }
        ]
        self.menu = MDDropdownMenu( caller = button, items = menu_list, width_mult=3,)
        self.menu.open()
    
    def error_message_popup(self, error_text):
        """popup to show error message to user"""
        error_dialog= MDDialog(text=error_text, buttons=[MDRectangleFlatButton( text='X', on_release=lambda *args: error_dialog.dismiss())])
        error_dialog.open()
        
       
    def export_to_pdf_dialog(self):
        """dialog to export the current list to pdf """
        self.menu.dismiss()
        export_message = 'export to PDF?'
        self.export_to_pdf_dialog_screen = MDDialog(
            text=export_message,
            buttons=[
                MDRectangleFlatButton(
                    text='Yes, export',
                    on_release=lambda *args: (self.export_to_pdf(), self.export_to_pdf_dialog_screen.dismiss())
                ),
                MDRectangleFlatButton(
                    text='Cancel',
                    on_release=lambda *args: self.export_to_pdf_dialog_screen.dismiss()
                )
            ]
        )
        self.export_to_pdf_dialog_screen.open()
    
    
    
    def set_max_quantity_dialog(self):
        """dialog to choose the max number of tablecloth and fabrics"""
        self.menu.dismiss()
        items = [2, 4, 6, 8, 10] #list of options to choose from
        
        options = [
            OneLineAvatarIconListItem(
                text=str(option),
                divider=None,
                on_release=lambda *args, option=option: on_option_selected(option)
            ) for option in items
        ]

        buttons = [
            MDRectangleFlatButton(
                text='Default',
                on_release=lambda *args: on_option_selected(4)
            ),
            MDRectangleFlatButton(
                text='Exit',
                on_release=lambda *args: self.set_max_quantity_screen.dismiss()
            )
        ]

        self.set_max_quantity_screen = MDDialog(
            title='Select max fabrics quantity',
            type="confirmation",
            items=options,
            buttons=buttons
        )

        self.set_max_quantity_screen.open()
        
        def on_option_selected(value):
            """handle the save to max_fabric and check the color of the numbers"""
            setattr(self, 'max_fabric', value)
            self.save_max_fabric(int(value))
            
            instance = self.ids.box_grid.children[0].children[0].children[0].children #path to buttons
            for row in range(6):
                
                self.color_check(instance[row])

    
    def delete_dialog(self):
        """dialog to remove all rows from the grid and database"""
        self.menu.dismiss()
        delete_message = 'are you sure you want to remove all fabrics? this action cant be undone'
        
        self.delete_dialog_screen = MDDialog(
            text=delete_message, 
            buttons=[
                MDRectangleFlatButton(
                    text='yes, remove',
                    on_release=lambda *args: (self.delete_all_fabrics(), self.delete_dialog_screen.dismiss())
                    ),
                MDRectangleFlatButton(
                    text='cancel',
                    on_release=lambda *args: self.delete_dialog_screen.dismiss() 
                    )])
        
        self.delete_dialog_screen.open()

    #delete all fabrics from app and db
    def delete_all_fabrics(self):
        """delete all fabrics from app screen and db"""
        self.ids.box_grid.clear_widgets() #remove all widgets from screen
        try:
                
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM fabrics')
                conn.commit()
                
        except sqlite3.Error as e:
             
                text= f"Error removing items from database:, {e}"
                self.error_message_popup(text)
            
        Clock.schedule_once(lambda dt: self.ids.box_grid.do_layout(), 0) #refresh the widgets
    
      
    
    def sort_fabric_by(self, text):
        """Sorts fabrics based on user's choice and direction"""
        self.reverse = True if self.reverse == False else False #toggle the sort direction
        
        if text in self.index_db_quantity_buttons: #check if the text exist in the index
            self.sort_elements(self.index_db_quantity_buttons[text])
         
   
    def sort_elements(self, index):
        """order the data in the grid"""
        index = 6 if index == 7 else index #hard-fix to avoid out-of-range. <----this one will be removed in future versions 
        sorted_cards = sorted(
            (card for card in self.ids.box_grid.children if isinstance(card, MDCardSwipe)),
            key=lambda card: card.children[0].children[0].children[index].text, reverse= True if self.reverse == True else False
        ) 
        
        self.ids.box_grid.clear_widgets() # remove the widgets from the box_grid
        for sorted_card in sorted_cards: # add sorted widgets to box_grid
            self.ids.box_grid.add_widget(sorted_card)
            
        Clock.schedule_once(lambda dt: self.ids.box_grid.do_layout(), 0) # refresh the screen
            
            
            
            
    
    def self_plus_check(self, state):
        """change the true/false in self.plus"""
        self.plus = True if state == '+' else False
    
    # manage the plus/minus button
    def quantity(self, btn_id):
        """changes the number(and number's color) displayed when the user adds or removes and save it in the db"""
        if self.plus == True and int(btn_id.text) < self.max_fabric:
            btn_id.text = str((int(btn_id.text) + 1))
            self.color_check(btn_id)
        elif self.plus == False and  int(btn_id.text) > 0:
            btn_id.text = str((int(btn_id.text) - 1))
            self.color_check(btn_id)
        id_to_change = btn_id.parent.id
        self.update_db_data(self.get_btn_id(btn_id.id), id_to_change, btn_id.text) #save the new data
       

    
    def color_check(self, button):
        """check the number colors and adjust it to the range between min and max""" 
        text_colors_mapping = {
            'green' : (0, 0.871, 0, 1), 
            'yellow':(0.851, 0.859, 0), 
            'red': (0.8, 0, 0, 1)
            } 
        
        if int(button.text) >= self.max_fabric:
            button.text_color = text_colors_mapping['green']
        elif self.min_fabric < int(button.text) < self.max_fabric:
            button.text_color = text_colors_mapping['yellow']
        else:
            button.text_color = text_colors_mapping['red']
          
            
    def add_new_fabric_row(self, is_new):
        """create a new row to the grid.
            - is_new: check if the row is being charged from the user or the load_data method to avoid infinite loop
        """ 
        new_grid = MDGridLayout(cols= 7, rows= 1)
        new_grid.id = str(uuid4()) #generate a random 16-digits unique code
        name_button = OneLineListItem( #create the name button
            text='name',
            id = '7',
            size_hint_x=None,
            width=dp(200)
            )
        name_button.bind(
            on_press=self.on_button_press,
            on_release=self.on_button_release
            )
        new_grid.add_widget(name_button)
        
        for buttons in range(0, 6): #create the number buttons
            button_stock =OneLineListItem(
                text= '0',
                text_color= (1,0,0,1),
                theme_text_color= "Custom"
                )
            button_stock.id = str(buttons)
            button_stock.bind(on_release= self.quantity)
            new_grid.add_widget(button_stock)
        
        fabric_card = MDCardSwipe( #create the card swipe with the delete and no-stock icons
            MDCardSwipeLayerBox(
                MDIconButton(
                    icon="trash-can",
                    pos_hint={"center_y": 0.5},
                    on_release=self.remove_item
                    ),
                MDIconButton(
                    icon="cart",
                    id='6',
                    pos_hint={"center_y": 0.5},
                    on_release=self.out_of_stock
                    ),
                    ),
            MDCardSwipeFrontBox(new_grid),
                    size_hint_y=None,
                    height="52dp",
                    type_swipe= 'hand'      
                    )
        self.ids.box_grid.add_widget(fabric_card)
        
        if is_new == True: #flag to save the data
            self.persistence(fabric_card)

        self.ids.box_grid.do_layout()

  
    def out_of_stock(self, button, is_load=False):
        """button to change the state of the stock on a single grid"""
        
        if button.icon == "cart": #check the state of icon button to change for its counterpart
            button.icon = "cart-off"
            no_stock_check = True
        else:
            button.icon = "cart"
            no_stock_check = False
         
        if is_load is True: #check the button state on program launch  
            button.icon = "cart-off"
            
        grid = button.parent.parent.children[0].children[0] #get the path to the gridlayout
        
        for grid_button in grid.children: #change buttons content one-by-one ignoring the name button and save the data if needed
                grid_button.disabled = no_stock_check #this one put the row in grey and disable the button interaction
                if grid_button.id != '7': #if 7 is true, is the name and not need to be changed
                    grid_button.text = '0' 
                    if is_load == False:
                        self.update_db_data(self.get_btn_id(grid_button.id), grid.id, grid_button.text)
                                           
        if is_load == False: #save the state of the button
            self.update_db_data(self.get_btn_id(button.id), grid.id, no_stock_check)
        

    def get_btn_id(self, button_id):
        """Retrieves the corresponding database column name from a button ID."""
        try:
            return next(key for key, value in self.index_db_quantity_buttons.items() if value == int(button_id)) #check if the match with a value in the index and return key
        
        except StopIteration: #return None and display error message
            text= f"No matching key found for Button ID: {button_id}"
            self.error_message_popup(text)
            return None
        
    
    def remove_item(self, instance):
        """Removes an item from the list and database."""
        item_id_to_remove = instance.parent.parent.children[0].children[0].id #path to the item to be removed

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM fabrics WHERE id=?", (item_id_to_remove,))
                conn.commit()
                
        except sqlite3.Error as e:
            text= f"Error removing item from database:, {e}"
            self.error_message_popup(text)

        self.ids.box_grid.remove_widget(instance.parent.parent) #remove the row from the screen
        Clock.schedule_once(lambda dt: self.ids.box_grid.do_layout(), 0) #refresh the widgets
    

    def on_button_press(self, instance):
        """start the counter to change name."""
        self.start_time = Clock.get_time()


    def on_button_release(self, instance):
        """stop the counter to change name and display the dialog if hit the correct time"""
        elapsed_time = Clock.get_time() - self.start_time
        min_time = 0.08
        if elapsed_time > min_time:
            self.name_changer(instance)
        else:
            pass
    
    
    def name_changer(self, button):
        """dialog to input the new name for the grid
            -row_id: the if from the row parent of the name button
        """
        box_name_changer = MDBoxLayout()
        self.name_input = MDTextField(hint_text=button.text) #keep the previous name until the user change it
        box_name_changer.add_widget(self.name_input)
        row_id = button.parent.id 
        self.name_change_dialog = MDDialog(
            text= 'change name',
            type="custom",
            content_cls=box_name_changer,
            buttons=[
                MDRectangleFlatButton(
                    text='change', 
                    on_release=lambda *args: (
                        self.update_button_text_name(self.name_input.text, button, row_id),
                        self.name_change_dialog.dismiss()
                        )),
                MDRectangleFlatButton(
                    text='close',
                    on_release=lambda *args: self.name_change_dialog.dismiss()
                    )
                                      ]     
        )
        self.name_change_dialog.open()
    

    def update_button_text_name(self, new_text, button, row_id):
        """change the name in the 'name' button and check if the user input an empty string"""
        button.text = new_text if new_text != '' else button.text
        self.update_db_data(self.get_btn_id(button.id), row_id, new_text)
    
    
    def persistence(self, new_card):
        """function to add rows into db using the data from the card buttons if the ID doesn't exist"""
        card_data = new_card.children[0].children[0].children #path to get buttons content
        card_id = new_card.children[0].children[0].id #pat to get grid id
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM fabrics WHERE id=?", (card_id,))   
                result = cursor.fetchone() # check if the data exist in the db 
                if result is None:
                    cursor.execute(f"INSERT INTO fabrics VALUES (?,?,?,?,?,?,?,?,?)",(
                        card_id,
                        card_data[0].text,
                        card_data[1].text,
                        card_data[2].text,
                        card_data[3].text,
                        card_data[4].text,
                        card_data[5].text,
                        card_data[6].text,
                        False,
                        ))
                conn.commit()
    
        except sqlite3.Error as e:
            text= f"Error {e}"
            self.error_message_popup(text)
            
        self.print_table_data()
        
    def update_db_data(self, col, row_id, new_data):
        """this function update db data when the user press the button, saving the data in live mode."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE fabrics SET {col} = ? WHERE id = ?", (new_data, row_id))
                conn.commit()
                
        except sqlite3.Error as e:
            text = f"Error accessing database: {e}"
            self.error_message_popup(text)
            
        
        
        self.print_table_data()
    
    def load_data(self):
        """load the data from db when the program launch and create the table if not exist. them populate the data in the rows"""
        self.load_max_fabric()  #load the max quantity of fabrics
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                #create the table if doesn't exist
                create_table_query = """
                    CREATE TABLE IF NOT EXISTS fabrics (
                        id TEXT PRIMARY KEY,
                        small TEXT,
                        medium TEXT,
                        large TEXT,
                        r_small TEXT,
                        r_large TEXT,
                        Fab_count TEXT,
                        fname TEXT,
                        no_stock BOOLEAN
                    );
                    """
                cursor.execute(create_table_query)
                rows_to_load = cursor.execute('SELECT * FROM fabrics') #get data from fabrics
            
            for row in rows_to_load: #populate the data and charge the widgets in grid
                self.populate_data(row)
        
        except sqlite3.Error as e:
            text = f"Error accessing database: {e}"
            self.error_message_popup(text)
        
        Clock.schedule_once(lambda dt: self.ids.box_grid.do_layout(), 0) #refresh widgets
            
            
    # create the widgets in the grid on start
    def populate_data(self, row):
        """Create the widgets when program launch"""
        self.add_new_fabric_row(False)
        instance = self.ids.box_grid.children[0].children[0].children[0] #path to the row
        instance.id = row[0] #give id to the row
        instance.children[6].text = row[7] # insert name in the last row, because kivymd create the rows in reverse order
        self.populate_text_fields(instance, row) #fill the remain fields with the data
        self.apply_color_check(instance, row) #check the color for the numbers
    
    def populate_text_fields(self, instance, row):
        """fill the number fields"""
        for i in range (6):
            instance.children[i].text = row[6-i]
            
    
    def apply_color_check(self, instance, row):
        """check the right color for each number based on the min/max quantity and put it out of stock if row 8(no_stock flag) return true"""
        if row[8] == 1:
            self.out_of_stock(instance.parent.parent.children[1].children[0], True)
        else:
            for i in range(6):
                self.color_check(instance.children[i])

    def load_max_fabric(self):
        """load the value from data db and create the table if doesn't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS data (max_fabrics INTEGER)')
                cursor.execute('SELECT max_fabrics FROM data')
                result = cursor.fetchone()
                if result: #try to get the data and if return false, insert the default value and show a message
                    self.max_fabric = result[0]
                else:
                    cursor.execute('INSERT INTO data (max_fabrics) VALUES (?)', (self.max_fabric,))
                    text = f"Max value not found in database. Using default value: {self.max_fabric}"
                    self.error_message_popup(text)

        except sqlite3.Error as e:
            text = f"Error accessing database: {e}"
            self.error_message_popup(text)
        

    def save_max_fabric(self, max_fabrics_new):
        """save the value of max fabrics in db and handle errors"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE data SET max_fabrics = ?", (str(max_fabrics_new),))
                conn.commit()
        except sqlite3.Error as e:
            text = f"Error accessing database: {e}"
            self.error_message_popup(text)
        
    
    def export_to_pdf(self):
        """create the connection to db, retrieve the data and create the pdf in document folder"""
        app_data_dir = MDApp.get_running_app().user_data_dir
        database_path = os.path.join(app_data_dir, self.db_path)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT fname, small, medium, large, R_small, r_large, Fab_count FROM fabrics')
            data = cursor.fetchall()
            pdf_filename = 'C:/Users/marti/hello-world/stock_app_beta/fabric-App/output_a4.pdf'
            #pdf_filename = os.path.join(app_data_dir, 'output_a4.pdf')
            pdf = canvas.Canvas(pdf_filename, pagesize=A4)
        
            title = "Tablecloth and fabrics stock"
            title_y = A4[1] - 50
            pdf.drawString(200, title_y, title)
            
            table_data = [['Name', '1,40', '1,80', '2,30', 'R 1,40', 'R 1,80', 'Fabrics' ]] + list(data)
            table = Table(table_data, colWidths=[100, 70, 70, 70])
            
            style = TableStyle([ #apply styles to table
                ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
                ])
            table.setStyle(style)

            width, height = table.wrap(0, 0) # get the table width and height
            margin_top = 100 
            table.drawOn(pdf, 20, A4[1] - margin_top - height) # calculate the superior margin and adjust the start position
            pdf.save()
            

    #borrar al final/////////////////////////////////////////////////////////////////////////////////////////////////////  
        
    def print_table_data(self):
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute("PRAGMA table_info(fabrics)")
            columns = [column[1] for column in cur.fetchall()]
            cur.execute('SELECT * FROM fabrics')
            rows = cur.fetchall()
            print(f"{'':<10}", end="")  # Print an empty space for the column names alignment
            for column in columns:
                print(f"{column:<15}", end="")
            print("\n" + "-" * (15 * len(columns) + 10))
            for row in rows:
                print(f"{row[0]:<10}", end="")  # Assuming the first column is an ID
                for value in row[1:]:
                    print(f"{value:<15}", end="")
                print()
        except sqlite3.Error as e:
            text = f"Error {e}"
            self.error_message_popup(text)
        finally:
            if con:
                con.close()
        
    

class test(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        return ListGridLayout()
    


if __name__ == "__main__":
    test().run()