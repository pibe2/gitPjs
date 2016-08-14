import pygame
import sys
from pygame.locals import *

from dbutils import DBUtils
from Blocks import *
from GGlobals import *
from GreenKoopaTroopa import GreenKoopaTroopa
from Goomba import Goomba
from Player import *
from Text import *

# TODO: sounds
# TODO: make x_update, use of rel_vx consistent across pixies
# TODO: check that pixies are using the right collision rects; ie self.get_collision_rect()
# TODO: ACCELERATION, button b accelerates mario, tweak jump height
# TODO: kill all enemies that are touching on block when hit(with powerup?)
# TODO: bug: can't walk past back blocks in stairs
# TODO: implement check points through out level to recover from out of bounds deaths
def draw_bg(bg_img, surface, player, prev_view_rect):
    """
    allows effect of 'camera' following the player.
    Returns the absolute position of the 'camera'.
    so other pixies draw themselves relative to this position.
    assumes the background images is at least as big
    as the surface size.
    """
    view_rect = surface.get_rect().copy()
    view_width, view_length = view_rect.size
    bg_width, bg_length = bg_img.get_size()

    player_x = player.rect.x
    player_y = player.rect.y

    if player_x >= bg_width - 1 - view_width/2:
        view_rect.right = bg_width - 1
    # if player_x <= view_width/2:  #this was valid when we could backwards
    #    view_rect.left = 0
    elif prev_view_rect is not None:
        if player_x > prev_view_rect.centerx:
            view_rect.centerx = player_x
        else:
            view_rect.centerx = prev_view_rect.centerx

    # flipped y-axis accounted for
    if player_y >= bg_length - 1 - view_length/2:
        view_rect.bottom = bg_length - 1
    elif player_y <= view_length/2:
        view_rect.top = 0
    else:
        view_rect.centery = player_y

    surface.blit(bg_img, (0, 0), view_rect)
    return view_rect


# xdir is +1(y increasing to the right) or -1(y increasing to the left)
def create_stair(start_pos, block_levels, extra_backblocks, xdir, game):
    block_width, block_length = GameSpecs.BLOCK_SIZE
    x, y = start_pos
    # create stairs except for top
    for k in range(block_levels - 1):
        Block((x, y), game)
        x += xdir * block_width
        y -= block_length

    # create extra top-plateau blocks
    for k in range(extra_backblocks):
        Block((x, y), game)
        x += xdir * block_width

    # create back vertical block
    VariableSizeBlock((x, y), (block_width, block_levels * block_length), game)


def create_pipe(pos, yground, game):
    x, y = pos
    lip_width, lip_height = 128, 60
    lip = VariableSizeBlock((x, y), (lip_width, lip_height), game)
    body_width = 110
    body_height = yground - (y + lip_height)
    body = VariableSizeBlock((x, y + lip_height), (body_width, body_height), game)
    body.rect.centerx = lip.rect.centerx


def create_flagpole(base_pos, game):
    base = StairBlock(base_pos, game)  # flagpole base
    FlagAndPole(base.rect.centerx, base.rect.y, game)


def create_floor_walls_ceiling(game):
    block_width, block_length = GameSpecs.BLOCK_SIZE
    world_width, world_length = GameSpecs.WORLD_SIZE

    # VariableSizeBlock((0, -block_length), (wd_wid, block_length), game) # top invisible wall

    # moving boundary that follows player
    game.moving_left_wall = VariableSizeBlock((-block_width, 0), (block_width, world_length), game)
    # so it doesn't affect enemies
    game.moving_left_wall.kill()
    game.moving_left_wall.add(game.player_block_sprites)

    # stationary boundary at the left end
    VariableSizeBlock((-block_width, 0), (block_width, world_length), game)
    VariableSizeBlock((world_width, 0), (block_width, world_length), game)  # right invisible wall

    elevation = world_length - GameSpecs.Y_GROUND
    # create the invisible floors
    VariableSizeBlock((0, GameSpecs.Y_GROUND), (4447, elevation), game)
    VariableSizeBlock((4576, GameSpecs.Y_GROUND), (5478 - 4576 + 64, elevation), game)
    VariableSizeBlock((5736, GameSpecs.Y_GROUND), (9850 - 5736 + 10, elevation), game)
    VariableSizeBlock((9990, GameSpecs.Y_GROUND), (world_width - 9990, elevation), game)


def create_platforms(game):
    block_width, block_length = GameSpecs.BLOCK_SIZE

    #MovingPlatform((400, 100), (100, 600), game)
    #MovingPlatform((400, 100), (100, 600), game)
    MovingPlatform((100, 600), (100, 100), game)
    num_coins = 1
    num_mushrooms = 5
    num_flowers = 5
    hittable_block = HittableBlock((1030, 548), game)
    hittable_block.add_flowers(num_flowers)

    x, y = 1290, 548
    BrickBlock((x, y), game)
    x += block_width
    hittable_block = HittableBlock((x, y), game)
    hittable_block.add_greenmushrooms(num_mushrooms)
    x += block_width
    BrickBlock((x, y), game)
    hittable_block = HittableBlock((x, 290), game)
    hittable_block.add_redmushrooms(num_mushrooms)
    x += block_width
    hittable_block = HittableBlock((x, y), game)
    hittable_block.add_star(num_mushrooms)
    x += block_width
    BrickBlock((x, y), game)

    create_pipe((1805, 676), GameSpecs.Y_GROUND, game)
    create_pipe((2450, 611), GameSpecs.Y_GROUND, game)
    create_pipe((2965, 546), GameSpecs.Y_GROUND, game)
    create_pipe((3674, 546), GameSpecs.Y_GROUND, game)

    x, y = 4963, 548
    BrickBlock((x, y), game)
    x += block_width
    hittable_block = HittableBlock((x, y), game)
    hittable_block.add_redmushrooms(num_mushrooms)
    hittable_block.add_coins(num_coins)
    x += block_width
    BrickBlock((x, y), game)

    x, y = 5157, 290
    for i in range(8):
        BrickBlock((x + i * block_width, y), game)

    x, y = 5865, 290
    for i in range(3):
        BrickBlock((x + i * block_width, y), game)
    hittable_block = HittableBlock((x + 3 * block_width, y), game)
    hittable_block.add_coins(num_coins)
    BrickBlock((x + 3 * block_width, 548), game)

    x, y = 6445, 548
    for i in range(2):
        BrickBlock((x + i * block_width, y), game)

    hittable_block = HittableBlock((6832, y), game)
    hittable_block.add_coins(num_coins)
    hittable_block = HittableBlock((7025, y), game)
    hittable_block.add_coins(num_coins)
    hittable_block = HittableBlock((7025, 290), game)
    hittable_block.add_coins(num_coins)
    hittable_block = HittableBlock((7218, y), game)
    hittable_block.add_coins(num_coins)

    BrickBlock((7605, 548), game)

    x, y = 7798, 290
    for i in range(3):
        BrickBlock((x + i * block_width, y), game)

    x, y = 8249, 290
    BrickBlock((x, y), game)
    hittable_block = HittableBlock((x + block_width, y), game)
    hittable_block.add_coins(num_coins)
    hittable_block = HittableBlock((x + 2 * block_width, y), game)
    hittable_block.add_coins(num_coins)
    BrickBlock((x + 3 * block_width, y), game)

    x, y = 8314, 548
    for i in range(2):
        BrickBlock((x + i * block_width, y), game)

    pos = (8637, 741)
    xdir = 1
    extra_back_blocks = 0
    blockheight = 4
    create_stair(pos, blockheight, extra_back_blocks, xdir, game)
    pos = (9216, 741)
    xdir = -1
    create_stair(pos, blockheight, extra_back_blocks, xdir, game)
    pos = (9538, 741)
    xdir = 1
    extra_back_blocks = 1
    create_stair(pos, blockheight, extra_back_blocks, xdir, game)
    pos = (10182, 741)
    xdir = -1
    extra_back_blocks = 0
    create_stair(pos, blockheight, extra_back_blocks, xdir, game)

    create_pipe((10505, 676), GameSpecs.Y_GROUND, game)

    x, y = 10828, 548
    BrickBlock((x, y), game)
    BrickBlock((x + block_width, y), game)
    hittable_block = HittableBlock((x + 2 * block_width, y), game)
    hittable_block.add_coins(num_coins)
    BrickBlock((x + 3 * block_width, y), game)

    create_pipe((11536, 676), GameSpecs.Y_GROUND, game)

    pos = (11665, 741)
    xdir = 1
    extra_back_blocks = 1
    blockheight = 8
    create_stair(pos, blockheight, extra_back_blocks, xdir, game)

    x, y = 12761, 741
    create_flagpole((x, y), game)


def create_obstacles(game):
    create_floor_walls_ceiling(game)
    create_platforms(game)


def create_testarea(game):
    block_width, block_length = GameSpecs.BLOCK_SIZE

    for x in range(block_width, GameSpecs.SCREEN_SIZE[0] - 3 * block_width, block_width):
        py = GameSpecs.SCREEN_SIZE[1] - 6 * block_length
        num_coins = 3
        hittable_block = HittableBlock((x, py), game)
        hittable_block.add_coins(num_coins)


def create_enemies(game):
    block_width, block_length = GameSpecs.BLOCK_SIZE
    start_pos1 = (30 * block_width, GameSpecs.Y_GROUND - 100)
    start_pos2 = (3 * block_width, GameSpecs.Y_GROUND - 100)
    GreenKoopaTroopa(start_pos1, game)
    Goomba(start_pos2, game)


class Mgame(object):
    """
    object representing the game/level.
    allows for clean restart functionality.
    """
    def __init__(self):
        self.screen, self.clock = init_game()

        self.bg_img = pygame.image.load('../images/mario_bg_scaled_superCleared.png').convert_alpha()

        self.view_rect = None  # helps keeps mario from moving backwards :(

        self.is_running = True
        self.is_stage_complete = False
        self.is_game_over = False
        self.remaining_time_mario_sec = 400
        # TODO: TRANSFER SCORING TO PLAYER CLASS; better for multiplayer
        self.score = 0
        self.num_coins = 0
        self.num_lives = 3

        self.text_sprites = pygame.sprite.Group()
        screen_w, screen_h = GameSpecs.SCREEN_SIZE

        #self.bg_song = pygame.mixer.Song('/home/daxterix/Desktop/mario_theme.wav')
        pygame.mixer.music.load('../sounds/mario_theme2_converted.mp3')

        self.font = pygame.font.Font('../fonts/SuperMario256.ttf', 26)
        coin_img = pygame.image.load('../images/coin.png').convert_alpha()
        PermanentText("MARIO", (20, 20), self)
        self.score_text = PermanentText(str(self.score).zfill(6), (20, 40), self)
        self.num_coins_text = PermanentText("x" + str(self.num_coins).zfill(2), (screen_w / 3 + 20, 40), self)
        PictureLabel(self.num_coins_text, coin_img, self)
        PermanentText("WORLD", (2 * screen_w / 3 - 40, 20), self)
        PermanentText("1-1", (2 * screen_w / 3 - 10, 40), self)
        self.time_text = PermanentText("TIME", (screen_w - 100, 20), self)
        self.time_text = PermanentText(str(int(self.remaining_time_mario_sec)).zfill(3), (screen_w - 100, 40), self)

        self.player = None
        self.moving_left_wall = None   #set by create obstacles
        self.player_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        # contains moving invisible wall that affects mario only
        self.player_block_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        self.redmushroom_sprites = pygame.sprite.Group()
        self.greenmushroom_sprites = pygame.sprite.Group()
        self.flower_sprites = pygame.sprite.Group()
        self.fireball_sprites = pygame.sprite.Group()
        self.star_sprites = pygame.sprite.Group()
        self.flag_and_pole_sprites = pygame.sprite.Group()

    def increment_num_coins(self):
        self.num_coins += 1
        self.num_coins_text.set_text("x" + str(self.num_coins).zfill(2))

    def increase_score_by(self, amt, pos):
        self.score += amt
        PopupText(str(amt), pos, self)
        self.score_text.set_text(str(self.score).zfill(6))

    def increment_num_lives(self, pos):
        self.num_lives += 1
        PopupText("1-UP", pos, self)

    def decrement_num_lives(self, pos):
        self.num_lives -= 1
        if self.num_lives <= 0:
            self.player.init_game_over()
            #self.game_over()

    def run(self):
        """
        main game loop; creates sprites then
        constantly updates and draws them onto the screen.
        """
        pygame.mixer.music.stop()
        self.show_title_screen()
        pygame.mixer.music.play(-1)

        frames_acc, time_acc, fps = 0, 0, 0
        create_obstacles(self)
        create_enemies(self)

        self.player = Player((0, 0), self)

        while (not self.is_game_over) and (not self.is_stage_complete):
            dt = self.clock.tick(GameSpecs.FPS)  # how long it took to run the loop
            time_acc += dt
            frames_acc += 1
            if time_acc >= 500:
                fps = frames_acc / (time_acc / 500.0)
                # print fps
                time_acc = 0
                frames_acc = 0
                self.remaining_time_mario_sec -= 1
                if self.remaining_time_mario_sec < 0:
                    self.player.init_game_over()
                else:
                    self.time_text.set_text(str(self.remaining_time_mario_sec).zfill(3))
            # TODO: HOW TO DISPLAY FPS ON WINDOW-PANE

            self.check_restart_quit()
            self.update_sprites(dt)
            self.draw_frame()

        pygame.mixer.music.stop()
        self.handle_endgame()

    def handle_endgame(self):
        if self.is_game_over:
            self.show_game_over_screen()
        else:
            # early bird gets the worms
            self.increase_score_by(10 * self.remaining_time_mario_sec, (-50, -100))
            self.show_stage_complete_screen()

    def restart(self):
        """ resets all sprites, effectively restarting the game. """
        self.view_rect = None
        self.is_running = True
        self.is_game_over = False
        self.is_stage_complete = False
        self.num_coins = 0
        self.block_sprites.empty()
        self.player_block_sprites.empty()
        self.player_sprites.empty()
        self.enemy_sprites.empty()
        self.coin_sprites.empty()
        self.redmushroom_sprites.empty()
        self.greenmushroom_sprites.empty()
        self.flower_sprites.empty()
        self.fireball_sprites.empty()
        self.star_sprites.empty()
        self.flag_and_pole_sprites.empty()
        self.run()

    def check_restart_quit(self):
        """ checks if restart or quit buttons were pressed. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    exit_game()

                if event.key == pygame.K_r:
                    self.restart()

    def stage_complete(self):
        self.is_stage_complete = True

    def game_over(self):
        self.is_game_over = True

    def update_sprites(self, dt):
        """ updates all sprites. """
        dt_sec = dt / 1000.0
        self.block_sprites.update(dt_sec)
        self.coin_sprites.update(dt_sec)
        self.redmushroom_sprites.update(dt_sec)
        self.greenmushroom_sprites.update(dt_sec)
        self.flower_sprites.update(dt_sec)
        self.enemy_sprites.update(dt_sec)
        self.player_sprites.update(dt_sec)
        #self.player.update_testing(dt_sec)
        self.fireball_sprites.update(dt_sec)
        self.star_sprites.update(dt_sec)
        self.flag_and_pole_sprites.update(dt_sec)

    def draw_frame(self):
        """ draw all sprites on the the screen. """
        self.view_rect = draw_bg(self.bg_img, self.screen, self.player, self.view_rect)
        view_pos = (self.view_rect.x, self.view_rect.y)

        # set its position to the viewposition
        new_left_boundary = view_pos[0] - self.moving_left_wall.get_size()[0]
        top = self.moving_left_wall.get_position()[1]
        self.moving_left_wall.set_position((new_left_boundary, top))

        # draw all sprites; order matters: consumables
        # should be draw before their containing blocks
        # platform player and enemies should be drawn
        # after moving platforms
        # nothing else to draw for player_block_sprites
        for coin in self.coin_sprites:
            coin.draw(self.screen, view_pos)
        for schroom in self.redmushroom_sprites:
            schroom.draw(self.screen, view_pos)
        for schroom in self.greenmushroom_sprites:
            schroom.draw(self.screen, view_pos)
        for flower in self.flower_sprites:
            flower.draw(self.screen, view_pos)
        for star in self.star_sprites:
            star.draw(self.screen, view_pos)
        for block in self.block_sprites:
            block.draw(self.screen, view_pos)
        for enemy in self.enemy_sprites:
            enemy.draw(self.screen, view_pos)
        for fireball in self.fireball_sprites:
            fireball.draw(self.screen, view_pos)
        for flag_and_pole in self.flag_and_pole_sprites:
            flag_and_pole.draw(self.screen, view_pos)
        self.player.draw(self.screen, view_pos)
        for text in self.text_sprites:
            text.draw(self.screen, view_pos)

        pygame.display.flip()

    def show_title_screen(self):
        frames_remaining = 1000

        small_rest_left = pygame.image.load('../images/smallmariorest_left.png').convert_alpha()
        mario_img = pygame.transform.flip(small_rest_left, True, False)

        screen_w, screen_h = GameSpecs.SCREEN_SIZE
        stage_text = PermanentText("WORLD  1-1", (screen_w / 2 - 50, screen_h/2 - 50), self)
        num_lives_text = PermanentText("    x  " + str(self.num_lives), (screen_w / 2, screen_h/2 + 20), self)
        num_lives_label = PictureLabel(num_lives_text, mario_img, self)

        while frames_remaining > 0:
            self.screen.fill((0, 0, 0))
            for text in self.text_sprites:
                text.draw(self.screen, text.get_position())
            pygame.display.flip()
            frames_remaining -= 1
            self.check_restart_quit()

        stage_text.kill()
        num_lives_text.kill()
        num_lives_label.kill()

    def show_game_over_screen(self):
        x, y = GameSpecs.SCREEN_SIZE
        x = x/2 - 50
        y /= 2
        game_over_text = PermanentText("GAME OVER", (x, y), self)

        frames_remaining = 1000
        while frames_remaining > 0:
            self.screen.fill((0, 0, 0))
            for text in self.text_sprites:
                text.draw(self.screen, text.get_position())
            pygame.display.flip()
            frames_remaining -= 1
            self.check_restart_quit()

        game_over_text.kill()

    def show_stage_complete_screen(self):
        screen_w, screen_h = GameSpecs.SCREEN_SIZE
        x, y = screen_w/2, screen_h/2
        PermanentText("Stage Complete!", (x, 270), self)
        PermanentText("Score\t" + str(self.score).zfill(6), (x, 300), self)
        PermanentText("TOP SCORES", (x, y), self)
        DBUtils.record_new_score(self.score, "Prime User")
        high_scores = DBUtils.get_top_3_scores()
        for score, name in high_scores:
            y += 30
            PermanentText(name.ljust(15) + "\t" + str(score).zfill(6), (x, y), self)

        frames_remaining = 3000
        while frames_remaining > 0:
            self.screen.fill((0, 0, 0))
            for text in self.text_sprites:
                text.draw(self.screen, text.get_position())
            pygame.display.flip()
            frames_remaining -= 1
            self.check_restart_quit()


def init_game():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(GameSpecs.SCREEN_SIZE)
    clock = pygame.time.Clock()
    return screen, clock


def exit_game():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    new_game = Mgame()
    GameSpecs.init(new_game.bg_img.get_size())
    new_game.run()
