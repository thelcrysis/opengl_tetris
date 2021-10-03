from Models.Model import *

import copy

class I(Model):
    template = [(0,0),(0,1),(0,2),(0,3)]
    template_1 = [(-1,1),(0,1),(1,1),(2,1)]
    template_2 = [(0,0),(0,1),(0,2),(0,3)]
    template_3 = [(-1,1),(0,1),(1,1),(2,1)]
    templates = [template, template_1, template_2, template_3]

    
    def __init__(self, ll_x, ll_y):
        super().__init__(ll_x,ll_y)

        self.title = 'I'
        
        self.template = I.template
        self.template_1 = I.template_1
        self.template_2 = I.template_2
        self.template_3 = I.template_3
        self.templates = I.templates