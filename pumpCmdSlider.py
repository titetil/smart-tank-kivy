from kivy.uix.slider import Slider
from kivy.properties import NumericProperty, StringProperty

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<PumpCmdSlider>:
    orientation: 'vertical'
    value: float(self.pump_cmd) if self.pump_cmd != '' else 0
    min: 0
    max: int(app.rio_data.pump_cmd_max) if app.rio_data.pump_cmd_max != '' else 100
    step: int(app.rio_data.pump_cmd_inc) if app.rio_data.pump_cmd_inc != '' else 1
    on_value: app.rio_data.set('pump_cmd/' + str(self.index) + '/' + str(self.value), 'Null')
""")

class PumpCmdSlider(Slider):
  index = NumericProperty(0)
  pump_cmd = StringProperty('')

Factory.register('KivyB', module='PumpCmdSlider')