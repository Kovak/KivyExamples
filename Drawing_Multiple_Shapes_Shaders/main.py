from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Mesh, RenderContext
from random import random
from kivy.core.image import Image
from kivy.uix.floatlayout import FloatLayout


class MultiQuadRenderer(Widget):

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'multiquad.glsl'
        super(MultiQuadRenderer, self).__init__(**kwargs) 
        self.draw_mesh_rectangle(20)

    def draw_mesh_rectangle(self, number):
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
            ('vTexCoords0', 2, 'float'),
            ('vRotation', 1, 'float'),
            ('vCenter', 2, 'float')
            ]
        indices = []
        for quad_n in xrange(len(star_list)):
            indices.append(0 + 4 * quad_n)
            indices.append(1 + 4 * quad_n)
            indices.append(2 + 4 * quad_n)
            indices.append(2 + 4 * quad_n)
            indices.append(3 + 4 * quad_n)
            indices.append(0 + 4 * quad_n)
        vertices = []
        for star in star_list:
            vertices += [
                -.5*star[2],
                -.5*star[2],
                0.0, 0.0, star[3], star[0], star[1],
                .5*star[2],
                -.5*star[2],
                1.0, 0.0, star[3], star[0], star[1],
                .5*star[2],
                .5*star[2],
                1.0, 1.0, star[3], star[0], star[1],
                -.5*star[2],
                .5*star[2],
                0.0, 1.0, star[3], star[0], star[1],
                ]
        with self.canvas:
            PushMatrix()
            self.mesh = Mesh(
                indices=indices,
                vertices=vertices,
                fmt=vertex_format,
                mode='triangles',
                texture=star_tex)
            PopMatrix()


class MultiQuadShaderApp(App):

    def build(self):
        root = FloatLayout()
        mq = MultiQuadRenderer(size=(800, 800))
        root.add_widget(mq)
        return root

if __name__ == '__main__':
    MultiQuadShaderApp().run()
