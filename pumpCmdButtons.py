from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<PumpCmdButtons>:
    id: pump_cmd_buttons
    rows: 1
    cols: 2

    Button:
        text: '+'
        font_size: '20sp'
        on_press: app.rio_data.set('pump_cmd/' + str(pump_cmd_buttons.index) + '/1/', 'Null'); pump_cmd_buttons.slider_ref.value = float(pump_cmd_buttons.pump_cmd) + 1

    Button:
        text: '-'
        font_size: '20sp'
        on_press: app.rio_data.set('pump_cmd/' + str(pump_cmd_buttons.index) + '/-1/', 'Null'); pump_cmd_buttons.slider_ref.value = float(pump_cmd_buttons.pump_cmd) - 1
""")

class PumpCmdButtons(GridLayout):
    index = NumericProperty(0)
    slider_ref = ObjectProperty(None)
    pump_cmd = StringProperty('')

Factory.register('KivyB', module='PumpCmdButtons')