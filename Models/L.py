from Models.Model import *

import copy

class L(Model):
    template = [(0,0),(0,1),(0,2),(1,0)]
    template_1 = [(0,1),(0,2),(1,2),(2,2)]
    template_2 = [(1,2),(2,2),(2,1),(2,0)]
    template_3 = [(2,1),(2,0),(1,0),(0,0)]
    templates = [template, template_1, template_2, template_3]

    def __init__(self,ll_x,ll_y) -> None:
        #ll_x - most left lower piece x coordinate 
        super().__init__(ll_x,ll_y)
        
        self.title = 'L'

        self.template = L.template
        self.template_1 = L.template_1
        self.template_2 = L.template_2
        self.template_3 = L.template_3
        self.templates = L.templates