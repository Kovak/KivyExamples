'''
Base for a particle engine using GLSL for computation
=====================================================

.. author:: Mathieu Virbel
.. status:: WIP

Particle position is between 0..2048
Particle velocity is between -1024..1024
Both are stored into 16 bits unsigned integer.

POC Summary:

- precision is critical, and bundling both X and Y in 16 bits doesn't give
  enough precision. Or at least, i'm not able to do correctly the calculation.
  -> we need a pass for X, and a pass for Y
- remember that we can't get more than 65535 indices in GLES2. Means we would
  need multiples meshes
- update_mesh() is a demo, but we should find a way to do it in glsl too, as
  dump is _slow_, due to glReadPixels.

'''

from struct import pack, unpack
from random import random
from kivy.graphics import Rectangle, BindTexture, Color, \
        ClearColor, ClearBuffers, Mesh
from kivy.graphics.fbo import Fbo
from kivy.graphics.texture import Texture
from kivy.graphics.opengl import glEnable, glDisable, GL_BLEND

# Shaders utilities for convertion
FS_UTILS = '''
float u16tof(vec2 v) {
    // convert vec2/16 bits to 0-65535. float
    return (v.x * 255.) + (v.y * 255.) * 256.;
}

vec2 ftou16(float v) {
    // convert 0-65535. float to vec2/16 bits
    float high_x = v / 256.;
    float low_x = v - (high_x * 256.);
    return vec2(low_x / 255., high_x / 255.);
}

'''

# Pass 1: shader that update the position according to the velocity
FS_P1 = FS_UTILS + '''
$HEADER$
uniform float dt;
uniform sampler2D texture_vel;

void main(void) {
    vec4 pos = texture2D(texture0, tex_coord0);
    vec4 vel = texture2D(texture_vel, tex_coord0);
    float px = u16tof(pos.xy);
    float py = u16tof(pos.zw);
    float vx = u16tof(vel.xy) - 32768.;
    float vy = u16tof(vel.zw) - 32768.;

    vec2 x = ftou16(px + vx * dt);
    vec2 y = ftou16(py + vy * dt);
    gl_FragColor = vec4(x, y);
}
'''

# Pass 2: shader that reduce the velocity
FS_P2 = FS_UTILS + '''
$HEADER$
uniform float dt;

void main(void) {
    vec4 vel = texture2D(texture0, tex_coord0);
    float vx = u16tof(vel.xy);
    float vy = u16tof(vel.zw);
    vx = (vx - 32767.) / 32.;
    vy = (vy - 32767.) / 32.;
    vx = vx / (1.1 * dt);
    vy = vy / (1.1 * dt);
    vx = (vx * 32.) + 32767.;
    vy = (vy * 32.) + 32767.;
    gl_FragColor = vec4(ftou16(vx), ftou16(vy));
}
'''


class GlslParticle(object):

    def __init__(self, texsize):
        super(GlslParticle, self).__init__()
        self.texsize = texsize
        self.initialize_particles()
        self.initialize_fbos()

    def initialize_particles(self):
        # position (x, y) and velocity (vx, vy) are set on 16 bits.
        # value is fitted into [0..2048] range, with 0.03 px precision
        texsize = self.texsize
        datasize = texsize ** 2

        # initialize positions to be x = y = 1024
        v = [32768 for x in xrange(datasize * 2)]
        self.particles_pos = pack('H' * datasize * 2, *v)

        # initialize velocity to be random, 1024 == 0
        v = [int((random() - 0.5) * 32 + 1024) * 32 for x in xrange(datasize * 2)]
        print [x / 32. - 1024 for x in  v[:2] ]
        self.particles_vel = pack('H' * datasize * 2, *v)

        # create textures
        self.tex_pos = self._create_texture(self.particles_pos)
        self.tex_vel = self._create_texture(self.particles_vel)
        self.tex_pos2 = self._create_texture('\x00' * datasize * 4)
        self.tex_vel2 = self._create_texture('\x00' * datasize * 4)

        self.fbo_pos = Fbo(texture=self.tex_pos, size=self.tex_pos.size)
        self.fbo_vel = Fbo(texture=self.tex_vel, size=self.tex_vel.size)
        self.fbo_pos2 = Fbo(texture=self.tex_pos2, size=self.tex_pos2.size)
        self.fbo_vel2 = Fbo(texture=self.tex_vel2, size=self.tex_vel2.size)

    def initialize_fbos(self):
        texsize = self.texsize
        size = (texsize, texsize)

        # pass 1, update position
        # both fbo have the associated texture as destination, and other fbo
        # texture as source.
        for fbo in (self.fbo_pos, self.fbo_pos2):
            fbo.shader.fs = FS_P1
            #self._print_shader(fbo.shader.fs)
            other_fbo = self.fbo_pos2 if fbo is self.fbo_pos else self.fbo_pos
            other_vel_fbo = self.fbo_vel2 if fbo is self.fbo_pos else self.fbo_vel
            with fbo:
                ClearColor(0, 0, 0, 0)
                ClearBuffers()
                BindTexture(texture=other_vel_fbo.texture, index=1)
                Rectangle(size=size, texture=other_fbo.texture)

        # pass 2, reduce velocity
        for fbo in (self.fbo_vel, self.fbo_vel2):
            fbo.shader.fs = FS_P2
            other_fbo = self.fbo_vel2 if fbo is self.fbo_vel else self.fbo_vel
            with fbo:
                ClearColor(0, 0, 0, 0)
                ClearBuffers()
                Rectangle(size=size, texture=other_fbo.texture)

    def iterate(self, dt):
        glDisable(GL_BLEND)

        # pass 1
        fbo = self.fbo_pos2
        fbo['texture_vel'] = 1
        fbo['dt'] = dt
        fbo.ask_update()
        fbo.draw()

        # pass 2
        fbo = self.fbo_vel2
        fbo['dt'] = dt
        fbo.ask_update()
        fbo.draw()

        glEnable(GL_BLEND)

        # switch the texture for the next run
        self.fbo_pos, self.fbo_pos2 = self.fbo_pos2, self.fbo_pos
        self.fbo_vel, self.fbo_vel2 = self.fbo_vel2, self.fbo_vel

    def dump(self, count):
        print '-- [ dump ] --------------------------------------------'
        datasize = self.texsize ** 2

        rawpos = unpack('HH' * datasize, self.fbo_pos.pixels)
        pos = [v / 32. for v in rawpos]

        rawvel = unpack('HH' * datasize, self.fbo_vel.pixels)
        vel = [v / 32. - 1024 for v in rawvel]

        for index in xrange(min(count, datasize)):
            print 'particle {}: pos=({:>6}, {:>6}) vel=({:>6}, {:>6})'.format(
                    index,
                    pos[index * 2],
                    pos[index * 2 + 1],
                    vel[index * 2],
                    vel[index * 2 + 1])

    def update_mesh(self, mesh):
        datasize = self.texsize ** 2
        rawpos = unpack('HH' * datasize, self.fbo_pos.pixels)
        # manually center on a 640x480 screen
        mesh.vertices = [(v / 32.) - 1024 + 320 for v in rawpos]
        mesh.indices = range(datasize)

    def _create_texture(self, data):
        texsize = self.texsize
        tex = Texture.create(size=(texsize, texsize), colorfmt='rgba')
        tex.blit_buffer(data, colorfmt='rgba')
        return tex

    def _print_shader(self, text):
        for index, line in enumerate(text.splitlines()):
            print index, line


if __name__ == '__main__':
    from kivy.uix.widget import Widget
    from kivy.clock import Clock
    from kivy.base import runTouchApp

    class TestWidget(Widget):
        def __init__(self, **kwargs):
            super(TestWidget, self).__init__()
            self.engine = e = GlslParticle(64)
            Clock.schedule_interval(self.iterate, 0)
            with self.canvas:
                Color(1, 1, 1, 1)
                Rectangle(pos=(0, 0), size=(100, 100), texture=e.tex_pos)
                Rectangle(pos=(100, 0), size=(100, 100), texture=e.tex_pos2)
                Rectangle(pos=(0, 100), size=(100, 100), texture=e.tex_vel)
                Rectangle(pos=(100, 100), size=(100, 100), texture=e.tex_vel2)
                self.mesh = Mesh(mode='points')


        def iterate(self, dt):
            self.engine.iterate(1.)
            self.engine.dump(5)
            self.engine.update_mesh(self.mesh)
            self.canvas.ask_update()

    runTouchApp(TestWidget())

    '''
    engine = GlslParticle(4)
    for x in xrange(4):
        engine.iterate(1 / 60.)
        engine.dump(1)
    '''
