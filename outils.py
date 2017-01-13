#!/usr/bin/env python
import math
import random

def random_color(min=0, max=255):
    return (
        int(random.randrange(min,max)),
        int(random.randrange(min,max)),
        int(random.randrange(min,max))
        )


def random_rgb(min_lum=0.5, alpha = 1):
    a,b,c = [random.random() for x in range(3) ]

    while a+b+c < 1.5 :
        a = min(1,a*1.2)
        b = min(1,b*1.2)
        c = min(1,c*1.2)
    return [a,b,c, alpha]

def random_vector(scale = 1):
    rand_angle=random.random()*math.pi*2
    rand_mag = random.random() * scale
    return [math.cos(rand_angle)*rand_mag,math.sin(rand_angle)*rand_mag]
