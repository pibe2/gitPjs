from mario1_1 import *
from GGlobals import *
from KoopaTroopa import KoopaTroopa


class RedKoopaTroopa(KoopaTroopa):
    def __init__(self, start_pos, end_pos, game):
        """
        start_post and end_pos are the boundaries for
        sprite's horizontal movement
        """
        super(RedKoopaTroopa, self).__init__(start_pos, game)

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

        # RedKoopaTroopa will move withing these bounds
        self.end_pos = end_pos

        self.init_rect()

    def update_x(self, dt):
        """ move forward if we hit our bounds then turn around """
        block_width, block_length = GameSpecs.BLOCK_SIZE

        dx = min(int(dt * self.rel_vx), block_width - 1)

        if self.xdir == Direction.RIGHT:
            self.rect.x = self.rect.x + dx
            if self.rect.x >= self.end_pos[0] and self.is_alive:
                self.rect.x = self.end_pos[0]
                self.xdir = not self.xdir
        else:
            self.rect.x = self.rect.x - dx
            if self.rect.x <= self.start_pos[0] and self.is_alive:
                self.rect.x = self.start_pos[0]
                self.xdir = not self.xdir
