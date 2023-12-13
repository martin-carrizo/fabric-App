from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from  kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class ListGridLayout(GridLayout):
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
        
         #buttoms para sumar y restar
        
        self.res_buttom = Button(text= '-')
        self.res_buttom.bind(on_press=self.res_quantity)
        self.add_widget(self.res_buttom)
        
        self.add_buttom = Button(text= '+')
        self.add_buttom.bind(on_press=self.add_quantity)
        self.add_widget(self.add_buttom)
        
        # indice de guia
        self.name = Label(text='name')
        self.add_widget(self.name)
        
        self.small = Label(text = '1,40')
        self.add_widget(self.small)
        
        self.medium = Label(text='1,80')
        self.add_widget(self.medium)
        
        self.large = Label(text='2,30')
        self.add_widget(self.large)
        
        self.small_r = Label(text='round 1,40')
        self.add_widget(self.small_r)
        
        self.large_r = Label(text='round 1,80')
        self.add_widget(self.large_r)
        
        # boton con nombre de tela 
        
        self.b_name = Button(text= 'name', color = (0, 0,0,1))
        self.b_name.bind(on_press = self.name_changer)
        self.add_widget(self.b_name)
        
        # botones de cada tela para sumarlo y restarlo
        
        self.thebuttom = Button(text= '0', color = (0, 0,0,1))
        self.thebuttom.bind(on_press= self.quantity)
        self.thebuttom.background_color = (220, 0, 0, 1)
        self.add_widget(self.thebuttom)
        
        self.thebuttom2 = Button(text= '0', color = (0, 0,0,1))
        self.thebuttom2.bind(on_press= self.quantity)
        self.thebuttom2.background_color = (220, 0, 0, 1)
        self.add_widget(self.thebuttom2)
        
    

    def add_quantity(self, button):
        self.plus = True
        
        
            
    def res_quantity(self, buttom):
        self.plus = False
        
    def quantity(self, buttom):
        if self.plus == True and int(buttom.text) < 4:
            buttom.text = str((int(buttom.text) + 1))
            self.color_check(buttom)
        elif self.plus == False and  int(buttom.text) > 0:
            buttom.text = str((int(buttom.text) - 1))
            self.color_check(buttom)


    # color change to every quantity
    
    def color_check(self, buttom):
        if int(buttom.text) == 4:
            buttom.background_color = (0, 255, 0, 1)
        elif int(buttom.text) in range(1, 4):
           buttom.background_color = (220, 255, 0, 1)
        else:
            buttom.background_color = (220, 0, 0, 1)
        
            
    def add_instance(self, buttom):
        self.thebuttom3 = Button(text= '0', color = (0, 0,0,1))
        self.thebuttom3.bind(on_press= self.quantity)
        self.thebuttom3.background_color = (220, 0, 0, 1)
        self.add_widget(self.thebuttom3)
    
        
    def name_changer(self, buttom):
         pop =  Popup (title='Test popup', 
                content=Label(text='Hello world'),
                size_hint=(None, None), size=(400, 400))w

         pop.open()
         text = TextInput(text='ingrese nombre')
         
         
          
        
        
       
        
        
        
    

class test(App):
    def build(self):
        
        return ListGridLayout("name", True)


if __name__ == "__main__":
    test().run()