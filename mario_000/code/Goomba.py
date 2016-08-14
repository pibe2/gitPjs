from mario1_1 import *
from GGlobals import *
from Enemy import Enemy


class Goomba(Enemy):
    def __init__(self, start_pos, game):
        super(Goomba, self).__init__(start_pos, game)

        run_left_img = pygame.image.load('../images/furballwalk1.png').convert_alpha()
        run_right_img = pygame.transform.flip(run_left_img, True, False)
        walk_left_img = pygame.image.load('../images/furballwalk2.png').convert_alpha()
        walk_right_img = pygame.transform.flip(walk_left_img, True, False)
        flat_img = pygame.image.load('../images/furballflat.png').convert_alpha()

        self.horiz_move_imgs = [[walk_left_img, run_left_img], [walk_right_img, run_right_img]]
        self.image = walk_left_img
        self.got_stepped_on_imgs = [flat_img, flat_img]
        self.got_shot_img = pygame.transform.flip(run_left_img, False, True)

        self.init_rect()
