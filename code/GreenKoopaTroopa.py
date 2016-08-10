from mario1_1 import *
from GGlobals import *
from KoopaTroopa import KoopaTroopa


# TODO: Change behavior so that it just wanders without a start_pos and an end_pos
# TODO: when live enemy is stomped on, turns into a stationary shell, shell's
#   TODO: movement can be toggled by additional stomping
#   TODO: shooting a shell kills it
#   TODO: moving shell kills on hit, moving shells cancel each other
#   TODO: not affected by left and right boundary walls; can fall to death off world edge
# TODO: IMPLEMENT FURBALL ENEMY
class GreenKoopaTroopa(KoopaTroopa):
    def __init__(self, start_pos, game):
        super(GreenKoopaTroopa, self).__init__(start_pos, game)

        run_left_img = pygame.image.load('../images/turtlewalk1_left.png').convert_alpha()
        run_right_img = pygame.transform.flip(run_left_img, True, False)
        walk_left_img = pygame.image.load('../images/turtlewalk2_left.png').convert_alpha()
        walk_right_img = pygame.transform.flip(walk_left_img, True, False)
        shell_left_img = pygame.image.load('../images/turtleshell_left.png').convert_alpha()
        shell_right_img = pygame.transform.flip(shell_left_img, True, False)

        self.horiz_move_imgs = [[walk_left_img, run_left_img], [walk_right_img, run_right_img]]
        self.image = walk_left_img
        self.got_stepped_on_imgs = [shell_left_img, shell_right_img]
        self.got_shot_img = pygame.transform.flip(shell_left_img, False, True)

        self.init_rect()
