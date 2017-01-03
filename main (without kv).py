import kivy
kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window

Window.size = (800,480)

import serial
#ser = serial.Serial('/dev/ttyUSB0', 115200)
ser = serial.Serial('COM3', 115200)

global digitalOutputBtn
digitalOutputBtn = [Button()]*8
global pumpDataLbl
pumpDataLbl = [Label()]*36


# Define some helper functions:

# This callback will be bound to the digital output buttons:
def press_callback(obj):
    if obj.state == "down":
        print ("button on")
        ser.write(obj.id + '1/')
    else:
        print ("button off")
        ser.write(obj.id + '0/')

#close app when exit button is pushed
def exit_callback(obj):
    App.get_running_app().stop()

# Periodically called to update digital inputs:
def update_digital_inputs(dt):
    digitalInputs = int(ser.readline().rstrip())
    for i in range(0,8):
        mask = 1 << i
        state = digitalInputs & mask
        state = state >> i
        if state == 1:
            digitalInputInd[i].state = 'down'
        else:
            digitalInputInd[i].state = 'normal'

# Periodically called to update data:
def update_data(dt):
    pump_data = ser.readline().rstrip()
    pump_data_array = pump_data.split(',')
    for i in range(0,36):
        pumpDataLbl[i].text = pump_data_array[i]

class MainScreen(Screen):

    def __init__(self,**kwargs):
        super (MainScreen,self).__init__(**kwargs)

        do_labels = ['Pump 1', 'Pump 2', 'Pump 3', 'Pump 4', 'Pump 5', 'Pump 6']

        # Set up the layout:
        main_layout = BoxLayout(orientation='vertical')
        di_layout = BoxLayout(orientation='vertical', spacing=5, padding=5, size_hint_x=None, width=200)
        do_layout = GridLayout(cols=6, rows=1, spacing=5, padding=5, size_hint_y=None, height=137.5)
        data_layout = GridLayout(cols=6, rows=6, size_hint_y=None, height=200)

        #main_layout.add_widget(di_layout)
        main_layout.add_widget(data_layout)
        main_layout.add_widget(do_layout)

        # Make the background gray:
        with main_layout.canvas.before:
            Color(.2,.2,.2,1)
            #self.rect = Rectangle(size=(800,480), pos=main_layout.pos)

        # Instantiate the digital input indicators:
        for i in range(0,8):
            digitalInputInd[i] = Button(text="Input_" + str(i))
        for i in range(0,36):
            pumpDataLbl[i] = Label(text='Null', markup=True)
            pumpDataLbl[i].font_size = '20sp'
            pumpDataLbl[i].texture_update()

        # Schedule the update of the state of the digital input indicators:
        event = Clock.schedule_interval(update_data, 0.01)

        # Create the rest of the UI objects (and bind them to callbacks, if necessary):
        for i in range(0,6):
            digitalOutputBtn[i] = ToggleButton(text=do_labels[i], id="digital/" + str(i) + "/", size=(127.5, 127.5), size_hint=(None, None))
            digitalOutputBtn[i].bind(on_press=press_callback)
            digitalOutputBtn[i].font_size = '20sp'
            digitalOutputBtn[i].texture_update()

        # Add the UI elements to the layout:
        for i in range(0,8):
            di_layout.add_widget(digitalInputInd[i])
        for i in range(0,6):
            do_layout.add_widget(digitalOutputBtn[i])
        for i in range(0,36):
            data_layout.add_widget(pumpDataLbl[i])
            
        self.add_widget(main_layout)  

'''class AnotherScreen(Screen):
    def __init__(self,**kwargs):
        super (AnotherScreen,self).__init__(**kwargs)
        another_layout = FloatLayout(orientation='horizontal')
        self.add_widget(another_layout)'''

sm = ScreenManager(transition=NoTransition())
main_screen = MainScreen(name='main_screen')
#another_screen = AnotherScreen(name='another_screen')
sm.add_widget(main_screen)
#sm.add_widget(another_screen)        

class MyApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
	MyApp().run()
