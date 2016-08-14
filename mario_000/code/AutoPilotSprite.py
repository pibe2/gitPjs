from mario1_1 import *
from GGlobals import *
from DrawableSprite import *


class AutoPilotSprite(DrawableSprite):
    """
    computer controlled sprite that moves back and forth
    horizontally, obeys gravity
    """
    def __init__(self, start_pos, game):
        super(AutoPilotSprite, self).__init__(start_pos, game)

        self.horiz_move_imgs = None
        self.vert_move_imgs = None
        self.death_img = None
        self.blank_img = pygame.image.load('../images/trans_blank.png').convert_alpha()

        self.prev_rect = None
        self.temp_rect = None   # saves the rectangle not in use; useful for when
                                # we expand our rectangle for better collision detection
        self.rel_vx = 200
        self.rel_vy = 0
        self.abs_vx = self.rel_vx
        self.abs_vy = self.rel_vy
        self.ax = 0
        self.ay = 0

        self.xdir = Direction.RIGHT
        self.is_inair = 1

    def init_rect(self):
        super(AutoPilotSprite, self).init_rect()
        self.temp_rect = self.rect.copy()

    # expands rectangle to be used before spritecollide
    def expand_rect(self):
        self.temp_rect.size = (self.rect.width * 2, self.rect.height * 2)
        self.temp_rect.center = self.rect.center
        self.swap_rects()

    # returns rectangle to normal size; assumes this is called
    # right after* a call to expand_rect
    def contract_rect(self):
        self.swap_rects()

    # returns the rectangle to normal
    def swap_rects(self):
        temp = self.rect
        self.rect = self.temp_rect
        self.temp_rect = temp

    # ________________________________________________________________________
    # GENERALIZED COLLISIONS
    # ________________________________________________________________________
    def handle_xcollisions(self, sprite_group, right_handler, left_handler):
        """
        Generalized horizontal collision function that given a sprite_group,
        a handler for the object's collision with a sprite's (in sprite_group) left
        and a handler for the right case.
        the handlers are of the form self.handler(other_sprite), where other_sprite
        is a sprite in sprite_group that has collided with self in the way handled by
        handler.
        Return two booleans, the first signifiying whether any collisions of the left
        case occured, and the second deals with the right case
        :param sprite_group:
        :param left_handler:
        :param right_handler:
        :return: (Boolean, Boolean)
        """
        last_rect = self.prev_rect
        next_rect = self.rect
        hit_right, hit_left = False, False
        kill_on_collide = False
        for other_sprite in pygame.sprite.spritecollide(self, sprite_group, kill_on_collide):
            other_sprite_rect = other_sprite.get_collision_rect()
            prev_other_sprite_rect = other_sprite.get_prev_collision_rect()
            if (last_rect.left >= prev_other_sprite_rect.right and
                        next_rect.left < other_sprite_rect.right):
                hit_left = True
                left_handler(other_sprite)

            if (last_rect.right <= prev_other_sprite_rect.left and
                        next_rect.right > other_sprite_rect.left):
                hit_right = True
                right_handler(other_sprite)
        return hit_right, hit_left

    def handle_ycollisions(self, sprite_group, top_handler, bottom_handler):
        """
        exactly like handle_xcollisions, but for vertical collisions
        """
        last_rect = self.prev_rect
        next_rect = self.rect
        hit_top, hit_bottom = False, False
        kill_on_collide = False
        for other_sprite in pygame.sprite.spritecollide(self, sprite_group, kill_on_collide):
            other_sprite_rect = other_sprite.get_collision_rect()
            prev_other_sprite_rect = other_sprite.get_prev_collision_rect()
            if (last_rect.top >= prev_other_sprite_rect.bottom and
                        next_rect.top < other_sprite_rect.bottom):
                hit_bottom = True
                bottom_handler(other_sprite)

            if (last_rect.bottom <= prev_other_sprite_rect.top and
                        next_rect.bottom > other_sprite_rect.top):
                hit_top = False
                top_handler(other_sprite)
        return hit_top, hit_bottom

    def all_direction_collision_handler(self, sprite_group, handler):
        """
        see handle_xcollisions, and handle_ycollisions; however
        uses the provided handler for all directions of collisions.
        returns whether any collisions were detected
        :param sprite_group:
        :param handler:
        :return: Boolean
        """
        has_collided = False
        kill_on_collide = False
        for other_sprite in pygame.sprite.spritecollide(self, sprite_group, kill_on_collide):
            has_collided = True
            handler(other_sprite)
        return has_collided

    def handle_xcollisions_with_expanded_rect(self, sprite_group, right_handler, left_handler):
        """
        similar to handle_xcollisions, but expands rectanglge before calling spritecollide
        """
        last_rect = self.prev_rect
        next_rect = self.rect
        hit_right, hit_left = False, False

        self.expand_rect()
        kill_on_collide = False
        collided_sprites = pygame.sprite.spritecollide(self, sprite_group, kill_on_collide)
        self.contract_rect()

        for other_sprite in collided_sprites:
            other_sprite_rect = other_sprite.get_collision_rect()
            prev_other_sprite_rect = other_sprite.get_prev_collision_rect()

            # since we used an expanded rect in spritecollide(), we have to
            # make sure they actually collided in the x direction
            if self.is_overlapped_y(prev_other_sprite_rect, last_rect):
                if (last_rect.left >= prev_other_sprite_rect.right and
                            next_rect.left < other_sprite_rect.right):
                    hit_left = True
                    left_handler(other_sprite)

                elif (last_rect.right <= prev_other_sprite_rect.left and
                              next_rect.right > other_sprite_rect.left):
                    hit_right = True
                    right_handler(other_sprite)
        return hit_right, hit_left

    def handle_ycollisions_with_expanded_rect(self, sprite_group, top_handler, bottom_handler):
        """
        see handle_ycollisions. but uses an expanded rect before calling spritecollide()
        """
        last_rect = self.prev_rect
        next_rect = self.rect  # gets adjusted
        hit_top, hit_bottom = False, False

        self.expand_rect()
        kill_on_collide = False
        collided_sprites = pygame.sprite.spritecollide(self, sprite_group, kill_on_collide)
        self.contract_rect()

        for other_sprite in collided_sprites:
            prev_other_sprite_rect = other_sprite.get_prev_collision_rect()
            other_sprite_rect = other_sprite.get_collision_rect()

            # since we used an expanded rect in spritecollide(), we have to
            # make sure they actually collided in the x direction
            if self.is_overlapped_x(prev_other_sprite_rect, last_rect):

                if (last_rect.top >= prev_other_sprite_rect.bottom and
                            next_rect.top <= other_sprite_rect.bottom):
                    hit_bottom = True
                    bottom_handler(other_sprite)

                elif (last_rect.bottom <= prev_other_sprite_rect.top and
                              next_rect.bottom >= other_sprite_rect.top):
                    hit_top = True
                    top_handler(other_sprite)
        return hit_top, hit_bottom

    # _________________________________________________
    # BLOCK COLLISION HANDLERS
    # _________________________________________________
    def right_block_collision_handler(self, block):
        next_rect = self.rect
        block_rect = block.rect
        next_rect.left = block_rect.right
        self.xdir = not self.xdir

    def left_block_collision_handler(self, block):
        next_rect = self.rect
        block_rect = block.rect
        next_rect.right = block_rect.left
        self.xdir = not self.xdir

    def top_block_collision_handler(self, block):
        next_rect = self.rect
        block_rect = block.get_collision_rect()
        next_rect.bottom = block_rect.top
        self.is_inair = 0
        self.rel_vy = 0

        # TODO: reset gravity? falls too fast after exiting platform (maybe, i can't actually tell)
        if block.is_moving():
            self.rel_vy = block.rel_vy
            #self.rect.y += block.dy
            if next_rect.x + block.dx > self.game.moving_left_wall.rect.right:
                next_rect.x += block.dx

    def bottom_block_collision_handler(self, block):
        next_rect = self.rect
        block_rect = block.get_collision_rect()
        next_rect.top = block_rect.bottom
        self.rel_vy = 0
    # ___________________________________________________________________
    # ___________________________________________________________________

    def init_bounds_death(self):
        """ if we go past the map limits we die by default """
        self.kill()

    def check_bounds(self):
        if self.rect.y > GameSpecs.Y_GROUND + 100:
            self.init_bounds_death()

    def update_float_status(self, has_landed):
        """ to properly animate falling without first jumping """
        if (not has_landed) and self.rel_vy != 0:
            self.is_inair = 1

    def update_x(self, dt):
        """ move forward if we hit our bounds then turn around """
        blk_wid, blk_len = GameSpecs.BLOCK_SIZE

        # capped to allow collision detection with a block
        dx = min(int(dt * self.rel_vx), blk_wid - 1)

        if self.xdir == Direction.RIGHT:
            self.rect.x = self.rect.x + dx
        else:
            self.rect.x = self.rect.x - dx

    def update_y(self, dt):
        """ moves according to gravity """
        block_width, block_length = GameSpecs.BLOCK_SIZE
        # so integer truncation doesn't leave us with 0
        dv = Utils.custom_int_round(dt * GameSpecs.GRAVITY)
        self.rel_vy += dv
        dy = Utils.custom_int_round(dt * self.rel_vy)
        self.rect.y += min(dy, block_length - 1)

    def update(self, dt):
        if self.is_dead:
            self.kill()
        self.prev_rect = self.rect.copy()
        self.update_x(dt)
        self.handle_xcollisions_with_expanded_rect(
                            self.game.block_sprites,
                            self.left_block_collision_handler,
                            self.right_block_collision_handler)
        self.update_y(dt)
        hit_top, hit_bottom = self.handle_ycollisions_with_expanded_rect(
                                                    self.game.block_sprites,
                                                    self.top_block_collision_handler,
                                                    self.bottom_block_collision_handler)
        self.update_float_status(hit_top)
        self.check_bounds()
        self.animate()

    def animate(self):
        pass
