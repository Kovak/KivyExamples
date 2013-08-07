from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class RootWidget(Widget):
    pass

class CustomButton(Button):
	
	def reset_animation(self, animation, widget):
		self.button_anim_2.start(self)

class OverridingStyleApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    OverridingStyleApp().run()
