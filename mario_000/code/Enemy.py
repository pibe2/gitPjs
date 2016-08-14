from mario1_1 import *
from GGlobals import *
from AutoPilotSprite import *


class Enemy(AutoPilotSprite):
    def __init__(self, start_pos, game):
        super(Enemy, self).__init__(start_pos, game)
        self.join_sprite_group(game.enemy_sprites)

        self.got_stepped_on_imgs = None
        self.got_shot_img = None
        self.prev_imgs = [None, None, None, None, None, None, None, None]

        self.xdir = Direction.LEFT
        self.y_collide_offset = 0

        self.got_stepped_on = False
        self.got_shot = False
        self.stomped_score_value = 100
        self.shot_score_value = 200

    def get_collision_rect(self):
        """
        gets the collision-rect that the player pixie collides
        with (allows us to ignore the head and jump on the shell)
        """
        rect = self.rect
        pos = rect.x, rect.y + self.y_collide_offset
        size = rect.width, rect.height - self.y_collide_offset
        return pygame.Rect(pos, size)

    def get_prev_collision_rect(self):
        """
        used with get_player_collitiderect() to determine collision
        with player (allows us to ignore the head and jump on the shell)
        """
        rect = self.prev_rect
        pos = rect.x, rect.y + self.y_collide_offset
        size = rect.width, rect.height - self.y_collide_offset
        return pygame.Rect(pos, size)

    def init_stepped_death(self):
        """
        triggered when player jumps on shell
        increases its velocity and turns into just a shell.
        """
        if self.is_alive:
            self.is_alive = 0
            self.got_stepped_on = True
            self.rel_vx = 0

            self.change_to_stepped_on_image_rect()

    def change_to_stepped_on_image_rect(self):
        prev_bottom = self.rect.bottom
        self.rect.size = self.got_stepped_on_imgs[0].get_size()
        self.rect.bottom = prev_bottom

    def init_shot_death(self, bullet_xdir):
        """
        triggered when hit by a fireball
        """
        if self.is_alive:
            self.xdir = bullet_xdir
            self.is_alive = 0
            self.got_shot = True

    def update(self, dt):
        """
        when turtle gets shot, we don't worry about collisions
        """
        if self.is_dead:
            self.kill()
        self.prev_rect = self.rect.copy()
        self.update_x(dt)
        if not self.got_shot:
            self.handle_xcollisions_with_expanded_rect(
                                self.game.block_sprites,
                                self.left_block_collision_handler,
                                self.right_block_collision_handler)
        self.update_y(dt)
        if not self.got_shot:
            hit_top, hit_bottom = self.handle_ycollisions_with_expanded_rect(
                                                        self.game.block_sprites,
                                                        self.top_block_collision_handler,
                                                        self.bottom_block_collision_handler)
            self.update_float_status(hit_top)
        self.check_bounds()
        self.animate()

    def animate(self):
        """
        assigns its image every frame;
        a shell when self.is_alive is false.
        """
        if self.got_stepped_on:
            self.update_image(self.got_stepped_on_imgs[self.xdir])
            return
        elif self.got_shot:
            self.update_image(self.got_shot_img)
            return
        else:
            valid_imgs = self.horiz_move_imgs[self.xdir]

            self.update_image_from_series(valid_imgs)