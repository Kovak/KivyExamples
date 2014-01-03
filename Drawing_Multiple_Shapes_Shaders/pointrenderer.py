from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Mesh, RenderContext
from random import random
from kivy.core.image import Image
from kivy.uix.floatlayout import FloatLayout
import cProfile

class PointRenderer(Widget):

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'pointshader.glsl'
        super(PointRenderer, self).__init__(**kwargs) 
        self.draw_mesh_points(6000)

    def draw_mesh_points(self, number):
        star_list = []
        for number in xrange(number):
            rand_x = random()*self.size[0]
            rand_y = random()*self.size[1]
            size = 28.
            rotation = random()*360.
            star_list.append((rand_x, rand_y, size, rotation))
        self.draw_mesh(star_list)

    def draw_mesh(self, star_list):
        star_tex = Image('star1.png').texture
        vertex_format = [
            ('vPosition', 2, 'float'),
            ('vSize', 1, 'float'),
            ('vRotation', 1, 'float'),
            ]
        indices = []
        for star_number in xrange(len(star_list)):
            indices.append(star_number)
        vertices = []
        for star in star_list:
            vertices += [
                star[0], star[1], star[2], star[3]
                ]
        with self.canvas:
            PushMatrix()
            self.mesh = Mesh(
                indices=indices,
                vertices=vertices,
                fmt=vertex_format,
                mode='points',
                texture=star_tex)
            PopMatrix()


class PointShaderApp(App):

    def build(self):
        root = FloatLayout()
        mq = PointRenderer(size=(800, 800))
        root.add_widget(mq)
        return root

if __name__ == '__main__':
    #MultiQuadShaderApp().run()
    cProfile.run('PointShaderApp().run()', 'point_prof')