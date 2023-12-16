
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from  kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang import builder
from kivy.properties import ObjectProperty

# TODO: out of stock button 

    

class ListGridLayout(Widget):
    # initialize infinite keywords
    def __init__(self, plus: bool):
        self.plus = plus
    #   call grid layout constructor
        super(ListGridLayout, self).__init__()
        
    # add to stock
    def add_quantity(self):
        self.plus = True
        
    # subtract from the stock
    def sub_quantity(self):
        self.plus = False
    
    # manage the min/max
    def quantity(self, btn_id):
        if self.plus == True and int(btn_id.text) < 4:
            btn_id.text = str((int(btn_id.text) + 1))
            self.color_check(btn_id)
        elif self.plus == False and  int(btn_id.text) > 0:
            btn_id.text = str((int(btn_id.text) - 1))
            self.color_check(btn_id)
    

    # color change to every quantity
    
    def color_check(self, button):
        if int(button.text) == 4:
            button.background_color = (0, 255, 0, 1)
        elif int(button.text) in range(1, 4):
           button.background_color = (220, 255, 0, 1)
        else:
            button.background_color = (220, 0, 0, 1)
    
        
            
    def add_instance(self, ids):
        
        self.b_name = Button(text= 'name', color = (0, 0,0,1), pos=(200, 1))
        self.b_name.bind(on_press = self.name_changer)
        self.ids.main_grid.add_widget(self.b_name)
        
        for buttons in range (0, 5):
            self.btn_stock = Button(text= '0', color = (0, 0,0,1), pos=((buttons * 100) , 1))
            self.btn_stock.bind(on_press= self.quantity)
            self.btn_stock.background_color = (220, 0, 0, 1)
            self.ids.main_grid.add_widget(self.btn_stock)
            self.ids.main_grid.rows += 1
            
            
    
       
        
    
        
    def name_changer(self, buttom):
        pass

    

class test(App):
    def build(self):
        
        return ListGridLayout(True)


if __name__ == "__main__":
    test().run()