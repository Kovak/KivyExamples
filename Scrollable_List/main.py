from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.label import Label
from random import random


class RootWidget(Widget):
    def __init__(self, **kwargs):
    	super(RootWidget, self).__init__(**kwargs)
    	Clock.schedule_once(self.setup)

    def setup(self, dt):
    	for x in range(15):
	    	size_y = 150*random()
	    	if size_y < 20:
	    		size_y = 20
	    	l = CustomLabel(text='test', size_hint=(1.0, None), height=size_y)
	    	self.scrollview.content_layout.add_widget(l)


class ScrollableContainer(ScrollView):
	pass


class CustomLabel(Label):
	pass

class ScrollableListApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    ScrollableListApp().run()
