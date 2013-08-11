from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty

class DeleteButton(Button):
	rectangle_size_x = NumericProperty(100)

class RootWidget(Widget):
    
    def delete_button_remove_widget(self, widget):
    	self.b_layout2.remove_widget(widget)

class DeleteSlideButton(Button):
	delete_button = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(DeleteSlideButton, self).__init__(**kwargs)
		self.delete_button = DeleteButton()

	def on_size(self, instance, value):
		if not self.delete_button.parent:
			self.delete_button.rectangle_size_x = value[0]

	def on_touch_move(self, touch):
		if self.collide_point(touch.x, touch.y):
			if touch.dx < -40:
				if not self.delete_button.parent:
					self.b_layout.add_widget(self.delete_button)
					self.delete_button.button_anim_1.start(self.delete_button)

	def button_pressed(self):
		print 'button pressed: ', self


class IOSDeleteButtonApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    IOSDeleteButtonApp().run()
