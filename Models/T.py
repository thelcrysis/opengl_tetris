from Models.Model import *

import copy

class T(Model):
    template = [(0,0),(1,0),(2,0),(1,1)]
    template_1 = [(0,0),(0,1),(0,2),(1,1)]
    template_2 = [(0,2),(1,2),(2,2),(1,1)]
    template_3 = [(2,0),(2,1),(2,2),(1,1)]
    templates = [template, template_1, template_2, template_3]

    
    def __init__(self, ll_x, ll_y):
        super().__init__(ll_x,ll_y)

        self.title = 'T'

        self.template = T.template
        self.template_1 = T.template_1
        self.template_2 = T.template_2
        self.template_3 = T.template_3
        self.templates = T.templates