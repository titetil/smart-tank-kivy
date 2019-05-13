import kivy
kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.config import Config
from math import sin
#from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.effectwidget import InvertEffect
import random
from gauge import Gauge

from kivy.core.window import Window

Window.size = (800,480)
Config.set('graphics', 'maxfps', '10')

import serial
import labelB, labelStatus, pumpCmdButtons, pumpCmdSlider, pumpToggle, tankControl
import collections

debug_mode = 0

class MainScreen(Screen):
    logged_in = NumericProperty(0)
    system_status = StringProperty('')
    alarm_popup = ObjectProperty(None)
    app_ref = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.start_inactivity_clock()

    def start_inactivity_clock(self):
        try:
            self.screen_inactive_event.cancel()
        except:
            pass
        self.screen_inactive_event = Clock.schedule_once(self.sys_inactive, 30)

    def sys_inactive(self, dt):
        self.app_ref.screen_man.current = 'gauge_screen'

    def on_system_status(self, instance, status):
        if status == '3':
            self.alarm_popup.open()
        else:
            try:
                self.alarm_popup.dismiss()
            except:
                pass

    def on_touch_down(self, touch):
        self.start_inactivity_clock()
        #passcode pop-up if area of tab headers are touched (other than 'Main'), and not logged in
        if touch.pos[0] > 104 and touch.pos[0] < 401 and touch.pos[1] < 480 and touch.pos[1] > 441 and self.logged_in == 0:
            self.ids.passcode_popup.open()
        return super(MainScreen, self).on_touch_down(touch)

class GaugeScreen(Screen):
    app_ref = ObjectProperty(None)

    def on_touch_down(self, touch):
        self.app_ref.screen_man.current = 'main_screen'
        self.app_ref.main_screen.start_inactivity_clock()

class ScreenManagement(ScreenManager):
    app_ref = ObjectProperty(None)

    def __init__(self,**kwargs):
        super (ScreenManagement,self).__init__(**kwargs)
        self.transition = NoTransition()

    def on_touch_down(self, touch):
        self.app_ref.main_screen.start_inactivity_clock()
        return super(ScreenManagement, self).on_touch_down(touch)

class MainApp(App):
    passcode = '1234'
    passcode_try = ''
    logged_in = NumericProperty(0)
    main_screen_ref = ObjectProperty(None)

    def build(self):
        self.rio_data = RIOData()
        '''try::
            self.main_screen = MainScreen()
        except:
            print('kivy error')
            ser.close()'''
        self.main_screen = MainScreen()
        self.screen_man = ScreenManagement()
        self.screen_man.current = 'main_screen'
        return self.screen_man

    def try_passcode(self, number):
        self.passcode_try = self.passcode_try + number
        if len(self.passcode_try) == len(self.passcode):
            if self.passcode_try == self.passcode:
                self.logged_in = 1
                self.main_screen_ref.add_widget(self.main_screen_ref.ids.logout_button)
            else:
                self.main_screen_ref.ids.main_tabbed_panel.switch_to(self.main_screen_ref.ids.main)
            self.passcode_try = ''
            self.main_screen_ref.ids.passcode_popup.dismiss()


class RIOData(Widget):
    time = NumericProperty(0.0)
    speed_1 = StringProperty('0')
    speed_2 = StringProperty('0')
    speed_3 = StringProperty('0')
    speed_4 = StringProperty('0')
    speed_5 = StringProperty('0')
    speed_6 = StringProperty('0')
    pressure_1 = StringProperty('0')
    pressure_2 = StringProperty('0')
    pressure_3 = StringProperty('0')
    pressure_4 = StringProperty('0')
    pressure_5 = StringProperty('0')
    pressure_6 = StringProperty('0')
    pressure_1_int = NumericProperty(0)
    pressure_2_int = NumericProperty(0)
    pressure_3_int = NumericProperty(0)
    pressure_4_int = NumericProperty(0)
    pressure_5_int = NumericProperty(0)
    pressure_6_int = NumericProperty(0)
    flow_1 = StringProperty('0')
    flow_2 = StringProperty('0')
    flow_3 = StringProperty('0')
    flow_4 = StringProperty('0')
    flow_5 = StringProperty('0')
    flow_6 = StringProperty('0')
    current_1 = StringProperty('0')
    current_2 = StringProperty('0')
    current_3 = StringProperty('0')
    current_4 = StringProperty('0')
    current_5 = StringProperty('0')
    current_6 = StringProperty('0')
    ph_current_1 = StringProperty('0')
    ph_current_2 = StringProperty('0')
    ph_current_3 = StringProperty('0')
    ph_current_4 = StringProperty('0')
    ph_current_5 = StringProperty('0')
    ph_current_6 = StringProperty('0')
    voltage_1 = StringProperty('0')
    voltage_2 = StringProperty('0')
    voltage_3 = StringProperty('0')
    voltage_4 = StringProperty('0')
    voltage_5 = StringProperty('0')
    voltage_6 = StringProperty('0')
    time_1 = StringProperty('0')
    time_2 = StringProperty('0')
    time_3 = StringProperty('0')
    time_4 = StringProperty('0')
    time_5 = StringProperty('0')
    time_6 = StringProperty('0')
    pump_state_1 = StringProperty('0')
    pump_state_2 = StringProperty('0')
    pump_state_3 = StringProperty('0')
    pump_state_4 = StringProperty('0')
    pump_state_5 = StringProperty('0')
    pump_state_6 = StringProperty('0')
    pump_cmd_1 = StringProperty('0')
    pump_cmd_2 = StringProperty('0')
    pump_cmd_3 = StringProperty('0')
    pump_cmd_4 = StringProperty('0')
    pump_cmd_5 = StringProperty('0')
    pump_cmd_6 = StringProperty('0')
    header_line_1 = StringProperty('0')
    header_line_2 = StringProperty('0')
    header_line_3 = StringProperty('0')
    header_line_4 = StringProperty('0')
    power_supply = StringProperty('0')
    temp_1 = StringProperty('0')
    temp_2 = StringProperty('0')
    system_status = StringProperty('0')
    ps_cmd = StringProperty('0')
    pressure_cmd = StringProperty('0')
    temp_cmd_1 = StringProperty('0')
    temp_cmd_2 = StringProperty('0')
    ps_enable = StringProperty('0')
    tog_button_spare_1 = StringProperty('0')
    tog_button_spare_2 = StringProperty('0')
    tog_button_spare_3 = StringProperty('0')
    tog_button_spare_4 = StringProperty('0')
    tog_button_spare_5 = StringProperty('0')
    pump_cmd_max = StringProperty('0')
    pump_cmd_inc = StringProperty('0')
    avg_pressure = StringProperty('0')
    alarm_message_1 = StringProperty('0')
    alarm_message_2 = StringProperty('0')
    recording = StringProperty('0')
    serial_number_1 = StringProperty('0')
    serial_number_2 = StringProperty('0')
    serial_number_3 = StringProperty('0')
    serial_number_4 = StringProperty('0')
    serial_number_5 = StringProperty('0')
    serial_number_6 = StringProperty('0')

    def __init__(self, **kwargs):
        super(RIOData, self).__init__(**kwargs)
        self.array_size = 85
        self.pump_data_array = ['0']*self.array_size
        Clock.schedule_interval(self.update_data, 0)

    def update_data(self, dt):
        if debug_mode == 0:
            try:
                self.pump_data_array = ser.readline().rstrip().split(',')
                #print(self.pump_data_array)
                #self.time = Clock.get_time()
            except:
                print('Serial Read Failure')
                exit()
        else:
            self.pump_data_array = ['0']*self.array_size
        if len(self.pump_data_array) == self.array_size:
            self.speed_1 = self.pump_data_array[0]
            #self.speed_1 = str(random.random() * 100)
            self.speed_2 = self.pump_data_array[1]
            self.speed_3 = self.pump_data_array[2]
            self.speed_4 = self.pump_data_array[3]
            self.speed_5 = self.pump_data_array[4]
            self.speed_6 = self.pump_data_array[5]
            self.pressure_1 = self.pump_data_array[6]
            #self.pressure_1 = str(random.random() * 5 + 650)
            self.pressure_2 = self.pump_data_array[7]
            self.pressure_3 = self.pump_data_array[8]
            self.pressure_4 = self.pump_data_array[9]
            self.pressure_5 = self.pump_data_array[10]
            self.pressure_6 = self.pump_data_array[11]
            self.pressure_1_int = int(self.pressure_1.split(' ')[0])
            self.pressure_2_int = int(self.pressure_2.split(' ')[0])
            self.pressure_3_int = int(self.pressure_3.split(' ')[0])
            self.pressure_4_int = int(self.pressure_4.split(' ')[0])
            self.pressure_5_int = int(self.pressure_5.split(' ')[0])
            self.pressure_6_int = int(self.pressure_6.split(' ')[0])
            self.flow_1 = self.pump_data_array[12]
            self.flow_2 = self.pump_data_array[13]
            self.flow_3 = self.pump_data_array[14]
            self.flow_4 = self.pump_data_array[15]
            self.flow_5 = self.pump_data_array[16]
            self.flow_6 = self.pump_data_array[17]
            self.current_1 = self.pump_data_array[18]
            self.current_2 = self.pump_data_array[19]
            self.current_3 = self.pump_data_array[20]
            self.current_4 = self.pump_data_array[21]
            self.current_5 = self.pump_data_array[22]
            self.current_6 = self.pump_data_array[23]
            self.ph_current_1 = self.pump_data_array[24]
            self.ph_current_2 = self.pump_data_array[25]
            self.ph_current_3 = self.pump_data_array[26]
            self.ph_current_4 = self.pump_data_array[27]
            self.ph_current_5 = self.pump_data_array[28]
            self.ph_current_6 = self.pump_data_array[29]
            self.voltage_1 = self.pump_data_array[30]
            self.voltage_2 = self.pump_data_array[31]
            self.voltage_3 = self.pump_data_array[32]
            self.voltage_4 = self.pump_data_array[33]
            self.voltage_5 = self.pump_data_array[34]
            self.voltage_6 = self.pump_data_array[35]
            self.time_1 = self.pump_data_array[36]
            self.time_2 = self.pump_data_array[37]
            self.time_3 = self.pump_data_array[38]
            self.time_4 = self.pump_data_array[39]
            self.time_5 = self.pump_data_array[40]
            self.time_6 = self.pump_data_array[41]
            self.pump_state_1 = self.pump_data_array[42]
            self.pump_state_2 = self.pump_data_array[43]
            self.pump_state_3 = self.pump_data_array[44]
            self.pump_state_4 = self.pump_data_array[45]
            self.pump_state_5 = self.pump_data_array[46]
            self.pump_state_6 = self.pump_data_array[47]
            self.pump_cmd_1 = self.pump_data_array[48]
            self.pump_cmd_2 = self.pump_data_array[49]
            self.pump_cmd_3 = self.pump_data_array[50]
            self.pump_cmd_4 = self.pump_data_array[51]
            self.pump_cmd_5 = self.pump_data_array[52]
            self.pump_cmd_6 = self.pump_data_array[53]
            self.header_line_1 = self.pump_data_array[54]
            self.header_line_2 = self.pump_data_array[55]
            self.header_line_3 = self.pump_data_array[56]
            self.header_line_4 = self.pump_data_array[57]
            self.power_supply = self.pump_data_array[58]
            self.temp_1 = self.pump_data_array[59]
            self.temp_2 = self.pump_data_array[60]
            self.system_status = self.pump_data_array[61]
            self.ps_cmd = self.pump_data_array[62]
            self.pressure_cmd = self.pump_data_array[63]
            self.temp_cmd_1 = self.pump_data_array[64]
            self.temp_cmd_2 = self.pump_data_array[65]
            self.ps_enable = self.pump_data_array[66]
            self.tog_button_spare_1 = self.pump_data_array[67]
            self.tog_button_spare_2 = self.pump_data_array[68]
            self.tog_button_spare_3 = self.pump_data_array[69]
            self.tog_button_spare_4 = self.pump_data_array[70]
            self.tog_button_spare_5 = self.pump_data_array[71]
            self.pump_cmd_max = self.pump_data_array[72]
            self.pump_cmd_inc = self.pump_data_array[73]
            self.avg_pressure = self.pump_data_array[74]
            self.alarm_message_1 = self.pump_data_array[75]
            self.alarm_message_2 = self.pump_data_array[76]
            self.recording = self.pump_data_array[77]
            self.serial_number_1 = self.pump_data_array[78]
            self.serial_number_2 = self.pump_data_array[79]
            self.serial_number_3 = self.pump_data_array[80]
            self.serial_number_4 = self.pump_data_array[81]
            self.serial_number_5 = self.pump_data_array[82]
            self.serial_number_6 = self.pump_data_array[83]

    def get(self, index):
        return self.pump_data_array[index]

    def set(self, command, state):
        if state == "down":
            int_state = '1'
        else:
            int_state = '0'
        ser.write(command + int_state)

if __name__ == '__main__':

    if debug_mode == 0:
        try:
            #ser = serial.Serial('COM4', 115200)
            ser = serial.Serial('/dev/ttyUSB0', 115200)
        except:
            print "Failed to connect"
            exit()

    MainApp().run()

    ser.close()
    print('closed')
