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
# check to remove the name_buttons list
#TODO: normalize syntaxis
# TODO: comment the code plis
# TODO settings panel
# TODO change the native kivy widgets for kivymd widgets
#TODO change the dismiss in the menu (delete the function)


class ListGridLayout(BoxLayout):
    # initialize infinite keywords
    def __init__(self):
        self.plus = True
        self.name_buttons = []
        self.max_fabric = 4
        self.min_fabric = 1
        self.out_of_stock_color = (0.42, 0.42, 0.42, 1)
        self.on_stock_color = (255,0,0,1)
        
        
        
        
    #   call grid layout constructor
        super(ListGridLayout, self).__init__()
    

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
        index_mapping = {'name': 5, '1,40': 4, '1,80': 3, '2,30': 2, 'R 1,40': 1, 'R 1,80': 0}

        if text in index_mapping:
            self.sort_elements(index_mapping[text])
         
         
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
          
    def fix_b_name_large():
        pass
            
    def add_instance(self, ids):
        self.new_grid = MDGridLayout(cols= 6, rows= 1)
        self.new_grid.id = str(uuid4())
        # self.b_name = MDRectangleFlatButton(text='  name  ', padding=(56,20), size= (dp(200), self.height), width=  self.parent.width * 0 + dp(140.0) )
        self.b_name = OneLineListItem(text='name', size_hint_x=None, width=dp(200))
        
        self.b_name.bind (on_press=self.on_button_press, on_release=self.on_button_release)
        self.name_buttons.append(self.b_name)
        self.new_grid.add_widget(self.b_name)
        
       
        for buttons in range(0, 5):
            # self.btn_stock = MDRectangleFlatButton(
            #                                         text= '0', line_color= self.on_stock_color, 
            #                                         text_color= (1,0,0,1), padding=(56,20),
            #                                         theme_text_color= "Custom",
            #                                         size_hint_x=0
            #                                         )
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
        self.button_index = self.name_buttons.index(instance)
        self.start_time = Clock.get_time()

    def on_button_release(self, instance):
        elapsed_time = Clock.get_time() - self.start_time
        min_time = 0.10
        if elapsed_time > min_time:
            self.name_changer(instance)
        else:
            pass


    # popUp to change the fabric name
    # TODO change the popup name
    #cambiar por mdialog y hacer la funcion para el dismiss unificada.
    
    def name_changer(self, button):
        self.box_name_changer = MDBoxLayout()
        index = self.name_buttons.index(button)
        self.name_input = MDTextField(hint_text=self.name_buttons[index].text, )
        self.box_name_changer.add_widget(self.name_input)
        name_change_dialog = MDDialog(text= 'change name',
                                      type="custom",
                                      content_cls=self.box_name_changer,
                                      buttons=[
                                          MDRectangleFlatButton(text='change', 
                                                                on_release=lambda *args: (self.update_button_text_name(self.name_input.text, button, index),
                                                                                            self.on_close_dialog(name_change_dialog))
                                                                ),
                                          MDRectangleFlatButton(text='close',
                                                                on_release=lambda *args: self.on_close_dialog(name_change_dialog)
                                                                )
                                      ]     
        )
        name_change_dialog.open()
    
    
    def update_button_text_name(self, new_text, button, index):
        self.name_buttons[index].text = self.name_input.text
    
    
    #function to close the dialog windows    
    def on_close_dialog(self, dialog):
        dialog.dismiss()
        

        

    # def persistence: un for que llame al add instance y que le inyecte desde las propiedades del widget todos los datos. (label='inserte variable aqui')
    # y tambien los settings.
        

class test(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.on_start
        
        
        return ListGridLayout()
    


if __name__ == "__main__":
    test().run()