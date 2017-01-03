from kivy.uix.label import Label
from kivy.properties import ListProperty, StringProperty

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<LabelB>:
  bcolor: 1, 1, 1, 1
  canvas.before:
    Color:
      rgba: self.bcolor
    Rectangle:
      pos: self.pos
      size: self.size
""")

class LabelB(Label):
  bcolor = ListProperty([1, 1, 1, 1])
  bcolor_on = ListProperty([1, 1, 1, 1])
  bcolor_off = ListProperty([1, 1, 1, 1])
  bstate = StringProperty('')

  def on_bstate(self, instance, state):
      if state == '1':
          self.bcolor = self.bcolor_on
      else:
          self.bcolor = self.bcolor_off

Factory.register('KivyB', module='LabelB')