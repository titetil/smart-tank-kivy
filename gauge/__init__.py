#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

'''
Gauge
=====

The :class:`Gauge` widget is a widget for displaying gauge.

.. note::

Source svg file provided for customing.

'''

__all__ = ('Gauge',)

__title__ = 'garden.gauge'
__version__ = '0.2'
__author__ = 'julien@hautefeuille.eu'

import kivy
kivy.require('1.6.0')
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from os.path import join, dirname, abspath


class Gauge(Widget):
    '''
    Gauge class

    '''

    unit = NumericProperty(.384)
    value = BoundedNumericProperty(0, min=0, max=700, errorvalue=0)
    path = dirname(abspath(__file__))
    gauge_pic = StringProperty('gauge_1.png')
    #file_gauge = StringProperty(join(path, gauge_pic.defaultvalue))
    file_needle = StringProperty(join(path, "gauge (needle, small).png"))
    size_gauge = BoundedNumericProperty(230, min=128, max=500, errorvalue=128)
    size_text = NumericProperty(10)

    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)

        self._gauge = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        self._img_gauge = Image(
            source=join(self.path, self.gauge_pic),
            size=(self.size_gauge, self.size_gauge)
        )

        self._needle = Scatter(
            size=(self.size_gauge, self.size_gauge),
            do_rotation=False,
            do_scale=False,
            do_translation=False
        )

        _img_needle = Image(
            source=self.file_needle,
            size=(self.size_gauge, self.size_gauge),
            pos=(-9,-9)
        )

        self._glab = Label(font_size=self.size_text, markup=True)
        self._progress = ProgressBar(max=400, height=20, value=self.value)

        self._gauge.add_widget(self._img_gauge)
        self._needle.add_widget(_img_needle)

        self.add_widget(self._gauge)
        self.add_widget(self._needle)
        #self.add_widget(self._glab)
        #self.add_widget(self._progress)

        self.bind(pos=self._update)
        self.bind(size=self._update)
        self.bind(value=self._turn)
        self.bind(gauge_pic=self._gauge_pic)

    def _gauge_pic(self, *args):
        self._img_gauge.source = join(self.path, self.gauge_pic)

    def _update(self, *args):
        '''
        Update gauge and needle positions after sizing or positioning.

        '''
        self._gauge.pos = self.pos
        self._needle.pos = (self.x, self.y)
        self._needle.center = self._gauge.center
        self._glab.center_x = self._gauge.center_x
        self._glab.center_y = self._gauge.center_y + (self.size_gauge / 4)
        self._progress.x = self._gauge.x
        self._progress.y = self._gauge.y + (self.size_gauge / 4)
        self._progress.width = self.size_gauge

    def _turn(self, *args):
        '''
        Turn needle, 1 degree = 1 unit, 0 degree point start on 50 value.

        '''
        self._needle.center_x = self._gauge.center_x
        self._needle.center_y = self._gauge.center_y
        self._needle.rotation = (1 + self.unit) - (self.value * self.unit)
        self._glab.text = "[b]{0:.0f}[/b]".format(self.value)
        self._progress.value = self.value


if __name__ == '__main__':
    from kivy.uix.slider import Slider

    class GaugeApp(App):
        increasing = NumericProperty(1)
        begin = NumericProperty(50)
        step = NumericProperty(1)

        def build(self):
            box = BoxLayout(orientation='horizontal', padding=5)
            self.gauge = Gauge(value=-1, size_gauge=230, size_text=25, gauge_pic='gauge_2.png')
            self.slider = Slider(orientation='vertical', value=-1)

            box.add_widget(self.gauge)
            box.add_widget(self.slider)
            Clock.schedule_interval(lambda *t: self.gauge_increment(), 0.03)
            return box

        def gauge_increment(self):
            self.gauge.value = self.slider.value * 7

    GaugeApp().run()
