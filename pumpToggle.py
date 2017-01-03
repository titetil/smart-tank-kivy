from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty, StringProperty, ObjectProperty

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<PumpToggle>:
    font_size: '20sp'
    text: 'Pump ' + str(self.index + 1)
    on_press: app.rio_data.set('power_relay/' + str(self.index) + '/', self.state)

""")

class PumpToggle(ToggleButton):
    index = NumericProperty(0)

Factory.register('KivyB', module='PumpToggle')