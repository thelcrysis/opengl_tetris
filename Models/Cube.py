from Models.Model import *

import copy

class Cube(Model):
    template = [(0,0),(0,1),(1,0),(1,1)]
    template_1 = [(0,0),(0,1),(1,0),(1,1)]
    template_2 = [(0,0),(0,1),(1,0),(1,1)]
    template_3 = [(0,0),(0,1),(1,0),(1,1)]
    templates = [template, template_1, template_2, template_3]

    
    def __init__(self, ll_x, ll_y):
        super().__init__(ll_x,ll_y)

        self.title = 'cube'

        self.template = Cube.template
        self.template_1 = Cube.template_1
        self.template_2 = Cube.template_2
        self.template_3 = Cube.template_3
        self.templates = Cube.templates