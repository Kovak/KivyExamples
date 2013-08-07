from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from functools import partial

class CountWidget(Widget):
	count = NumericProperty(0)

	def __init__(self, **kwargs):
		super(CountWidget, self).__init__(**kwargs)
		Clock.schedule_interval(self.increment_count, 1.0)
		Clock.schedule_once(partial(self.example_with_partial, 
				'partial function called'), 2.5)

	def example_with_partial(self, string, dt):
		print string

	def increment_count(self, dt):
		self.count += 1

	def on_count(self, instance, value):
		print 'Clock Incremented: ', instance, value

	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			print 'Touched Count Widget at: ', touch.x, touch.y

class RootWidget(Widget):

	def a_function(self):
		print 'Doing Touch Down Function'
	
	def on_touch_move(self, touch):
		print touch.dx, touch.dy

class WidgetFunctionsApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    WidgetFunctionsApp().run()
