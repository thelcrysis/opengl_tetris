from Models.Model import *

import copy

class reverseL(Model):
    template = [(2,2),(2,1),(2,0),(1,0)]
    template_1 = [(0,1),(0,0),(1,0),(2,0)]
    template_2 = [(0,0),(0,1),(0,2),(1,2)]
    template_3 = [(0,2),(1,2),(2,2),(2,1)]
    templates = [template, template_1, template_2, template_3]

    
    def __init__(self, ll_x, ll_y):
        super().__init__(ll_x,ll_y)

        self.title = 'reverseL'

        self.template = reverseL.template
        self.template_1 = reverseL.template_1
        self.template_2 = reverseL.template_2
        self.template_3 = reverseL.template_3
        self.templates = reverseL.templates