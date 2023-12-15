
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
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
    def __init__(self, name: str, plus: bool):
        self.name = name
        self.plus = plus
    #   call grid layout constructor
        super(ListGridLayout, self).__init__()
        
        # set columns
        self.cols = 6
        
        # set rows
        self.rows = 5
        
        # buttom to add more fabrics
        
        self.add_fabric = Button(text='add fabric')
        self.add_fabric.bind(on_press= self.add_instance)
        self.add_widget(self.add_fabric)
        self.rows += 1
        print(self.rows)
        
        
        
        # boton con nombre de tela 
        
        self.b_name = Button(text= 'name', color = (0, 0,0,1))
        self.b_name.bind(on_press = self.name_changer)
        self.add_widget(self.b_name)
        
        # botones de cada tela para sumarlo y restarlo
        
    # add to stock
    def add_quantity(self):
        self.plus = True
        
    # subtract from the stock
    def sub_quantity(self):
        self.plus = False
    
    # 
    def quantity(self, btn_id):
        if self.plus == True and int(btn_id.text) < 4:
            btn_id.text = str((int(btn_id.text) + 1))
            self.color_check(btn_id)
        elif self.plus == False and  int(btn_id.text) > 0:
            btn_id.text = str((int(btn_id.text) - 1))
            self.color_check(btn_id)
    

    # color change to every quantity
    
    def color_check(self, buttom):
        if int(buttom.text) == 4:
            buttom.background_color = (0, 255, 0, 1)
        elif int(buttom.text) in range(1, 4):
           buttom.background_color = (220, 255, 0, 1)
        else:
            buttom.background_color = (220, 0, 0, 1)
        
            
    def add_instance(self):
        self.thebuttom3 = Button(text= '0', color = (0, 0,0,1))
        self.thebuttom3.bind(on_press= self.quantity)
        self.thebuttom3.background_color = (220, 0, 0, 1)
        self.add_widget(self.thebuttom3)
    
        
    def name_changer(self, buttom):
        pass
        
        
        
        
         
         
         
          
        
        
       
        
        
        
    

class test(App):
    def build(self):
        
        return ListGridLayout('juan', True)


if __name__ == "__main__":
    test().run()