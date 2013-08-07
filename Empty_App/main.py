from kivy.app import App
from kivy.uix.widget import Widget


class RootWidget(Widget):
    pass

class EmptyApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    EmptyApp().run()
