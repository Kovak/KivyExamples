from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Mesh, RenderContext
from random import random, choice
from kivy.core.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.opengl import glEnable
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.graphics.opengl_utils import gl_get_version
from kivy.graphics.opengl import glEnable

class PointRenderer(Widget):
    shader_source = StringProperty('pointshader.glsl')

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = self.shader_source
        self.mesh = None
        super(PointRenderer, self).__init__(**kwargs) 
        self.generate_mesh_points(600)
        Clock.schedule_interval(self.test_mesh_remove, 1.0)

    def test_mesh_remove(self, dt):
        self.generate_mesh_points(600)

    def on_shader_source(self, instance, value):
        self.canvas.shader.source = value

    def generate_mesh_points(self, number):
        star_list = []
        w, h = self.size
        sa = star_list.append
        for number in xrange(number):
            rand_x = random()*w
            rand_y = random()*h
            size = 29.0
            color = (random(), random(), random(), random())
            rotation = random()*360.0
            sa((rand_x, rand_y, size, rotation, color))
        self.draw_mesh(star_list)

    def draw_mesh(self, star_list):
        address = 'assets/particles/'
        tex_choice = choice(['particle.png', 'smokeparticle.png', 
            'VFX-0-Circle.png', 'VFX-0-Star.png', 'VFX-1-Star.png'])
        tex = Image(address+tex_choice).texture
        vertex_format = [
            ('vPosition', 2, 'float'),
            ('vSize', 1, 'float'),
            ('vRotation', 1, 'float'),
            ('vColor', 4, 'float')
            ]
        indices = []
        ia = indices.append
        for star_number in range(len(star_list)):
            ia(star_number)
        vertices = []
        e = vertices.extend
        for star in star_list:
            color = star[4]
            e([
                star[0], star[1], star[2], star[3], 
                color[0], color[1], color[2], color[3]
                ])
        if self.mesh == None:
            with self.canvas:
                PushMatrix()
                self.mesh = Mesh(
                    indices=indices,
                    vertices=vertices,
                    fmt=vertex_format,
                    mode='points',
                    texture=tex)
                PopMatrix()
        else:
            self.mesh.indices = indices
            self.mesh.vertices = vertices
            self.mesh.texture = tex


class PointShaderApp(App):
    shader_path = StringProperty('assets/shaders/ES2/')

    def build(self):
        root = FloatLayout()
        mq = PointRenderer(size=(800, 800))
        root.add_widget(mq)
        gl_major, gl_minor = gl_get_version()
        if gl_major > 2 or (gl_major == 2 and gl_minor >= 1):
            glEnable(0x8642) #GL_VERTEX_PROGRAM_POINT_SIZE
            glEnable(0x8861) #GL_POINT_SPRITE
            self.shader_path = 'assets/shaders/GL/'
        return root

if __name__ == '__main__':
    PointShaderApp().run()
