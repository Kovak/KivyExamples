from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Quad, Translate, Rotate, RenderContext
from random import random
from kivy.core.image import Image
from kivy.uix.floatlayout import FloatLayout
import cProfile

class QuadRenderer(Widget):

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'multiquad.glsl'
        super(QuadRenderer, self).__init__(**kwargs) 
        self.draw_quads(6000)

    def draw_quads(self, number):
        star_list = []
        for number in xrange(number):
            rand_x = random()*self.size[0]
            rand_y = random()*self.size[1]
            size = 28.
            rotation = random()*360.
            star_list.append((rand_x, rand_y, size, rotation))
        self.draw_quad(star_list)

    def draw_quad(self, star_list):
        star_tex = Image('star1.png').texture
       
        with self.canvas:
            for star in star_list:
                size = .5*star[2]
                PushMatrix()
                t = Translate()
                r = Rotate()
                r.angle = star[3]
                Quad(texture = star_tex, points = (-size, 
                    -size, size, -size,
                    size, size, -size, size))
                t.xy = star[0], star[1]
                PopMatrix()


class QuadRendererApp(App):

    def build(self):
        root = FloatLayout()
        mq = QuadRenderer(size=(800, 800))
        root.add_widget(mq)
        return root

if __name__ == '__main__':
    #QuadRendererApp().run()
    cProfile.run('QuadRendererApp().run()', 'traditional_prof')