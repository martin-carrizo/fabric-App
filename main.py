from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import Layout
from kivy.uix.textinput import TextInput
from  kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView



# TODO: out of stock button
# TODO: delete button, fijarse de cambiar el largo en tiempo de ejecucion

class ListGridLayout(BoxLayout):
    # initialize infinite keywords
    def __init__(self, plus: bool):
        self.plus = plus
        self.name_buttons = []
        self.max_fabric = 4
        
        
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
        if int(button.text) == self.max_fabric:
            button.background_color = (0, 255, 0, 1)
        elif int(button.text) in range(1, self.max_fabric):
           button.background_color = (220, 255, 0, 1)
        else:
            button.background_color = (220, 0, 0, 1)
    
        
            
    def add_instance(self, ids):
        
        self.b_name = Button(text= 'name', color = (0, 0,0,1), pos=(200, 1))
        self.b_name.bind(on_press = self.name_changer)
        self.name_buttons.append(self.b_name)
        self.ids.main_grid.add_widget(self.b_name)
        self.ids.main_grid.row_default_height=40
        
        for buttons in range(0, 5):
            self.btn_stock = Button(text= '0', color = (0, 0,0,1), pos=((buttons * 100) , 1))
            self.btn_stock.bind(on_press= self.quantity)
            self.btn_stock.background_color = (220, 0, 0, 1)
            self.ids.main_grid.add_widget(self.btn_stock)
            self.ids.main_grid.rows += 1
            self.ids.main_grid
    
    

    def name_changer(self, button):
        popup = Popup(size_hint=(.30, .20))
        index = self.name_buttons.index(button)
        popup_content = BoxLayout(orientation='vertical')
        self.name_input = TextInput(text=self.name_buttons[index].text, multiline=False)
        popup_content.add_widget(self.name_input)

        close_button = Button(text="Cerrar", size_hint=(1, 0.2))
        close_button.bind(on_press=lambda instance: popup.dismiss())
        popup_content.add_widget(close_button)
        popup.content = popup_content
        
        def on_dismiss_callback(instance):
            entered_name = self.name_input.text
            self.name_buttons[index].text = entered_name

        popup.bind(on_dismiss=on_dismiss_callback)
        popup.open()

    



class test(App):
    def build(self):
        
        return ListGridLayout(True)


if __name__ == "__main__":
    test().run()