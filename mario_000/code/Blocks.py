import math

from mario1_1 import *
from GGlobals import *
from Consumables import *
from DrawableSprite import *


class Block(DrawableSprite):
    """
    generic invisible block
    """
    def __init__(self, position, game):
        super(Block, self).__init__(position, game)

        self.join_sprite_group(game.player_block_sprites)
        self.join_sprite_group(game.block_sprites)

        self.rect = pygame.rect.Rect(position, GameSpecs.BLOCK_SIZE)
        self.prev_rect = self.rect.copy()
        self.game = game

    def on_hit(self):
        """
        meant to be triggered when mario hits the underside
        """
        pass

    def on_land(self, landing_sprite):
        """
        meant to be triggered when mario lands on a platform
        used for moving platforms
        """
        pass

    def init_rect(self):
        if self.image is None:
            self.rect.size = GameSpecs.BLOCK_SIZE
        else:
            super(Block, self).init_rect()

    def is_moving(self):
        return False

    def is_breakable(self):
        return False


class BrickBlock(Block):
    def __init__(self, position, game):
        super(BrickBlock, self).__init__(position, game)
        self.image = pygame.image.load('../images/brickblock.png').convert_alpha()
        self.init_rect()

    def is_breakable(self):
        return True


class StairBlock(Block):
    def __init__(self, position, game):
        super(StairBlock, self).__init__(position, game)
        self.image = pygame.image.load('../images/stairblock.png').convert_alpha()
        self.init_rect()


class VariableSizeBlock(Block):
    def __init__(self, position, size, game):
        super(VariableSizeBlock, self).__init__(position, game)
        self.rect = pygame.rect.Rect(position, size)
        self.prev_rect = self.rect


# TODO: Kill enemies on top of a block that has been hit (from underneath)
class HittableBlock(Block):
    """
     holds consumables, and releases one on each hit until it
     runs out
     may also be broken, i think(TODO: use an is_breakable flag which will be set to
                                        true when mario eats block breaking powerup)
    """
    def __init__(self, position, game):
        super(HittableBlock, self).__init__(position, game)

        self.image = pygame.image.load('../images/questblock.png').convert_alpha()
        self.spent_image = pygame.image.load('../images/questblock_spent.png').convert_alpha()
        self.init_rect()

        self.consumables = []
        self.num_consumables = 0

        self.ground = position[1]
        self.is_jumping = 0
        self.rel_vy = 0

    def add_coins(self, num):
        """
        meant to be used only at init
        adds the given number of coins
        """
        self.num_consumables += num
        is_stationary = False
        for i in range(num):
            c = Coin(self.rect.center, is_stationary, self.rect.top, self.game)
            self.consumables.append(c)

    def add_redmushrooms(self, num):
        """
        meant to be used only at init
        adds the given number of red shrooms
        """
        self.num_consumables += num
        is_stationary = False
        for i in range(num):
            rm = RedMushroom(self.rect.center, is_stationary, self.rect.top, self.game)
            self.consumables.append(rm)

    # meant to be used only at init
    def add_greenmushrooms(self, num):
        """
        meant to be used only at init
        adds the given number of green shrooms
        """
        self.num_consumables += num
        is_stationary = False
        for i in range(num):
            rm = GreenMushroom(self.rect.center, is_stationary, self.rect.top, self.game)
            self.consumables.append(rm)

    def add_flowers(self, num):
        """
        meant to be used only at init
        adds the given number of flowers
        """
        self.num_consumables += num
        is_stationary = False
        for i in range(num):
            f = Flower(self.rect.center, is_stationary, self.rect.top, self.game)
            self.consumables.append(f)

    # meant to be used only at init
    def add_star(self, num):
        """
        meant to be used only at init
        adds the given number of green shrooms
        """
        self.num_consumables += num
        is_stationary = False
        for i in range(num):
            rm = Star(self.rect.center, is_stationary, self.rect.top, self.game)
            self.consumables.append(rm)

    def on_hit(self):
        """
        triggered when player hits underside of the block (as in player.
        handle_block_collisions); releases one of remaining consumable
        may also be broken(see todo note at class start).
        Also triggers a small jump animation on the block
        """
        if self.is_jumping:
            return
        self.init_jump()
        self.release_consumable()

    def init_jump(self):
        """
        triggers a small jump animation, as in self.on_hit()
        """
        self.is_jumping = 1
        self.rel_vy = GameSpecs.JUMP_VEL / 8

    def release_consumable(self):
        """
        releases one of the remaining consumable, triggering its relase handler
        """
        if self.num_consumables:
            self.num_consumables -= 1
            if self.num_consumables == 0:
                self.image = self.spent_image

            consumable = self.consumables.pop()
            consumable.release()

    def update(self, dt):
        """
        updates the position of the block positon, in the case of jumps
        """
        if self.is_jumping:
            if self.rect.y > self.ground:
                self.rect.y = self.ground
                self.is_jumping = 0
                return

            self.rect.y += Utils.custom_int_round(dt * self.rel_vy)
            self.rel_vy += Utils.custom_int_round(dt * GameSpecs.GRAVITY)


# TODO: Implement breaking of blocks
class MovingPlatform(Block):
    """
    moving block/platform
    """
    def __init__(self, start_pos, end_pos, game):
        super(MovingPlatform, self).__init__(start_pos, game)
        self.image = pygame.image.load('../images/cloud.png').convert_alpha()  # to-be-changed
        self.init_rect()

        self.rel_vx = 200
        self.rel_vy = 300

        self.dx = 0
        self.dy = 0

        self.start_pos = start_pos
        self.end_pos = end_pos
        self.rect.x, self.rect.y = start_pos
        self.goal_x = end_pos[0]
        self.goal_y = end_pos[1]
        self.y_collide_offset = 50

    def is_moving(self):
        return True

    def update(self, dt):
        self.prev_rect = self.rect.copy()
        xdir = math.copysign(1, self.goal_x - self.rect.x)
        ydir = math.copysign(1, self.goal_y - self.rect.y)
        self.rect.x += Utils.custom_int_round(dt * self.rel_vx * xdir)
        self.rect.y += Utils.custom_int_round(dt * self.rel_vy * ydir)

        if (self.rect.x - self.goal_x) * xdir > 0:
            self.rect.x = self.goal_x
        if (self.rect.y - self.goal_y) * ydir > 0:
            self.rect.y = self.goal_y
        if self.rect.y == self.goal_y and self.rect.x == self.goal_x:
            if self.goal_x == self.start_pos[0] and self.goal_y == self.start_pos[1]:
                self.goal_x, self.goal_y = self.end_pos
            else:
                self.goal_x, self.goal_y = self.start_pos

        self.dx = self.rect.x - self.prev_rect.x
        self.dy = self.rect.y - self.prev_rect.y

    def get_collision_rect(self):
        # we want to stay below the image top
        rect = self.rect
        pos = rect.x, rect.y + self.y_collide_offset
        size = rect.width, rect.height - self.y_collide_offset
        return pygame.Rect(pos, size)

    def get_prev_collision_rect(self):
        # we want to stay below the image top
        rect = self.prev_rect
        pos = rect.x, rect.y + self.y_collide_offset
        size = rect.width, rect.height - self.y_collide_offset
        return pygame.Rect(pos, size)


class GreenFlagPole(DrawableSprite):
    """
    end-game flag pole; positioned relative to its base
    """
    def __init__(self, base_center_x, base_y, game):
        super(GreenFlagPole, self).__init__((0, 0), game)
        self.image = pygame.image.load('../images/greenflagpole.png').convert_alpha()
        self.base_y = base_y
        self.base_center_x = base_center_x
        self.init_rect()

    def init_rect(self):
        super(GreenFlagPole, self).init_rect()
        self.rect.bottom = self.base_y
        self.rect.centerx = self.base_center_x


class GreenFlag(DrawableSprite):
    """
    end-game flag; positioned relative to its flagpole
    """
    def __init__(self, flag_pole_pos, base_y, game):
        super(GreenFlag, self).__init__((0, 0), game)
        self.image = pygame.image.load('../images/greenflag.png').convert_alpha()
        self.flag_pole_pos = flag_pole_pos
        self.init_rect()
        self.base_y = base_y
        self.is_released = False
        self.is_at_base = False
        self.descent_vy = 300

    def init_rect(self):
        super(GreenFlag, self).init_rect()
        pole_left, pole_top = self.flag_pole_pos
        self.rect.right = pole_left + 15
        self.rect.top = pole_top + 30

    def update(self, dt):
        if self.is_released and self.rect.y < self.base_y:
            dy = Utils.custom_int_round(dt * self.descent_vy)
            self.rect.y += dy

            if self.rect.bottom > self.base_y:
                self.rect.bottom = self.base_y
                self.is_at_base = True

    def set_released(self):
        self.is_released = True


class FlagAndPole(pygame.sprite.Sprite):
    def __init__(self, base_center_x, base_y, game):
        super(FlagAndPole, self).__init__(game.flag_and_pole_sprites)
        self.game = game
        self.flag_pole = GreenFlagPole(base_center_x, base_y, game)
        self.flag = GreenFlag(self.flag_pole.get_position(), base_y, game)
        self.rect = self.flag_pole.rect.copy()

    def update(self, dt):
        self.flag.update(dt)

    def release_flag(self):
        self.flag.set_released()

    def draw(self, surface, view_pos):
        self.flag.draw(surface, view_pos)
        self.flag_pole.draw(surface, view_pos)
