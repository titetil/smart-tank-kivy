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
from kivy.config import Config
from math import sin
#from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.effectwidget import InvertEffect
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from main import MainScreen, RIOData
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.graphics.transformation import Matrix
from math import radians
from kivy.uix.image import Image
from kivy.properties import BooleanProperty
from kivy.animation import Animation
import math

from kivy.core.window import Window

Window.size = (1920,1080)
Window.maximize()
Window.clearcolor = (1, 1, 1, 1)
#Window.fullscreen = True
#Config.set('graphics', 'maxfps', '10')

scale_global = 0.06
positions = [(1411.5, 428), (1460.5, 428), (1509.5, 428), (1558.5, 428)]

class MyScatterLayout(ScatterLayout):
    double_click = BooleanProperty(False)

    def on_touch_up( self, touch ):
        x, y = touch.x, touch.y
        # if the touch isnt on the widget we do nothing, just try children
        if not touch.grab_current == self:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if super(Scatter, self).on_touch_up(touch):
                touch.pop()
                return True
            touch.pop()

        # remove it from our saved touches
        if touch in self._touches and touch.grab_state:
            touch.ungrab(self)
            del self._last_touch_pos[touch]
            self._touches.remove(touch)

        # stop propagating if its within our bounds
        #if self.collide_point(x, y):
        #    return True
        if self.double_click:
            if self.collide_point(*touch.pos):
                if touch.is_double_tap:
                    if self.scale > scale_global:
                        scale = scale_global / self.scale
                        anim = Animation(scale=scale_global ** (1/30), duration=.5, s=1/30, pos = positions[int(self.id)])
                        anim.start(self)
                        #self.apply_transform(Matrix().scale(scale, scale, 1))
                        #self.pos = positions[int(self.id)]
                    else:
                        scale = 1 / self.scale
                        anim = Animation(scale=scale ** (1/30), duration=1, s=1/30, pos = (533, 316))
                        anim.start(self)
                        #self.apply_transform(Matrix().scale(scale, scale, 1))
                        #self.pos = (533, 316)

                    return super(MyScatterLayout, self).on_touch_up(touch)

    '''def alarm_animation(self, state):
        anim = Animation(opacity=0, duration=.5) + Animation(
            opacity=1, duration=.5)
        if state:
            anim.repeat = True
            anim.start(self.main_screen.ids.alarm_indicator)
        else:
            anim.cancel_all(self.main_screen.ids.alarm_indicator)
            self.main_screen.ids.alarm_indicator.opacity = 0
        self.alarm_state = state'''

    def transform_with_touch(self, touch):
        # just do a simple one finger drag
        changed = False
        if len(self._touches) == self.translation_touches:
            # _last_touch_pos has last pos in correct parent space,
            # just like incoming touch
            dx = (touch.x - self._last_touch_pos[touch][0]) \
                * self.do_translation_x
            dy = (touch.y - self._last_touch_pos[touch][1]) \
                * self.do_translation_y
            dx = dx / self.translation_touches
            dy = dy / self.translation_touches
            self.apply_transform(Matrix().translate(dx, dy, 0))
            changed = True

        if len(self._touches) == 1:
            return changed

        # we have more than one touch... list of last known pos
        points = [Vector(self._last_touch_pos[t]) for t in self._touches
                  if t is not touch]
        # add current touch last
        points.append(Vector(touch.pos))

        # we only want to transform if the touch is part of the two touches
        # farthest apart! So first we find anchor, the point to transform
        # around as another touch farthest away from current touch's pos
        anchor = max(points[:-1], key=lambda p: p.distance(touch.pos))

        # now we find the touch farthest away from anchor, if its not the
        # same as touch. Touch is not one of the two touches used to transform
        farthest = max(points, key=anchor.distance)
        if farthest is not points[-1]:
            return changed

        # ok, so we have touch, and anchor, so we can actually compute the
        # transformation
        old_line = Vector(*touch.ppos) - anchor
        new_line = Vector(*touch.pos) - anchor
        if not old_line.length():   # div by zero
            return changed

        angle = radians(new_line.angle(old_line)) * self.do_rotation
        self.apply_transform(Matrix().rotate(angle, 0, 0, 1), anchor=anchor)

        if self.do_scale:
            scale = new_line.length() / old_line.length()
            new_scale = scale * self.scale
            if new_scale < self.scale_min:
                scale = self.scale_min / self.scale
            elif new_scale > self.scale_max:
                scale = self.scale_max / self.scale
            self.apply_transform(Matrix().scale(scale, scale, scale),
                                 anchor=anchor)
            changed = True
        return changed

class MyFloatLayout(FloatLayout):
    pass

class MainApp(App):
    passcode = '1234'
    passcode_try = ''
    logged_in = NumericProperty(0)

    def build(self):
        self.rio_data = RIOData()
        main_layout = MyFloatLayout()
        image_scatter = MyScatterLayout(do_rotation=False)
        image_scatter.add_widget(Image(source='lab_layout.png', double_click = False))
        main_layout.add_widget(image_scatter)
        for i in range(4):
            tank_layout = BoxLayout(id = 'float_' + str(i), orientation='vertical', padding=25)
            tank_layout.add_widget(Label(text='Tank ' + str(i), size_hint=(1, .1), font_size='30sp', color=(0,0,0,1)))
            tank_layout.add_widget(MainScreen(size_hint=(1, .9)))
            tank_scatter = MyScatterLayout(id=str(i), do_rotation=False, size=(800, 528), size_hint=(None, None), scale=scale_global, pos=positions[i], double_click = True, on_scale=lambda scale: self.apply_transform(Matrix().scale(self.scale, self.scale, 1)))
            tank_scatter.add_widget(tank_layout)
            image_scatter.add_widget(tank_scatter)

        return main_layout


MainApp().run()

