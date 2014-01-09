from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Mesh, RenderContext, Line, Color
from kivy.uix.floatlayout import FloatLayout
from kivy.vector import Vector
from math import fabs
from kivy.properties import ListProperty, NumericProperty

class NiceLineRenderer(Widget):
    points = ListProperty([])
    tolerance = NumericProperty(1.0)
    line_color = ListProperty([1.0, 0., 0.0, 1.0])
    regular_line_offset = ListProperty([100, 100])
    regular_points = ListProperty([])
    line_width = NumericProperty(5.)

    def __init__(self, other_widget, **kwargs):
        self.other_widget = other_widget
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'niceline.glsl'
        super(NiceLineRenderer, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        self.points = []
        self.regular_points = []
        offset = self.regular_line_offset
        self.points.append((touch.x, touch.y))
        self.regular_points.append(touch.x + offset[0])
        self.regular_points.append(touch.y + offset[1])

    def on_touch_move(self, touch):
        offset = self.regular_line_offset
        width = self.line_width
        if fabs(touch.dx) + fabs(touch.dy) >= self.tolerance:
            self.points.append((touch.x, touch.y))
            self.regular_points.append(touch.x + offset[0])
            self.regular_points.append(touch.y + offset[1])
            self.draw_line(self.points, width=width)
            self.draw_regular_line(self.regular_points, width=width/4.)

    def on_touch_up(self, touch):
        offset = self.regular_line_offset
        width = self.line_width
        self.points.append((touch.x, touch.y))
        self.regular_points.append(touch.x + offset[0])
        self.regular_points.append(touch.y + offset[1])
        self.draw_line(self.points, width=width)
        self.draw_regular_line(self.regular_points, width=width/4.)

    def draw_regular_line(self, points_list, width=5.):
        line_color = self.line_color
        with self.other_widget.canvas:
            self.color = Color(line_color[0], line_color[1], line_color[2], line_color[3])
            self.line = Line(points=points_list, width=width)

    def draw_line(self, points_list, width=5.):
        vertex_format = [
            ('vPosition', 2, 'float'),
            ('vdxdy', 2, 'float'),
            ('vWidth', 1, 'float'),
            ('vColor', 4, 'float')
            ]
        indices = []
        ie = indices.extend
        vertices = []
        e = vertices.extend
        line_color = self.line_color
        for numpoint in range(len(points_list)-1):
            point1 = points_list[numpoint]
            point2 = points_list[numpoint+1]
            dx = point2[0] - point1[0]
            dy = point2[1] - point1[1]
            a = Vector(dx, dy).normalize()
            if numpoint == 0:
                ie([0, 5, 3, 
                    3, 1, 0,
                    5, 0, 2, 
                    2, 4, 5])
                e([
                    point1[0], point1[1], 0.0, 0.0,
                    width, line_color[0], line_color[1], line_color[2], line_color[3],
                    point1[0], point1[1], a[0], -a[1],
                    width, 0.0, 0.0, 0.0, 0.0,
                    point1[0], point1[1], -a[0], a[1],
                    width, 0.0, 0.0, 0.0, 0.0,
                    point2[0], point2[1], a[0], -a[1],
                    width, 0.0, 0.0, 0.0, 0.0,
                    point2[0], point2[1], -a[0], a[1],
                    width, 0.0, 0.0, 0.0, 0.0,
                    point2[0], point2[1], 0.0, 0.0,
                    width, line_color[0], line_color[1], line_color[2], line_color[3],
                    ])
            else:
                offset = 5 + (numpoint-1)*3
                ie([offset, offset+3, offset+1,
                    offset+1, offset-2, offset,
                    offset+3, offset, offset-1,
                    offset-1, offset+2, offset+3])
                e([
                    point2[0], point2[1], a[0], -a[1],
                    width, 0.0, 0.0, 0.0, 0.0,
                    point2[0], point2[1], -a[0], a[1],
                    width, 0.0, 0.0, 0.0, 0.0,
                    point2[0], point2[1], 0.0, 0.0,
                    width, line_color[0], line_color[1], line_color[2], line_color[3],
                    ])

        with self.canvas:
            self.mesh = Mesh(
                indices=indices,
                vertices=vertices,
                fmt=vertex_format,
                mode='triangles',)


class NiceLineShaderApp(App):

    def build(self):
        root = FloatLayout()
        other_widget = Widget()
        mq = NiceLineRenderer(other_widget, size=(800, 800))
        root.add_widget(other_widget)
        root.add_widget(mq)
        return root

if __name__ == '__main__':
    NiceLineShaderApp().run()
