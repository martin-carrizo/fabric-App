from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import Layout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from  kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
import uuid


#TODO: normalize syntaxis
# TODO: out of stock button
# TODO: delete button
# TODO: comment the code plis

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
        
        self.new_grid = GridLayout(cols= 6, rows= 1, size_hint_y=None)
        self.new_grid.id = str(uuid.uuid4())
        self.ids.box_grid.add_widget(self.new_grid)
        self.b_name = Button(text= 'name', color = (0, 0,0,1), pos=(200, 1))
        self.b_name.bind (on_press=self.on_button_press, on_release=self.on_button_release)
        self.name_buttons.append(self.b_name)
        self.new_grid.add_widget(self.b_name)
        self.new_grid.row_default_height=40
        
        
        for buttons in range(0, 5):
            self.btn_stock = Button(text= '0', color = (0, 0,0,1), pos=((buttons * 100) , 1))
            self.btn_stock.bind(on_press= self.quantity)
            self.btn_stock.background_color = (220, 0, 0, 1)
            self.new_grid.add_widget(self.btn_stock)
    
    
    # make a single function from these two
    def on_button_press(self, instance):
        # check this latter
        self.button_index = self.name_buttons.index(instance)
        self.start_time = Clock.get_time()

    def on_button_release(self, instance):
        elapsed_time = Clock.get_time() - self.start_time
        min_time = 0.20
        if elapsed_time < min_time:
            self.name_changer(instance)
        else:
            
            parent_id = instance.parent.id
            self.delete_line_by_id(parent_id)



    def name_changer(self, button):
        popup = Popup(size_hint=(.30, .20))
        index = self.name_buttons.index(button)
        popup_content = BoxLayout(orientation='vertical')
        self.name_input = TextInput(text=self.name_buttons[index].text, multiline=False)
        popup_content.add_widget(self.name_input)

        close_button = Button(text="Close", size_hint=(1, 0.2))
        close_button.bind(on_press=lambda instance: popup.dismiss())
        popup_content.add_widget(close_button)
        popup.content = popup_content
        
        def on_dismiss_callback(instance):
           self.name_buttons[index].text = self.name_input.text

        popup.bind(on_dismiss=on_dismiss_callback)
        popup.open()
   
    def delete_line_by_id(self, widget_id):
        print(widget_id)
        # search widget by id
        widget_to_delete = None
        for widget in self.ids.box_grid.children:
            if widget.id == widget_id:
                widget_to_delete = widget
                break
        # remove the widget
        self.ids.box_grid.remove_widget(widget_to_delete)

    


class test(App):
    def build(self):
        
        return ListGridLayout(True)


if __name__ == "__main__":
    test().run()