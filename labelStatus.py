from kivy.uix.label import Label
from kivy.properties import ListProperty, StringProperty

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<LabelStatus>:
    bcolor: 1, 1, 1, 1
    text_size: self.size
    halign: 'center'
    valign: 'middle'
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
""")

class LabelStatus(Label):
    bstate = StringProperty('')
    bcolor = ListProperty([1, 1, 1, 1])

    def on_bstate(self, instance, state):
        if state == '0':
            self.text = 'Idle'
            self.bcolor = 0.34, 0.34, 0.34, 1
        elif state == '1':
            self.text = 'Manual'
            self.bcolor = 0.19, 0.64, 0.8, 1
        elif state == '2':
            self.text = 'Test Running'
            self.bcolor = 0.03, 0.55, 0.07, 1
        elif state == '3':
            self.text = 'Alarm'
            self.bcolor = 1, 0, 0, 1


Factory.register('KivyB', module='LabelStatus')