import pygame
from GGlobals import *


class DrawableSprite(pygame.sprite.Sprite):
    """
    generic sprite meant to be drawn relative to player
    contains useful hook methods
    """

    def __init__(self, position, game):
        super(DrawableSprite, self).__init__()

        self.start_pos = position
        self.game = game
        self.rect = None
        self.prev_rect = None
        self.image = None
        self.prev_image = None

        self.is_alive = True
        self.is_dead = False

        self.frame_counter = 0
        self.image_index = 0

    def get_position(self):
        return self.rect.x, self.rect.y

    def set_position(self, position):
        self.rect.x, self.rect.y = position

    def get_size(self):
        return self.rect.width, self.rect.height

    def get_collision_rect(self):
        return self.rect

    def get_prev_collision_rect(self):
        return self.prev_rect

    @staticmethod
    def is_overlapped_x(rect1, rect2):
        if rect1.left == rect2.left and rect1.right == rect2.right:
            return True

        """ note the strict comparisons: important! """
        if rect1.width > rect2.width:
            return (rect1.left <= rect2.left < rect1.right or
                    rect1.left <= rect2.right < rect1.right)
        else:
            return (rect2.left <= rect1.left < rect2.right or
                    rect2.left <= rect1.right < rect2.right)

    @staticmethod
    def is_overlapped_y(rect1, rect2):
        if rect1.top == rect2.top and rect1.bottom == rect2.bottom:
            return True

        """ note the strict comparisons: important! """
        if rect1.height > rect2.height:
            return (rect1.top <= rect2.top < rect1.bottom or
                    rect1.top <= rect2.bottom < rect1.bottom)
        else:
            return (rect2.top <= rect1.top < rect2.bottom or
                    rect2.top <= rect1.bottom < rect2.bottom)

    def init_rect(self):
        """
        called after image is first initialized to create and
        set rectangle size according to image size
        """
        self.rect = pygame.rect.Rect(self.start_pos, self.image.get_size())
        self.prev_rect = self.rect

    def join_sprite_group(self, sprite_group):
        self.add(sprite_group)

    def end_of_animation_series_handler(self):
        if self.is_alive == 0:
            self.is_dead = 1

    # TODO: generalize with handlers?
    def update_image_from_series(self, valid_imgs, end_of_series_handler=None):
        """
        sets our image to the correct image in the series
        if the sprite is not alive (rolling through death animation)
        and reaches the end of the animation image series, we
        set the sprite's is_dead flag
        """
        if end_of_series_handler is None:
            end_of_series_handler = self.end_of_animation_series_handler

        if self.prev_image not in valid_imgs:
            self.frame_counter = 0
            self.image_index = 0

        if self.frame_counter > GameSpecs.NUM_FRAMES_PER_IMAGE:
            self.frame_counter = 0
            if self.image_index == len(valid_imgs) - 1:
                end_of_series_handler()
            self.image_index = (self.image_index + 1) % len(valid_imgs)
        self.frame_counter += 1
        self.update_image(valid_imgs[self.image_index])

    def update_image(self, new_image):
        """
        given an images, sets it to the current image and updates
        self.prev_image
        """
        self.prev_image = self.image
        self.image = new_image

    def draw(self, screen_surface, view_pos):
        """
        given view_pos, the player's position, draws the block
        on the scr_surface relative to the player's position
        """
        if self.image is None:
            return
        xv, yv = view_pos
        x, y = self.rect.x, self.rect.y
        pos_on_scr = (x - xv, y - yv)
        screen_surface.blit(self.image, pos_on_scr)
