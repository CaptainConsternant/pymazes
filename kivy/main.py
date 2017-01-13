#!/usr/bin/env python
"""
Bouncing balls
"""


from random import random

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.core.window import Window
from outils import random_vector, random_rgb

from kivy.uix.scatterlayout import ScatterLayout


DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 100.0
ALPHA = 0.7

class Ball(Widget):
    """Class for bouncing ball."""
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    col= ListProperty([1,1,1,ALPHA])
    def __init__(self, *args, **kwargs):
        super(Ball, self).__init__(*args, **kwargs)
        self.col= random_rgb(alpha=ALPHA)


    def update(self, dt):
        self.pos = Vector(*self.velocity) * dt + self.pos

    def change_color(self):
        self.col= random_rgb(alpha=ALPHA)





class BallsContainer(Widget):
    """Class for balls container, a main widget."""
    def __init__(self, *args, **kwargs):
        super(BallsContainer, self).__init__(*args, **kwargs)
        # import pdb; pdb.set_trace()
        for i in range(50) :
            ball = Ball()
            ball.pos = (Window.width/2,Window.height/2)
            ball.velocity = random_vector(MAX_BALL_SPEED)

            # ball.col= random_rgb(alpha=ALPHA)
            self.add_widget(ball)

    def update(self, dt):
        balls = (c for c in self.children if isinstance(c, Ball))
        for ball in balls:
            ball.update(dt)

            # bounce of walls
            # (note: Y axis is pointing *up*)
            if ball.x < 0 or ball.right > self.width:
                ball.velocity_x *= -1
            if ball.y < 0 or ball.top > self.height:
                ball.velocity_y *= -1

    def on_touch_up(self, touch):
        """Touch (or click) 'up' event: releasing the mouse button
        or lifting finger.
        """
        ball = Ball()
        ball.center = (touch.x, touch.y)
        ball.velocity = random_vector(MAX_BALL_SPEED)
        self.add_widget(ball)

        balls = (c for c in self.children if isinstance(c, Ball))
        for ball in balls:
            ball.change_color()


class BallsApp(App):
    """Represents the whole application."""

    def build(self):
        """Entry point for creating app's UI."""
        scat = ScatterLayout()
        bc=BallsContainer()
        scat.add_widget(bc)
        Clock.schedule_interval(bc.update, DELTA_TIME)
        # return bc
        return scat


if __name__ == '__main__':
    BallsApp().run()
