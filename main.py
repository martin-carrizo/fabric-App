from kivymd.app import MDApp

from kivymd.uix.card import (MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox)
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDTextButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp #<---- esto sirve para cambiar la resolucion de los pixeles de forma dinamica, revisar
from kivymd.uix.slider import MDSlider
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDList
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.datatables import MDDataTable

from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from uuid import uuid4
import sqlite3
#TODO: normalize syntaxis
# TODO: comment the code plis
# TODO settings panel
# TODO change the native kivy widgets for kivymd widgets
#TODO change the dismiss in the menu (delete the function)


class ListGridLayout(BoxLayout):
    # initialize infinite keywords
    def __init__(self):
        self.plus = True
        self.max_fabric = 4
        self.min_fabric = 1
        self.out_of_stock_color = (0.42, 0.42, 0.42, 1)
        self.on_stock_color = (255,0,0,1)
        self.index_size_mapping = {'name': 5, '1,40': 4, '1,80': 3, '2,30': 2, 'R 1,40': 1, 'R 1,80': 0}
        self.loaded_rows = set()
        
        
    #   call grid layout constructor
        super(ListGridLayout, self).__init__()
        Clock.schedule_once(lambda dt: self.load_data(), 0)
    

    #aca agregar el slider para la cantidad maxima de objetos.       
    def options_menu(self, button):
       self.menu_list = [
            {
                "viewclass": "OneLineListItem",
                "text": 'set max quantity',
                "on_release": self.set_max_quantity_dialog
            },
            {
                "viewclass": "OneLineListItem",
                "text": 'remove all fabrics',
                "on_release": self.delete_dialog
            }
       ]
       self.menu = MDDropdownMenu(

           caller = button,
           items = self.menu_list,
           width_mult=3,
           
       )
       self.menu.open()
       
    
    
    def set_max_quantity_dialog(self):
        
        self.set_max_quantity_screen = MDDialog(text='set new max quantity',
                                                type="custom",
                                                content_cls=MDSlider(),
                                                buttons=[
                                                    MDRectangleFlatButton(text='hi')
                                                ]
                                                
                                      )
        self.set_max_quantity_screen.open()
    #need more work        

    def delete_dialog(self):
        self.delete_dialog_screen = MDDialog(text='are you sure you want to remove all fabrics? this action cant be undone',
                                      buttons=[
                                        MDRectangleFlatButton(text='yes, remove', on_release=self.delete_all_fabrics),
                                        MDRectangleFlatButton(text='cancel', on_release=lambda *args: self.on_close_dialog(self.delete_dialog_screen))
                                      ]
                                      
                                      
                                      
                                      )
        self.delete_dialog_screen.open()

    def delete_all_fabrics(self, instance):
        
        self.ids.box_grid.clear_widgets()
        self.delete_dialog_screen.dismiss()
    
       
        
    
    
    def sort_fabric_by(self, text):
        
        if text in self.index_size_mapping:
            self.sort_elements(self.index_size_mapping[text])
         
         
    def sort_elements(self, index):
        sorted_cards = sorted(
            (card for card in self.ids.box_grid.children if isinstance(card, MDCardSwipe)),
            key=lambda card: card.children[0].children[0].children[index].text
        )
        
        # remove the widgets from the box_grid
        self.ids.box_grid.clear_widgets()
        
        # add sorted widgets to box_grid
        for sorted_card in sorted_cards:
            self.ids.box_grid.add_widget(sorted_card)
            
        # refresh the screen
        Clock.schedule_once(lambda dt: self.ids.box_grid.do_layout(), 0)
            
            
            
            
    # esto funciona, pero quiero simplificarlo mas 
    def stock_quantity(self):
        if self.plus:
            self.plus = False
            self.ids.quantity_button.text = '-'
        else:
            self.plus = True
            self.ids.quantity_button.text = '+'
    
    
    # manage the add/substract button
    def quantity(self, btn_id):
        if self.plus == True and int(btn_id.text) < self.max_fabric:
            btn_id.text = str((int(btn_id.text) + 1))
            self.color_check(btn_id)
        elif self.plus == False and  int(btn_id.text) > 0:
            btn_id.text = str((int(btn_id.text) - 1))
            self.color_check(btn_id)


    # color change to every quantity
    def color_check(self, button):
        if int(button.text) == self.max_fabric:
            button.line_color = (0, 0.871, 0, 1)
            button.text_color = (0, 0.871, 0, 1)
        elif int(button.text) in range(self.min_fabric, self.max_fabric):
           button.line_color = (0.851, 0.859, 0)
           button.text_color = (0.851, 0.859, 0)
        else:
            button.line_color = (0.8, 0, 0, 1)
            button.text_color = (0.8, 0, 0, 1)        
          
            
    def add_instance(self, ids):
        self.new_grid = MDGridLayout(cols= 6, rows= 1)
        self.new_grid.id = str(uuid4())
        self.b_name = OneLineListItem(text='name', size_hint_x=None, width=dp(200))
        
        self.b_name.bind (on_press=self.on_button_press, on_release=self.on_button_release)
        # self.name_buttons.append(self.b_name)
        self.new_grid.add_widget(self.b_name)
        
       
        for buttons in range(0, 5):
            self.btn_stock =OneLineListItem(
                                                    text= '0', text_color= (1,0,0,1),theme_text_color= "Custom",
                                                    )
            self.btn_stock.id = 'stockbtn'
            self.btn_stock.bind(on_release= self.quantity)
            
            self.new_grid.add_widget(self.btn_stock)
        self.fabric_card = MDCardSwipe(
                    MDCardSwipeLayerBox(
                            MDIconButton(
                            icon="trash-can",
                            pos_hint={"center_y": 0.5},
                            on_release=self.remove_item
                            ),
                            MDIconButton(
                            icon="cart",
                            pos_hint={"center_y": 0.5},
                            on_release=self.out_of_stock
                            ),
                            ),

                    MDCardSwipeFrontBox(self.new_grid),
                    size_hint_y=None,
                    height="52dp",
                    type_swipe= 'hand'      
                                        )
        self.ids.box_grid.add_widget(self.fabric_card)
        self.persistence(self.fabric_card)
        self.ids.box_grid.do_layout()

    # button to change the state of the stock on a single grid
    def out_of_stock(self, button):
        card_root = button.parent.parent.children[0]
        if button.icon == "cart":
            button.icon = "cart-off"
            no_stock = True
        else:
            button.icon = "cart"
            no_stock = False
        for grid in card_root.children:
            for grid_button in grid.children:
                    grid_button.disabled = no_stock
                    if grid_button.id == 'stockbtn':
                        grid_button.line_color = self.out_of_stock_color if no_stock == True else self.on_stock_color
                        grid_button.text_color = self.out_of_stock_color if no_stock == True else (1,0,0)
                        grid_button.text = '0'

         
        
    # remove the fabric from the list
    def remove_item(self, instance):
        self.ids.box_grid.remove_widget(instance.parent.parent)
    
    # make a single function from these two
    def on_button_press(self, instance):
        # check this latter
        # self.button_index = self.name_buttons.index(instance)
        self.start_time = Clock.get_time()

    def on_button_release(self, instance):
        elapsed_time = Clock.get_time() - self.start_time
        min_time = 0.10
        if elapsed_time > min_time:
            self.name_changer(instance)
        else:
            pass

    
    def name_changer(self, button):
        self.box_name_changer = MDBoxLayout()
        self.name_input = MDTextField(hint_text=button.text)
        self.box_name_changer.add_widget(self.name_input)
        row_id = button.parent.id
        name_change_dialog = MDDialog(text= 'change name',
                                      type="custom",
                                      content_cls=self.box_name_changer,
                                      buttons=[
                                          MDRectangleFlatButton(text='change', 
                                                                on_release=lambda *args: (self.update_button_text_name(self.name_input.text, button, row_id),
                                                                                            self.on_close_dialog(name_change_dialog))
                                                                ),
                                          MDRectangleFlatButton(text='close',
                                                                on_release=lambda *args: self.on_close_dialog(name_change_dialog)
                                                                )
                                      ]     
        )
        name_change_dialog.open()
    
    
    def update_button_text_name(self, new_text, button, row_id):
        button.text = new_text
        print(button.parent.id)
        self.update_db_data('fname', row_id, new_text)
    
    
    
    
    #function to close the dialog windows    
    def on_close_dialog(self, dialog):
        dialog.dismiss()
        

    def persistence(self, new_card):

        #create the connection to db
        save_data_con = sqlite3.connect('fabric_db.db')
        #create cursor
        save_data_cursor = save_data_con.cursor()
        
        #path to get buttons content
        card_data = new_card.children[0].children[0].children
        
        #pat to get grid id
        card_id = new_card.children[0].children[0].id
        
        
            
        save_data_cursor.execute("SELECT card_id FROM fabrics WHERE card_id=?", (card_id,))
        result = save_data_cursor.fetchone()
            #create the row and fill it with the card data
        if result is None:
            save_data_cursor.execute(f"INSERT INTO fabrics VALUES (?,?,?,?,?,?,?)", (
                                                                                    card_id,
                                                                                    card_data[0].text,
                                                                                    card_data[1].text,
                                                                                    card_data[2].text,
                                                                                    card_data[3].text,
                                                                                    card_data[4].text,
                                                                                    card_data[5].text,
                                                                                    ))
        
        #insert the data into the table
        save_data_con.commit()
        
        save_data_con.close()
        #aca tendria que tener una funcion que tome como parametro el indice de la iteracion y haga el trabajo para cada uno.
        
        
    
    def update_db_data(self, col, row_id, new_data):
        #create the connection to db
        update_data_con = sqlite3.connect('fabric_db.db')
        #create cursor
        update_data_cursor = update_data_con.cursor()
        update_data_cursor.execute(f"UPDATE fabrics SET {col} = ? WHERE id = ?", (new_data, row_id))
        update_data_con.commit()
        update_data_con.close()
        
    def load_data(self):
        #claro, el add_instance agrega a la base de datos cuando crea el objeto.
        self.view_data()
        load_data_con = sqlite3.connect('fabric_db.db')
        load_data_cursor = load_data_con.cursor()
        # Create the table if it doesn't exist
        load_data_cursor.execute("CREATE TABLE if not exists fabrics(id, small, medium, large, rsmall, lsmall, fname)")
        # load_data_cursor.execute("CREATE TABLE if not exists row_count(row_qtity)")

        # # Obtener las filas actuales en la tabla
        # rows = load_data_cursor.execute("SELECT * FROM fabrics").fetchall()
        # load_data_cursor.execute('INSERT INTO row_count VALUES (?)',(10,))
        # rows_to_load = load_data_cursor.execute('SELECT row_qtity FROM row_count').fetchone()
        # print(rows_to_load)
        

        # Cerrar la conexión a la base de datos
        load_data_cursor.close()
        load_data_con.close()
        
        
        
        # while int(rows_to_load) > 0:
        #     self.add_instance(self.ids.box_grid)

        # Refresh the screen
        Clock.schedule_once(lambda dt: self.ids.box_grid.do_layout(), 0)
    
        
        
#crear un metodo que salve los widgets a medida que se crean.
#crear un metodo que borre los datos a medida que se borran.
#crear un metodo que cierre la conexion luego de usarla.
#definir la tabla y los saves necesarios. en este caso serian los widgets y los settings de usuario.
#crear un metodo que cargue todos los widgets al iniciar.
        

class test(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        return ListGridLayout()
    


if __name__ == "__main__":
    test().run()