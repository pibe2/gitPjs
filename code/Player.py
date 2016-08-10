from mario1_1 import *
from GGlobals import *
from AutoPilotSprite import *
from FireBall import FireBall


# TODO: refine animation scheme: each different animation sequence should have its own functions
#       as in separate each animation sequence
# TODO: allow movement after fatal touch(during blink animation)
# TODO: Implement sprinting
# TODO: fully IMPLEMENT ENLARGEMENT transition animation
# TODO: fully implement transition animations
# TODO: flip images instead of using completely different png files for right and left facing
# TODO: don't copy prev rects, and instead just move them. providing that
class Player(AutoPilotSprite):
    def __init__(self, position, game):
        super(Player, self).__init__(position, game)
        self.join_sprite_group(game.player_sprites)

        small_walk_left1 = pygame.image.load('../images/smallmariowalk1_left.png').convert_alpha()
        small_walk_left2 = pygame.image.load('../images/smallmariowalk2_left.png').convert_alpha()
        small_walk_left3 = pygame.image.load('../images/smallmariowalk3_left.png').convert_alpha()
        small_walk_right1 = pygame.transform.flip(small_walk_left1, True, False)
        small_walk_right2 = pygame.transform.flip(small_walk_left2, True, False)
        small_walk_right3 = pygame.transform.flip(small_walk_left3, True, False)
        large_walk_left1 = pygame.image.load('../images/bigmariowalk1_left.png').convert_alpha()
        large_walk_left2 = pygame.image.load('../images/bigmariowalk2_left.png').convert_alpha()
        large_walk_left3 = pygame.image.load('../images/bigmariowalk3_left.png').convert_alpha()
        large_walk_right1 = pygame.transform.flip(large_walk_left1, True, False)
        large_walk_right2 = pygame.transform.flip(large_walk_left2, True, False)
        large_walk_right3 = pygame.transform.flip(large_walk_left3, True, False)
        small_horiz_imgs = [[small_walk_left1, small_walk_left2, small_walk_left3],
                            [small_walk_right1, small_walk_right2, small_walk_right3]]
        large_horiz_imgs = [[large_walk_left1, large_walk_left2, large_walk_left3],
                            [large_walk_right1, large_walk_right2, large_walk_right3]]
        self.horiz_move_imgs = [small_horiz_imgs, large_horiz_imgs]

        small_jump_left = pygame.image.load('../images/smallmariojump_left.png').convert_alpha()
        small_jump_right = pygame.transform.flip(small_jump_left, True, False)
        large_jump_left = pygame.image.load('../images/bigmariojump_left.png').convert_alpha()
        large_jump_right = pygame.transform.flip(large_jump_left, True, False)
        self.vert_move_imgs = [[small_jump_left, small_jump_right],[large_jump_left, large_jump_right]]

        small_rest_left = pygame.image.load('../images/smallmariorest_left.png').convert_alpha()
        small_rest_right = pygame.transform.flip(small_rest_left, True, False)
        large_rest_left = pygame.image.load('../images/bigmariorest_left.png').convert_alpha()
        large_rest_right = pygame.transform.flip(large_rest_left, True, False)
        self.rest_imgs = [[small_rest_left, small_rest_right], [large_rest_left, large_rest_right]]

        large_swerve_left = pygame.image.load('../images/bigmariochangedir_left.png').convert_alpha()
        large_swerve_right = pygame.transform.flip(large_swerve_left, True, False)
        small_swerve_left = pygame.image.load('../images/smallmariochangedir_left.png').convert_alpha()
        small_swerve_right = pygame.transform.flip(small_swerve_left, True, False)
        small_swerve_imgs = [[small_swerve_left], [small_swerve_right]]
        large_swerve_imgs = [[large_swerve_left], [large_swerve_right]]
        self.swerve_imgs = [small_swerve_imgs, large_swerve_imgs]

        small_bending_right = pygame.image.load('../images/smallmariobending.png').convert_alpha()
        small_bending_left = small_bending_right  # not actually facing any direction
        large_bending_right = pygame.image.load('../images/bigmariobending.png').convert_alpha()
        large_bending_left = pygame.transform.flip(large_bending_right, True, False)
        small_bending_imgs = [[small_bending_left], [small_bending_right]]
        large_bending_imgs = [[large_bending_left], [large_bending_right]]
        self.bending_imgs = [small_bending_imgs, large_bending_right]

        small_swimming_right1 = pygame.image.load('../images/smallmarioflying1.png').convert_alpha()
        small_swimming_right2 = pygame.image.load('../images/smallmarioflying2.png').convert_alpha()
        small_swimming_right3 = pygame.image.load('../images/smallmarioflying3.png').convert_alpha()
        small_swimming_left1 = pygame.transform.flip(small_swimming_right1, True, False)
        small_swimming_left2 = pygame.transform.flip(small_swimming_right2, True, False)
        small_swimming_left3 = pygame.transform.flip(small_swimming_right3, True, False)
        large_swimming_right1 = pygame.image.load('../images/bigmarioflying1.png').convert_alpha()
        large_swimming_right2 = pygame.image.load('../images/bigmarioflying2.png').convert_alpha()
        large_swimming_right3 = pygame.image.load('../images/bigmarioflying3.png').convert_alpha()
        large_swimming_left1 = pygame.transform.flip(large_swimming_right1, True, False)
        large_swimming_left2 = pygame.transform.flip(large_swimming_right2, True, False)
        large_swimming_left3 = pygame.transform.flip(large_swimming_right3, True, False)
        small_swimming_imgs = [[small_swimming_left1, small_swimming_left2, small_swimming_left3],
                                [small_swimming_right1, small_swimming_right2, small_swimming_right3]]
        large_swimming_imgs = [[large_swimming_left1, large_swimming_left2, large_swimming_left3],
                                [large_swimming_right1, large_swimming_right2, large_swimming_right3]]
        self.swimming_imgs = [small_swimming_imgs, large_swimming_imgs]

        small_pole_catch_right1 = pygame.image.load('../images/smallmarioflying4.png').convert_alpha()
        small_pole_catch_right2 = pygame.image.load('../images/smallmarioflying5.png').convert_alpha()
        small_pole_catch_left1 = pygame.transform.flip(small_pole_catch_right1, True, False)
        small_pole_catch_left2 = pygame.transform.flip(small_pole_catch_right2, True, False)
        large_pole_catch_right1 = pygame.image.load('../images/bigmarioflying4.png').convert_alpha()
        large_pole_catch_right2 = pygame.image.load('../images/bigmarioflying5.png').convert_alpha()
        large_pole_catch_left1 = pygame.transform.flip(large_pole_catch_right1, True, False)
        large_pole_catch_left2 = pygame.transform.flip(large_pole_catch_right2, True, False)
        small_pole_catch_imgs = [[small_pole_catch_left1, small_pole_catch_left2],
                                [small_pole_catch_right1, small_pole_catch_right2]]
        large_pole_catch_imgs = [[large_pole_catch_left1, large_pole_catch_left2],
                                [large_pole_catch_right1, large_pole_catch_right2]]
        self.pole_catch_imgs = [small_pole_catch_imgs, large_pole_catch_imgs]

        self.image = small_rest_right
        self.image_size = ImageSize.SMALL

        self.move_rel_vx = 400

        #self.rel_vx = 400
        self.rel_vx = 1500
        self.rel_vy = 0

        self.can_fire = False
        self.can_break_blocks = False
        self.last_fired = 0 #so we don't fire too many bullets at one
        self.is_invinsible = False
        self.is_game_over = False

        self.flag_and_pole = None
        self.is_released_from_pole = False
        self.init_rect()

    def init_bounds_death(self):
        """ triggers the death animation/flashing when out of bounds"""
        if self.is_alive:
            self.is_alive = 0
            self.death_img = self.image

    def init_enemy_death(self):
        """ triggers death animation/flashing when hit by enemy """
        self.init_bounds_death()

    def init_game_over(self):
        if not self.is_game_over:
            self.is_game_over = True
            self.rel_vy = - 200
            self.rel_vx = 0

    def game_over_update(self, dt):
        self.update_y(dt)
        self.check_bounds()
        self.game_over_animate()

    def game_over_animate(self):
        self.image = self.bending_imgs[self.image_size][self.xdir][0]

    def check_bounds(self):
        if self.rect.y > GameSpecs.Y_GROUND + 100:
            if self.is_game_over:
                self.game.game_over()
            else:
                self.init_bounds_death()

    def set_image_size(self, image_size):
        """
        enlarges or shrinks the pixie as determined by
        power-ups.
        """
        self.image_size = image_size

        centerx = self.rect.centerx
        bottom = self.rect.bottom

        self.rect = pygame.Rect((0, 0), (self.rest_imgs[self.image_size][self.xdir]).get_size())
        self.rect.centerx = centerx
        self.rect.bottom = bottom

    def handle_redmushroom_collisions(self):
        """ consumption of red mushroom powerup. """
        kill_on_collide = False  # so spritecollide() doesn't kill consumables
        for redshroom in pygame.sprite.spritecollide(self, self.game.redmushroom_sprites, kill_on_collide):
            schroom_x, schroom_y = redshroom.get_position()
            self.game.increase_score_by(redshroom.score_value, (schroom_x + 50, schroom_y - 50))
            redshroom.kill()
            self.can_break_blocks = True
            self.set_image_size(ImageSize.LARGE)

    def handle_greenmushroom_collisions(self):
        """ consumption of green mushroom powerup. """
        kill_on_collide = False
        for greenshroom in pygame.sprite.spritecollide(self, self.game.greenmushroom_sprites, kill_on_collide):
            schroom_x, schroom_y = greenshroom.get_position()
            self.game.increase_score_by(greenshroom.score_value, (schroom_x + 50, schroom_y - 50))
            self.game.increment_num_lives((schroom_x - 50, schroom_y - 50))
            greenshroom.kill()

    def handle_flower_collisions(self):
        """ consumption of flower powerup. """
        kill_on_collide = False
        for flower in pygame.sprite.spritecollide(self, self.game.flower_sprites, kill_on_collide):
            flower_x, flower_y = flower.get_position()
            self.game.increase_score_by(flower.score_value, (flower_x + 50, flower_y - 50))
            flower.kill()
            self.can_fire = True

    def handle_coin_collisions(self):
        kill_on_collide = False
        for coin in pygame.sprite.spritecollide(self, self.game.coin_sprites, kill_on_collide):
            coin_x, coin_y = coin.get_position()
            self.game.increase_score_by(coin.score_value, (coin_x + 50, coin_y - 50))
            coin.kill()
            self.game.increment_num_coins()

    def handle_star_collisions(self):
        kill_on_collide = False
        for star in pygame.sprite.spritecollide(self, self.game.star_sprites, kill_on_collide):
            star_x, star_y = star.get_position()
            self.game.increase_score_by(star.score_value, (star_x + 50, star_y - 50))
            star.kill()
            self.is_invinsible = True

    # ____________________________________________________________________________________________
    # FLAGPOLE COLLISIONS and EVENTS
    # ____________________________________________________________________________________________
    def flagpole_collision_handler(self, flag_and_pole):
        self.rel_vx = 0
        self.rel_vy = flag_and_pole.flag.descent_vy
        self.xdir = Direction.RIGHT
        self.rect.right = flag_and_pole.rect.left
        self.flag_and_pole = flag_and_pole
        flag_and_pole.release_flag()

    def to_otherside_of_flagpole(self):
        self.xdir = Direction.LEFT
        self.rect.left = self.flag_and_pole.rect.right

    def release_from_flag_pole(self):
        self.xdir = Direction.RIGHT
        self.rel_vx = self.move_rel_vx
        self.is_released_from_pole = True

    # ___________________________________________________________________________________________
    # ENEMY COLLISIONS
    # ___________________________________________________________________________________________
    def enemy_bottom_left_right_collision_handler(self, enemy):
        if (not self.is_alive) or (not enemy.is_alive):
            return

        enemy_x, enemy_y = enemy.get_position()
        if self.is_invinsible:
            self.game.increase_score_by(enemy.shot_score_value, (enemy_x + 50, enemy_y - 50))
            enemy.init_shot_death(self.xdir)
            return

        self.init_enemy_death()

    def enemy_top_collision_handler(self, enemy):
        if (not self.is_alive) or (not enemy.is_alive):
            return

        next_rect = self.rect
        enemy_rect = enemy.get_collision_rect()
        enemy_x, enemy_y = enemy.get_position()

        if self.is_invinsible:
            enemy.init_shot_death(self.xdir)
            self.game.increase_score_by(enemy.shot_score_value, (enemy_x + 50, enemy_y - 50))
            return

        next_rect.bottom = enemy_rect.top
        self.rel_vy = GameSpecs.JUMP_VEL / 2
        self.is_inair = 1
        self.game.increase_score_by(enemy.stomped_score_value, (enemy_x + 50, enemy_y - 50))
        enemy.init_stepped_death()

    # ___________________________________________________________________________________________
    # BLOCK COLLISIONS
    # ___________________________________________________________________________________________
    def right_block_collision_handler(self, block):
        next_rect = self.rect
        block_rect = block.rect
        next_rect.left = block_rect.right

    def left_block_collision_handler(self, block):
        next_rect = self.rect
        block_rect = block.rect
        next_rect.right = block_rect.left

    def bottom_block_collision_handler(self, block):
        next_rect = self.rect
        block_rect = block.get_collision_rect()
        next_rect.top = block_rect.bottom
        self.rel_vy = 0
        if self.can_break_blocks:
            block.kill()
        block.on_hit()
    # ___________________________________________________________________________________________
    # UPDATING
    # ___________________________________________________________________________________________

    def check_buttons(self, keys):
        """ updates the pixie's flags based on keyboard inputs. """
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.rel_vx = 0

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rel_vx = -self.move_rel_vx
            self.xdir = Direction.LEFT

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rel_vx = self.move_rel_vx
            self.xdir = Direction.RIGHT

        else:
            self.rel_vx = 0

        if self.is_inair == 0 and (keys[pygame.K_UP] or keys[pygame.K_w]):
            # 'is_inair' flag is set a frame or two earlier
            # than if falling without first jumping
            self.is_inair = 1
            self.rel_vy = GameSpecs.JUMP_VEL

        if keys[pygame.K_SPACE] and self.can_fire and self.last_fired > 6:
            self.launch_fireball()
            self.last_fired = 0

    def update_x(self, dt):
        blk_wid, blk_len = GameSpecs.BLOCK_SIZE
        # min bc we don't want it to be able to completely move past a block in
        # one update (for collision detection)
        dx = min(int(dt * self.abs_vx), blk_wid - 1)
        self.rect.x += dx

        self.abs_vx = self.rel_vx  #reset it, so platform can set it again

    def update_y(self, dt):
        """
        updates the pixie's x position based on keyboard inputs
        and gravity.
        """
        blk_wid, blk_len = GameSpecs.BLOCK_SIZE

        dv = Utils.custom_int_round(dt * GameSpecs.GRAVITY)
        self.rel_vy += dv
        dy = Utils.custom_int_round(dt * self.rel_vy)
        self.rect.y += min(dy, blk_len - 1)

    def flagpole_end_update(self, dt):
        self.prev_rect = self.rect.copy()

        self.update_x(dt)
        if self.is_released_from_pole:
            self.update_y(dt)
        else:
            self.rect.y += self.rel_vy * dt
        if self.rect.x >= 13210:
            self.game.stage_complete()

        hit_top, hit_bottom = self.handle_ycollisions_with_expanded_rect(
                                                    self.game.player_block_sprites,
                                                    self.top_block_collision_handler,
                                                    self.bottom_block_collision_handler)
        if ((not self.is_released_from_pole) and
                (self.rect.bottom == self.flag_and_pole.flag.base_y)):

            self.to_otherside_of_flagpole()
        if self.flag_and_pole.flag.is_at_base:
            self.release_from_flag_pole()
        self.update_float_status(hit_top)  #sets the is_in_air flag, if needed
        self.flagpole_end_animate()

    def update(self, dt):
        """
        updates pixie position based on inputs, gravity, and
        collisions.
        """
        if self.is_game_over:
            self.game_over_update(dt)
            return
        elif self.flag_and_pole is not None:
            self.flagpole_end_update(dt)
            return
        if self.is_alive:
            self.check_buttons(pygame.key.get_pressed())
            # self.set_prev_rect()
            self.prev_rect = self.rect.copy()

            self.update_x(dt)
            self.handle_xcollisions_with_expanded_rect(
                                        self.game.player_block_sprites,
                                        self.left_block_collision_handler,
                                        self.right_block_collision_handler)

            self.update_y(dt)
            hit_top, hit_bottom = self.handle_ycollisions_with_expanded_rect(
                                                        self.game.player_block_sprites,
                                                        self.top_block_collision_handler,
                                                        self.bottom_block_collision_handler)
            self.update_float_status(hit_top)  #sets the is_in_air flag, if needed

            self.handle_redmushroom_collisions()
            self.handle_greenmushroom_collisions()
            self.handle_flower_collisions()
            self.handle_star_collisions()
            self.handle_xcollisions(self.game.enemy_sprites,
                                    self.enemy_bottom_left_right_collision_handler,
                                    self.enemy_bottom_left_right_collision_handler)
            self.handle_ycollisions(self.game.enemy_sprites, self.enemy_top_collision_handler,
                                    self.enemy_bottom_left_right_collision_handler)

            self.all_direction_collision_handler(self.game.flag_and_pole_sprites,
                                                 self.flagpole_collision_handler)
        self.last_fired += 1
        self.check_bounds()
        self.animate()

    def launch_fireball(self):
        FireBall((self.rect.x, self.rect.centery), self.xdir, self.game)

    def update_testing(self, dt):
        """
        for testing purposes, no gravity or much animation
        updates mario pixie based on keyboard inputs.
        """
        self.prev_rect = self.rect.copy()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= int(dt * 5*self.rel_vx)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += int(dt * 5*self.rel_vx)

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= int(dt * 3*self.rel_vx)

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += int(dt * 3*self.rel_vx)

    def flagpole_end_animate(self):
        if not self.is_released_from_pole:
            self.image = self.pole_catch_imgs[self.image_size][self.xdir][1]
        else:
            valid_imgs = self.horiz_move_imgs[self.image_size][self.xdir]
            self.update_image_from_series(valid_imgs)

    def animate(self):
        """
        sets the correct image for the sprite, keeping track of
        the number of frame is image is displayed for before
        switching to the next image; takes into consideration
        whether player pressed any keys as well.
        """
        if self.is_alive:
            if not (self.rel_vx != 0 or self.is_inair):
                self.update_image(self.rest_imgs[self.image_size][self.xdir])
                return
            if self.is_inair:
                self.update_image(self.vert_move_imgs[self.image_size][self.xdir])
                return
            else:
                valid_imgs = self.horiz_move_imgs[self.image_size][self.xdir]

        else:
            valid_imgs = [self.blank_img, self.death_img, self.blank_img,
                          self.death_img, self.blank_img, self.death_img]

        self.update_image_from_series(valid_imgs)

    def end_of_animation_series_handler(self):
        if self.is_alive == 0:
            self.game.decrement_num_lives(self.get_position())
            self.is_alive = 1

    def draw(self, screen_surface, view_pos):
        """
        draws player at the center of the screen.
        """
        xv, yv = view_pos
        x, y = self.rect.x, self.rect.y
        pos_on_scr = (x - xv, y - yv)
        screen_surface.blit(self.image, pos_on_scr)
