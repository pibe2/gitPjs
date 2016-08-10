import pygame
from GGlobals import *
from AutoPilotSprite import AutoPilotSprite


class FireBall(AutoPilotSprite):
    def __init__(self, position, xdir, game):
        super(FireBall, self).__init__(position, game)
        self.join_sprite_group(game.fireball_sprites)

        img_angle1 = pygame.image.load("../images/fireball.png").convert_alpha()
        img_angle2 = pygame.transform.rotate(img_angle1, 120)
        img_angle3 = pygame.transform.rotate(img_angle2, 120)
        explode_img1 = pygame.image.load("../images/explosion1.png")
        explode_img2 = pygame.image.load("../images/explosion2.png")
        explode_img3 = pygame.image.load("../images/explosion3.png")

        self.explode_imgs = [explode_img1, explode_img2, explode_img3]
        self.angle_imgs = [img_angle1, img_angle2, img_angle3]
        self.image = img_angle1
        self.init_rect()

        self.xdir = xdir
        self.rel_vx = 600

    def init_explosion_death(self):
        self.is_alive = 0

    def all_directions_enemy_collision_handler(self, enemy):
        if enemy.is_alive:
            enemy.init_shot_death(self.xdir)
            self.init_explosion_death()

    def top_block_collision_handler(self, block):
        self.rel_vy = GameSpecs.JUMP_VEL/1.6

    def bottom_block_collision_handler(self, block):
        self.init_explosion_death()

    def left_right_block_collision_handler(self, block):
        self.init_explosion_death()

    def update(self, dt):
        if self.is_dead:
            self.kill()

        if self.is_alive:
            self.prev_rect = self.rect.copy()

            self.update_x(dt)
            self.handle_xcollisions_with_expanded_rect(
                                        self.game.block_sprites,
                                        self.left_right_block_collision_handler,
                                        self.left_right_block_collision_handler)
            self.update_y(dt)
            hit_top, hit_bottom = self.handle_ycollisions_with_expanded_rect(
                                                        self.game.block_sprites,
                                                        self.top_block_collision_handler,
                                                        self.bottom_block_collision_handler)
            self.update_float_status(hit_top)  #sets the is_in_air flag, if needed

            self.all_direction_collision_handler(self.game.enemy_sprites,
                                                 self.all_directions_enemy_collision_handler)
        self.check_bounds()
        self.animate()

    def animate(self):
        if self.is_alive:
            valid_imgs = self.angle_imgs
        else:
            valid_imgs = self.explode_imgs

        self.update_image_from_series(valid_imgs)



