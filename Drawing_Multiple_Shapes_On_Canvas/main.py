from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Rotate, Translate, PushMatrix, PopMatrix
from random import random, choice


class RootWidget(Widget):

    def choose_star(self):
        star_choices = [('star1.png', 28), ('star2.png', 16)]
        return choice(star_choices)
    
    def draw_stars_simple(self, number):
        with self.canvas.before:
            for number in xrange(number):
                star_choice = self.choose_star()
                rand_x = random()*self.width
                rand_y = random()*self.height
                Rectangle(source=star_choice[0], size=(star_choice[1], 
                    star_choice[1]), pos=(rand_x, rand_y))

    def draw_stars_with_rotate(self, number):
        with self.canvas.before:
            for number in xrange(number):
                PushMatrix()
                star_choice = self.choose_star()
                rand_x = random()*self.width
                rand_y = random()*self.height
                rand_angle = random()*360
                Translate(rand_x, rand_y)
                Rotate(angle=rand_angle)
                Rectangle(source=star_choice[0], 
                    size=(star_choice[1], star_choice[1]), 
                    pos=(-star_choice[1]/2., -star_choice[1]/2.))
                PopMatrix()

    def draw_stars(self, draw_type):
        self.canvas.before.clear()
        number_stars = int(random()*100)
        if draw_type == 'simple':
            self.draw_stars_simple(number_stars)
        elif draw_type == 'rotate':
            self.draw_stars_with_rotate(number_stars)


class MultipleShapesCanvasApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    MultipleShapesCanvasApp().run()
