from kivy.app import App
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingItem
from kivy.uix.settings import SettingSpacer
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.label import Label

from settingsjson import settings_json, global_test

global_test = global_test()

Builder.load_string('''
<Interface>:
    orientation: 'vertical'
    Button:
        text: 'open the settings!'
        font_size: 150
        on_release: app.open_settings()
        
<-SettingScrollOptions>:
    size_hint: .25, None
    height: labellayout.texture_size[1] + dp(20)
    content: content
    canvas:
        Color:
            rgba: 47 / 255., 167 / 255., 212 / 255., self.selected_alpha
        Rectangle:
            pos: self.x, self.y + 1
            size: self.size
        Color:
            rgb: .2, .2, .2
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1

    BoxLayout:
        pos: root.pos

        Label:
            size_hint_x: .66
            id: labellayout
            markup: True
            text: root.title or ''
            font_size: '15sp'
            text_size: self.width - 32, None

        BoxLayout:
            id: content
            size_hint_x: .33
            
            Button:
                text: root.value or ''
        

''')

class Interface(BoxLayout):
    pass

class SettingsApp(App):
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        setting = self.config.get('example', 'boolexample')
        return Interface()

    def build_config(self, config):
        config.setdefaults('example', {
            'boolexample': True,
            'numericexample': 10,
            'optionsexample': 'option2',
            'stringexample': 'some_string',
            'pathexample': '/some/path'})

    def build_settings(self, settings):
        settings.register_type('scrolloptions', SettingScrollOptions)
        settings.add_json_panel('Panel Name',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value
        print global_test.get()
        global_test.set(2)
        print global_test.get()


class SettingScrollOptions(SettingItem):
    options = ListProperty([])
    '''List of all availables options. This must be a list of "string" items.
    Otherwise, it will crash. :)

    :attr:`options` is a :class:`~kivy.properties.ListProperty` and defaults
    to [].
    '''

    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it is shown.

    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _set_option(self, instance):
        self.value = instance.text
        self.popup.dismiss()

    def _create_popup(self, instance):
        # global oORCA
        # create the popup

        content = GridLayout(cols=1, spacing='5dp')
        scrollview = ScrollView(do_scroll_x=False)
        scrollcontent = GridLayout(cols=1, spacing='5dp', size_hint=(None, None))
        scrollcontent.bind(minimum_height=scrollcontent.setter('height'))
        self.popup = popup = Popup(content=content, title=self.title, size_hint=(0.5, 0.9), auto_dismiss=False)

        # we need to open the popup first to get the metrics
        popup.open()
        # Add some space on top
        content.add_widget(Widget(size_hint_y=None, height=dp(2)))
        # add all the options
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid, size=(popup.width, dp(55)), size_hint=(None, None))
            btn.bind(on_release=self._set_option)
            scrollcontent.add_widget(btn)

        # finally, add a cancel button to return on the previous panel
        scrollview.add_widget(scrollcontent)
        content.add_widget(scrollview)
        content.add_widget(SettingSpacer())
        # btn = Button(text='Cancel', size=((oORCA.iAppWidth/2)-sp(25), dp(50)),size_hint=(None, None))
        btn = Button(text='Cancel', size=(popup.width, dp(50)), size_hint=(0.9, None))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)

        #super(SettingScrollOptions, self)._create_popup(instance)

SettingsApp().run()