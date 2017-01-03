from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, ObjectProperty

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<TankControl>:
    orientation: 'vertical'

    Label:
        text: root.header
        font_size: '20sp'
        size_hint: 1, 0.15

    BoxLayout:
        orientation: 'horizontal'
        size_hint: 1, 0.85

        Slider:
            id: setpoint_slider
            orientation: 'vertical'
            value: float(root.tank_cmd) if root.tank_cmd != '' else 0
            min: root.slider_min
            max: root.slider_max
            step: root.slider_inc
            size_hint: 0.55, 1
            on_value: app.rio_data.set('tank_cmd/' + root.cmd_type + '/' + str(self.value), 'Null')

        FloatLayout:
            size_hint: 0.05, 1

            Label:
                text: str(setpoint_slider.max)
                pos: setpoint_slider.pos[0] + (setpoint_slider.width / 2) + 25, setpoint_slider.pos[1] + (setpoint_slider.height / 2) - 15

            Label:
                text: str(int(setpoint_slider.min))
                pos: setpoint_slider.pos[0] + (setpoint_slider.width / 2) + 25, setpoint_slider.pos[1] - (setpoint_slider.height / 2) + 15

        BoxLayout:
            orientation: 'vertical'
            size_hint: 0.4, 1
            spacing: 10

            BoxLayout:
                orientation: 'vertical'
                size_hint: 1, 0.25
                padding: 0, 2

                Label:
                    text: 'Actual:'
                    size_hint: 1, 0.3
                    text_size: self.size
                    halign: 'left'
                    valign: 'bottom'
                    padding: 2, 1

                Button:
                    text: root.actual
                    size_hint: 1, 0.7
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                    font_size: '20sp'
                    color: 0, 0, 0, 1
                    background_normal: 'atlas://data/images/defaulttheme/textinput'

            BoxLayout:
                orientation: 'vertical'
                size_hint: 1, 0.25
                padding: 0, 2

                Label:
                    text: 'Setpoint:'
                    size_hint: 1, 0.3
                    text_size: self.size
                    halign: 'left'
                    valign: 'bottom'
                    padding: 2, 1

                Button:
                    text: root.tank_cmd if root.tank_cmd != '' else '0'
                    size_hint: 1, 0.7
                    input_filter: 'int'
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                    font_size: '20sp'
                    color: 0, 0, 0, 1
                    background_normal: 'atlas://data/images/defaulttheme/textinput'

            BoxLayout:
                orientation: 'vertical'
                size_hint: 1, 0.5
                spacing: 2

                Button:
                    text: '+'
                    font_size: '25sp'
                    on_press: app.rio_data.set('tank_cmd/' + root.cmd_type + '_inc' + '/' + str(root.button_inc) + '/', 'Null')

                Button:
                    text: '-'
                    font_size: '25sp'
                    on_press: app.rio_data.set('tank_cmd/' + root.cmd_type + '_inc' + '/-' + str(root.button_inc) + '/', 'Null')
""")

class TankControl(BoxLayout):
  header = StringProperty('')
  slider_max = NumericProperty(0)
  slider_min = NumericProperty(0)
  slider_inc = NumericProperty(0)
  actual = StringProperty('')
  cmd_type = StringProperty('')
  tank_cmd = StringProperty('')
  button_inc = NumericProperty(0)
  id = ObjectProperty(None)

Factory.register('KivyB', module='TankControl')