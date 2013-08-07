from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty

class RootWidget(Widget):
    pass

class MyCustomLayout1(FloatLayout):
	label_color = ListProperty([1., 1., 1., 1.])

class RulesExampleApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    RulesExampleApp().run()
