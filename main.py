from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty
from kivymd.uix.card import (MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox)
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDRectangleFlatButton


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from uuid import uuid4

# check to remove the name_buttons list
#TODO: normalize syntaxis
# TODO: out of stock button
# TODO: comment the code plis
# TODO: toggle button for add/rest

class ListGridLayout(BoxLayout):
    # initialize infinite keywords
    def __init__(self):
        self.plus = True
        self.name_buttons = []
        self.max_fabric = 4
        self.out_of_stock_color = (0.42, 0.42, 0.42, 1)
        self.no_stock_color = (255,0,0,1)
        
        
        
    #   call grid layout constructor
        super(ListGridLayout, self).__init__()

    
    # also this two will become one
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
            button.line_color = (0, 0.871, 0, 1)
            button.text_color = (0, 0.871, 0, 1)
        elif int(button.text) in range(1, self.max_fabric):
           button.line_color = (0.851, 0.859, 0)
           button.text_color = (0.851, 0.859, 0)
        else:
            button.line_color = (0.8, 0, 0, 1)
            button.text_color = (0.8, 0, 0, 1)        
            
    def add_instance(self, ids):
        
        
        self.new_grid = GridLayout(cols= 6, rows= 1)
        self.new_grid.id = str(uuid4())
        self.b_name = MDRectangleFlatButton(text='name', padding=(56,20))
        self.b_name.bind (on_press=self.on_button_press, on_release=self.on_button_release)
        self.name_buttons.append(self.b_name)
        self.new_grid.add_widget(self.b_name)
        
        for buttons in range(0, 5):
            self.btn_stock = MDRectangleFlatButton(text= '0', line_color= self.no_stock_color, text_color= (1,0,0,1), padding=(60,20))
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
                            icon="cart-off",
                            pos_hint={"center_y": 0.5},
                            on_release=self.out_of_stock
                            ),
                            MDIconButton(
                            icon="cart",
                            pos_hint={"center_y": 0.5},
                            on_release=self.on_stock
                            )
                            ),

                    MDCardSwipeFrontBox(self.new_grid),
                    size_hint_y=None,
                    height="52dp"          
                                        )
        self.ids.box_grid.add_widget(self.fabric_card)
        self.ids.box_grid.do_layout()


    # change all the row buttons to grey and deactivate his binds
    def out_of_stock(self, button):
        
        parent_id = button.parent.parent.children[0]
        for child_widget in parent_id.children:
            pass
        
        # fix the text in the imput text
        for grandchild_widget in child_widget.children:
            grandchild_widget.line_color = self.out_of_stock_color
            grandchild_widget.text_color = self.out_of_stock_color
            grandchild_widget.text ='0'
            grandchild_widget.disabled = True
    
        # fix the color when the row return to normal state
    def on_stock(self, button):
        parent_id = button.parent.parent.children[0]
        for child_widget in parent_id.children:
            pass
        for grandchild_widget in child_widget.children:
            grandchild_widget.line_color = self.no_stock_color
            grandchild_widget.text_color = (1,0,0,1)
            grandchild_widget.disabled = False
            
        
    
           
        
        
        
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
        min_time = 0.20
        if elapsed_time < min_time:
            self.name_changer(instance)
        else:
            pass
        # block buttons to slide


    # popUp to change the fabric name
    def name_changer(self, button):
        popup = Popup(size_hint=(.30, .20))
        index = self.name_buttons.index(button)
        popup_content = BoxLayout(orientation='vertical')
        self.name_input = TextInput(text=self.name_buttons[index].text, multiline=False)
        popup_content.add_widget(self.name_input)

        # button to close the popUp
        close_button = MDRectangleFlatButton(text="////////////////Close///////////////////", size_hint=(1, 0.2))
        close_button.bind(on_press=lambda instance: popup.dismiss())
        popup_content.add_widget(close_button)
        popup.content = popup_content
        
        # TODO add a dismiss button
        
        # callback to confirm the change
        def on_dismiss_callback(instance):
           self.name_buttons[index].text = self.name_input.text

        popup.bind(on_dismiss=on_dismiss_callback)
        popup.open()
        

class test(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return ListGridLayout()


if __name__ == "__main__":
    test().run()