#!/usr/bin/env python
import math
import random

def random_color(min=0, max=255):
    return (
        int(random.randrange(min,max)),
        int(random.randrange(min,max)),
        int(random.randrange(min,max))
        )

def random_vector(scale = 1):
    rand_angle=random.random()*math.pi*2
    rand_mag = random.random() * scale
    return [math.cos(rand_angle)*rand_mag,math.sin(rand_angle)*rand_mag]
