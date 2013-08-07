from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty

class MyCustomLayout1(FloatLayout):
	label_color = ListProperty([1., 1., 1., 1.])