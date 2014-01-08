from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Mesh, RenderContext
from random import random
from kivy.core.image import Image
from kivy.uix.floatlayout import FloatLayout
import cProfile
from kivy.graphics.opengl import glEnable
from kivy.clock import Clock

class PointRenderer(Widget):

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'pointshader.glsl'
        glEnable(0x8642) #GL_VERTEX_PROGRAM_POINT_SIZE
        glEnable(0x8861) #GL_POINT_SPRITE
        self.mesh = None
        super(PointRenderer, self).__init__(**kwargs) 
        self.draw_mesh_points(60)
        Clock.schedule_interval(self.test_mesh_remove, 1./60.)

    def test_mesh_remove(self, dt):
        
        r = random()
        if r > .5:
            self.canvas.remove(self.mesh)
            self.mesh = None
        self.draw_mesh_points(60)


    def draw_mesh_points(self, number):
        star_list = []
        w, h = self.size
        sa = star_list.append
        for number in xrange(number):
            rand_x = random()*w
            rand_y = random()*h
            size = 29.0
            rotation = random()*360.0
            sa((rand_x, rand_y, size, rotation))
        self.draw_mesh(star_list)


    def draw_mesh(self, star_list):
        star_tex = Image('star1.png').texture
        vertex_format = [
            ('vPosition', 2, 'float'),
            ('vSize', 1, 'float'),
            ('vRotation', 1, 'float'),
            ]
        indices = []
        ia = indices.append
        for star_number in range(len(star_list)):
            ia(star_number)
        vertices = []
        e = vertices.extend
        for star in star_list:
            e([
                star[0], star[1], star[2], star[3]
                ])
        if self.mesh == None:
            with self.canvas:
                PushMatrix()
                self.mesh = Mesh(
                    indices=indices,
                    vertices=vertices,
                    fmt=vertex_format,
                    mode='points',
                    texture=star_tex)
                PopMatrix()
        else:
            self.mesh.indices = indices
            self.mesh.vertices = vertices


class PointShaderApp(App):

    def build(self):
        root = FloatLayout()
        mq = PointRenderer(size=(800, 800))
        root.add_widget(mq)
        return root

if __name__ == '__main__':
    #MultiQuadShaderApp().run()
    cProfile.run('PointShaderApp().run()', 'point_prof')