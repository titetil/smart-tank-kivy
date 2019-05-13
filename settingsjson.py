
import json
from kivy.uix.widget import Widget


class global_test(Widget):
    global_test = 1

    def set(self, value):
        self.global_test = value

    def get(self):
        return self.global_test

settings_json = json.dumps([
    {'type': 'title',
     'title': 'example title'},
    {'type': 'bool',
     'title': 'A boolean setting',
     'desc': 'Boolean description text',
     'section': 'example',
     'key': 'boolexample'},
    {'type': 'numeric',
     'title': 'A numeric setting',
     'desc': 'Numeric description text',
     'section': 'example',
     'key': 'numericexample'},
    {'type': 'scrolloptions',
     'title': 'An options setting',
     'desc': 'Options description text',
     'section': 'example',
     'key': 'optionsexample',
     'options': ['option1', 'option2', 'option3', '40', '5', '6', '7', '8', '9']},
    {'type': 'string',
     'title': 'A string setting',
     'desc': 'String description text',
     'section': 'example',
     'key': 'stringexample'},
    {'type': 'path',
     'title': 'A path setting',
     'desc': 'Path description text',
     'section': 'example',
     'key': 'pathexample'}])
