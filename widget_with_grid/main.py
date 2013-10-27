from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.graphics import Color, Line

class GridWidget(Widget):
	grid_spacing = NumericProperty(30.)
	'''Number of pixels between each grid line'''
	grid_line_width = NumericProperty(2.)
	'''Width of grid lines'''
	grid_line_color = ListProperty([1., 1., 1., 1.])
	'''Color of grid lines in RGBA'''
	grid_outline_color = ListProperty([1., 1., 1., 1.])
	'''color of line around grid'''
	grid_outline_width = NumericProperty(2.)
	'''width of grid outline'''
	grid_location = StringProperty('behind')
	'''location of grid lines, takes 'behind' or 'on_top' '''

	def __init__(self, **kwargs):
		super(GridWidget, self).__init__(**kwargs)
		self.draw_grid()

	def on_size(self, instance, value):
		self.canvas.before.clear()
		self.canvas.after.clear()
		self.draw_grid()


	def draw_grid(self):
		canvas = self.canvas.after
		if self.grid_location == 'behind':
			canvas = self.canvas.before
		width = self.size[0]
		height = self.size[1]
		iters = 0
		grid_spacing = self.grid_spacing
		#draw grid interior
		with canvas:
			Color(rgba=self.grid_line_color)
			while width > grid_spacing:
				
				Line(width=self.grid_line_width,
					points=(self.pos[0] + iters*grid_spacing, 
						self.pos[1], 
						self.pos[0] + iters*grid_spacing, 
						self.pos[1] + self.size[1]))
				width -= grid_spacing
				iters += 1
			iters = 0
			while height > grid_spacing:
				Line(width=self.grid_line_width,
					points=(self.pos[0], 
						self.pos[1] + iters*grid_spacing, 
						self.pos[0] + self.size[0], 
						self.pos[1] + iters*grid_spacing))
				height -= grid_spacing
				iters += 1
		#draw grid outline
		with self.canvas.after:
			Color(self.grid_outline_color)
			Line(width=self.grid_outline_width, 
				rectangle=(self.pos[0], self.pos[1], 
				self.size[0], self.size[1]))


class GridWidgetApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    GridWidgetApp().run()
