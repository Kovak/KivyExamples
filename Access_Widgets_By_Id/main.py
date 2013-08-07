from kivy.app import App
from kivy.uix.widget import Widget


class RootWidget(Widget):
    
    def get_widget_by_id(self, w_id):
    	print self.ids[w_id]

class Access_WidgetsApp(App):

    def build(self):
        pass

    def on_start(self):
    	print self.root.ids

if __name__ == '__main__':
    Access_WidgetsApp().run()
