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
from kivy.properties import StringProperty, NumericProperty
from kivy.config import Config
from math import sin
#from kivy.garden.graph import Graph, MeshLinePlot

from kivy.core.window import Window

Window.size = (800,480)
Config.set('graphics', 'maxfps', '10')

import serial
import labelB, labelStatus, pumpCmdButtons, pumpCmdSlider, pumpToggle, tankControl
import collections

debug_mode = 0

class MainScreen(FloatLayout):
    logged_in = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        #self.graph_popup = GraphPopup()

    def on_touch_down(self, touch):
        #passcode pop-up if area of tab headers are touched (other than 'Main'), and not logged in
        if touch.pos[0] > 104 and touch.pos[0] < 401 and touch.pos[1] < 480 and touch.pos[1] > 441 and self.logged_in == 0:
            self.ids.passcode_popup.open()
        return super(MainScreen, self).on_touch_down(touch)

    #def show_graph_popup(self):
        #self.graph_popup = GraphPopup()


'''class PumpData(Label):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.main_ref.graph_popup.title = self.description
            self.graph.ylabel = self.text.split(' ')[1]
            self.main_ref.graph_popup.open()
        return super(PumpData, self).on_touch_down(touch)

class GraphPopup(Popup):
    pass

class TestGraph(Graph):
    graph_data = StringProperty('0')
    time = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super(TestGraph, self).__init__(**kwargs)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.add_plot(plot)
        self.plot = plot
        self.buffer_x = collections.deque(maxlen=100)
        self.buffer_y = collections.deque(maxlen=100)

    def on_time(self, instance, value):
        self.buffer_x.append(float("{0:.1f}".format(value))) #this formatting removes jitter from the graph
        self.buffer_y.append(float(self.graph_data.split(" ")[0]) * 10)
        self.plot.points = [(self.buffer_x[i], self.buffer_y[i]) for i in range(len(self.buffer_x))]
        self._xmin = self.buffer_x[0] + 0.05 #offsets remove jitter
        self._xmax = self.buffer_x[len(self.buffer_x) - 1] - 0.05
        if self._xmax != self._xmin:
            self.xmin = self._xmin
            self.xmax = self._xmax
            self._ymin = min(self.buffer_y) - min(self.buffer_y)*0.1
            self._ymax = max(self.buffer_y) * 1.1
            if self._ymax != self._ymin:
                self.ymin = self._ymin - 1
                self.ymax = self._ymax + 1
                self.y_ticks_major = (self.ymax - self.ymin) / 5'''

class MainApp(App):
    passcode = '1234'
    passcode_try = ''
    logged_in = NumericProperty(0)

    def build(self):
        self.rio_data = RIOData()
        '''try::
            self.main_screen = MainScreen()
        except:
            print('kivy error')
            ser.close()'''
        return MainScreen()

    def try_passcode(self, number):
        self.passcode_try = self.passcode_try + number
        if len(self.passcode_try) == len(self.passcode):
            if self.passcode_try == self.passcode:
                self.logged_in = 1
                self.root.add_widget(self.root.ids.logout_button)
            else:
                self.root.ids.main_tabbed_panel.switch_to(self.root.ids.main)
            self.passcode_try = ''
            self.root.ids.passcode_popup.dismiss()


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

    def __init__(self, **kwargs):
        super(RIOData, self).__init__(**kwargs)
        self.array_size = 75
        self.pump_data_array = ['0']*self.array_size
        Clock.schedule_interval(self.update_data, 0)

    def update_data(self, dt):
        if debug_mode == 0:
            try:
                self.pump_data_array = ser.readline().rstrip().split(',')
                #self.time = Clock.get_time()
            except:
                print('Serial Read Failure')
                exit()
        else:
            self.pump_data_array = ['0']*self.array_size
        if len(self.pump_data_array) == self.array_size:
            self.speed_1 = self.pump_data_array[0]
            self.speed_2 = self.pump_data_array[1]
            self.speed_3 = self.pump_data_array[2]
            self.speed_4 = self.pump_data_array[3]
            self.speed_5 = self.pump_data_array[4]
            self.speed_6 = self.pump_data_array[5]
            self.pressure_1 = self.pump_data_array[6]
            self.pressure_2 = self.pump_data_array[7]
            self.pressure_3 = self.pump_data_array[8]
            self.pressure_4 = self.pump_data_array[9]
            self.pressure_5 = self.pump_data_array[10]
            self.pressure_6 = self.pump_data_array[11]
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
            self.power_supply = self.pump_data_array[57]
            self.temp_1 = self.pump_data_array[58]
            self.temp_2 = self.pump_data_array[59]
            self.system_status = self.pump_data_array[60]
            self.ps_cmd = self.pump_data_array[61]
            self.pressure_cmd = self.pump_data_array[62]
            self.temp_cmd_1 = self.pump_data_array[63]
            self.temp_cmd_2 = self.pump_data_array[64]
            self.ps_enable = self.pump_data_array[65]
            self.tog_button_spare_1 = self.pump_data_array[66]
            self.tog_button_spare_2 = self.pump_data_array[67]
            self.tog_button_spare_3 = self.pump_data_array[68]
            self.tog_button_spare_4 = self.pump_data_array[69]
            self.tog_button_spare_5 = self.pump_data_array[70]
            self.pump_cmd_max = self.pump_data_array[71]
            self.pump_cmd_inc = self.pump_data_array[72]
            self.avg_pressure = self.pump_data_array[73]

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
            #ser = serial.Serial('COM3', 115200)
            ser = serial.Serial('/dev/ttyUSB0', 115200)
        except:
            print "Failed to connect"
            exit()

    MainApp().run()

    ser.close()
    print('closed')
