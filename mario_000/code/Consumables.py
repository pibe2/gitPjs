from GGlobals import *
from mario1_1 import *
from AutoPilotSprite import *


# TODO: auto-detect box-top(via collisions) instead of using ground parameter
class Consumable(AutoPilotSprite):
    def __init__(self, center_pos, is_stationary, ground, game):
        super(Consumable, self).__init__(center_pos, game)
        # self.start_pos is now center_pos

        self.ground = ground
        self.score_value = 100
        self.rel_vy = 0
        self.rel_vx = 0
        self.is_inair = 0

        # is_stationary is True if not originally inside a block
        self.is_stationary = is_stationary
        self.is_released = 0
        self.has_emerged = 0

    def release(self):
        """
        to be triggered after holding container is hit
        by player
        """
        pass

    def init_rect(self):
        """
        sets rect size as in DrawableSprite.init_rect() then
        overwrites center with user given center(start_pos)
        """
        super(Consumable, self).init_rect()
        # rect size set to image size (from DrawableSprite)
        self.rect.center = self.start_pos
        self.prev_rect = self.rect.copy()

    def draw(self, screen_surface, view_pos):
        """
        same calls DrawableSprite.draw() only if the sprite
        is not inside a container
        """
        if self.is_stationary or self.is_released:
            super(Consumable, self).draw(screen_surface, view_pos);


class Coin(Consumable):
    def __init__(self, center_pos, is_stationary, ground, game):
        super(Coin, self).__init__(center_pos, is_stationary, ground, game)
        self.join_sprite_group(game.coin_sprites)
        self.image = pygame.image.load('../images/coin.png').convert_alpha()
        self.init_rect()
        self.score_value = 100

    def release(self):
        """
        coin releases itself from the enclosing block
        by jumping.
        """
        self.game.increase_score_by(self.score_value, (self.rect.x + 50, self.rect.y - 50))
        self.game.increment_num_coins()
        self.is_released = 1
        self.rel_vy = GameSpecs.JUMP_VEL

    def update(self, dt):
        """
        updates coin's position; only used after coin
        is released, jumps and when it goes back into box
        disappears via self.kill().
        """
        if self.is_released:
            self.rect.y += Utils.custom_int_round(dt * self.rel_vy)
            self.rel_vy += Utils.custom_int_round(dt * 2 * GameSpecs.GRAVITY)
            # 2 times gravity so it drops faster

            if self.rect.y > self.ground:
                self.kill()


class Flower(Consumable):
    def __init__(self, center_pos, is_stationary, ground, game):
        super(Flower, self).__init__(center_pos, is_stationary, ground, game)
        self.join_sprite_group(game.flower_sprites)

        self.image = pygame.image.load('../images/whiteorangered_flower.png')
        self.init_rect()
        self.score_value = 1000

    def release(self):
        """
        triggers the flower's release from holding box.
        """
        self.is_released = 1
        self.rel_vy = GameSpecs.JUMP_VEL / 2

    def update(self, dt):
        """
        once released, slowly rises out of the ground
        then stops, otherwise does nothing.
        """
        self.prev_rect = self.rect.copy()

        if self.is_released and self.has_emerged == 0:
            self.update_y(dt)  # from AutoPilotSprite
            if self.rect.bottom < self.ground:
                self.has_emerged = 1
                self.rect.bottom = self.ground


class MovingConsumable(Consumable):
    """
    consumables that move after emerging from container
    superclass of both mushroom power-ups, and the star power-up.
    """
    def __init__(self, center_pos, is_stationary, ground, game):
        super(MovingConsumable, self).__init__(center_pos, is_stationary, ground, game)
        self.score_value = 1000

    def release(self):
        """
        releases mushroom by rising out of the box.
        """
        self.is_released = 1
        self.rel_vy = GameSpecs.JUMP_VEL / 2

    def update(self, dt):
        """
        when released, mushroom rises rising out of the box
        then once out, move to the right, till it hits a wall
        or falls into a hole and self.kill()s. switches direction
        if it hits a wall.
        """
        self.prev_rect = self.rect.copy()
        if self.is_released:
            if self.has_emerged:
                self.update_x(dt)
                self.handle_xcollisions_with_expanded_rect(self.game.block_sprites,
                                                           self.left_block_collision_handler,
                                                           self.right_block_collision_handler)
                self.update_y(dt)
                self.handle_ycollisions_with_expanded_rect(
                                                            self.game.block_sprites,
                                                            self.top_block_collision_handler,
                                                            self.bottom_block_collision_handler)
                self.check_bounds()
            else:
                self.update_y(dt)
                if self.rect.bottom < self.ground:
                    self.rect.bottom = self.ground
                    self.rel_vx = 370
                    self.rel_vy = 0
                    self.has_emerged = 1

            self.check_bounds()
    '''
    def update(self, dt):
        """
        when released, mushroom rises rising out of the box
        then once out, move to the right, till it hits a wall
        or falls into a hole and self.kill()s. switches direction
        if it hits a wall.
        """
        self.prev_rect = self.rect.copy()
        if self.is_released:
            if self.has_emerged:
                self.update_x(dt)
                self.handle_xcollisions(self.game.block_sprites,
                                                           self.left_block_collision_handler,
                                                           self.right_block_collision_handler)
                self.update_y(dt)
                self.handle_ycollisions(
                                                            self.game.block_sprites,
                                                            self.top_block_collision_handler,
                                                            self.bottom_block_collision_handler)
                self.check_bounds()
            else:
                self.update_y(dt)
                if self.rect.bottom < self.ground:
                    self.rect.bottom = self.ground
                    self.rel_vx = 370
                    self.rel_vy = 0
                    self.has_emerged = 1

            self.check_bounds()
    '''


class RedMushroom(MovingConsumable):
    def __init__(self, center_pos, is_stationary, ground, game):
        super(RedMushroom, self).__init__(center_pos, is_stationary, ground, game)
        self.join_sprite_group(game.redmushroom_sprites)
        self.image = pygame.image.load('../images/yellowred_mushroom.png')
        self.init_rect()


class GreenMushroom(MovingConsumable):
    def __init__(self, center_pos, is_stationary, ground, game):
        super(GreenMushroom, self).__init__(center_pos, is_stationary, ground, game)
        self.join_sprite_group(game.greenmushroom_sprites)
        self.image = pygame.image.load('../images/yellowgreen_mushroom.png')
        self.init_rect()


class Star(MovingConsumable):
    def __init__(self, center_pos, is_stationary, ground, game):
        super(Star, self).__init__(center_pos, is_stationary, ground, game)
        self.join_sprite_group(game.star_sprites)
        self.image = pygame.image.load('../images/star.png')
        self.init_rect()

    def top_block_collision_handler(self, block):
        self.rel_vy = GameSpecs.JUMP_VEL/1.6





