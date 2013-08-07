from kivy.app import App
from kivy.uix.widget import Widget
from layout1 import MyCustomLayout1
from kivy.lang import Builder
Builder.load_file('layout1.kv')

class RootWidget(Widget):
    pass

class RulesExampleApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    RulesExampleApp().run()
