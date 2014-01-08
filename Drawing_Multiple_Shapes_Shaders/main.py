from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Mesh, RenderContext
from random import random, choice
from kivy.core.image import Image
from kivy.uix.floatlayout import FloatLayout
import cProfile
from kivy.atlas import Atlas
import json


class MultiQuadRenderer(Widget):

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'multiquad.glsl'
        super(MultiQuadRenderer, self).__init__(**kwargs) 
        self.draw_mesh_rectangle(20)
        self.draw_mesh_rectangle(200)

    def draw_mesh_rectangle(self, number):
        star_list = []
        w, h = self.size
        for number in xrange(number):
            rand_x = random()*w
            rand_y = random()*h
            rotation = random()*360.
            star_list.append((rand_x, rand_y, rotation))
        self.draw_mesh(star_list)

    def return_uv_coordinates(self, atlas_name, atlas_page, atlas_size):
        w, h = atlas_size
        with open(atlas_name, 'r') as fd:
            atlas_data = json.load(fd)
        atlas_content = atlas_data[atlas_page]
        uv_dict = {}
        for texture_name in atlas_content:
            data = atlas_content[texture_name]
            x1, y1 = data[0], data[1]
            x2, y2 = x1 + data[2], y1 + data[3]
            uv_dict[texture_name] = x1/w, 1.-y1/h, x2/w, 1.-y2/h, data[2], data[3]
        return uv_dict

    def draw_mesh(self, star_list):
        filename = 'background_objects.atlas'
        star_tex = Image('background_objects-0.png').texture
        size_tex = (float(star_tex.size[0]), float(star_tex.size[1]))
        uv_dict = self.return_uv_coordinates(filename, 'background_objects-0.png', size_tex)
        choices = [x for x in uv_dict]
        vertex_format = [
            ('vPosition', 2, 'float'),
            ('vTexCoords0', 2, 'float'),
            ('vRotation', 1, 'float'),
            ('vCenter', 2, 'float')
            ]
        indices = []
        ie = indices.extend
        for quad_n in xrange(len(star_list)):
            offset = 4 * quad_n
            ie([0 + offset, 1 + offset, 
                2 + offset, 2 + offset,
                3 + offset, 0 + offset])
        vertices = []
        e = vertices.extend
        for star in star_list:
            tex_choice = choice(choices)
            uv = uv_dict[tex_choice]
            w, h = uv[4], uv[5]
            x0, y0 = uv[0], uv[1]
            x1, y1 = uv[2], uv[3]
            e([
                -w, -h,
                x0, y0, star[2], star[0], star[1],
                w, -h,
                x1, y0, star[2], star[0], star[1],
                w, h,
                x1, y1, star[2], star[0], star[1],
                -w, h,
                x0, y1, star[2], star[0], star[1],
                ])
        with self.canvas:
            self.mesh = Mesh(
                indices=indices,
                vertices=vertices,
                fmt=vertex_format,
                mode='triangles',
                texture=star_tex)



class MultiQuadShaderApp(App):

    def build(self):
        root = FloatLayout()
        mq = MultiQuadRenderer(size=(800, 800))
        root.add_widget(mq)
        return root

if __name__ == '__main__':
    #MultiQuadShaderApp().run()
    cProfile.run('MultiQuadShaderApp().run()', 'shader_prof')