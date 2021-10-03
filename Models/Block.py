class Block:
    def __init__(self,x,y) -> None:
        #defined by lower left vertex
        self.x = x
        self.y = y
        self.vertices = Block.generate_vertices(self.x, self.y)

    def generate_vertices(x,y):
        vertices = {"down_l":(x,y),
                      "up_l":(x,y+1),
                    "down_r":(x+1,y),
                      "up_r":(x+1,y+1)}
        return vertices

    def translate(self, delta_x, delta_y):
        # Generates a block's translated by delta_x and delta_y 
        self.x += delta_x
        self.y += delta_y
        self.vertices = Block.generate_vertices(self.x, self.y)
        
    def __repr__(self) -> str:
        return self.vertices.__repr__()

    def __str__(self) -> str:
        return '(' + str(self.x) + ',' + str(self.y) + ')'