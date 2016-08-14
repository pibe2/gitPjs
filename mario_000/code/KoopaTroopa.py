from mario1_1 import *
from GGlobals import *
from Enemy import Enemy


class KoopaTroopa(Enemy):
    def __init__(self, start_pos, game):
        super(KoopaTroopa, self).__init__(start_pos, game)
        self.y_collide_offset = 56
