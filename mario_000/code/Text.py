import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, text, position, game, color):
        super(Text, self).__init__(game.text_sprites)
        self.x, self.y = position
        self.text = str(text)
        self.game = game
        self.color = color

    def set_text(self, new_text):
        self.text = str(new_text)

    def set_color(self, new_color):
        self.color = new_color

    def draw(self, surface, view_pos):
        pass

    def get_position(self):
        return self.x, self.y


class PopupText(Text):
    def __init__(self, text, position, game, color=(255, 255, 255)):
        super(PopupText, self).__init__(text, position, game, color)
        self.remaining_screen_time = 30  # in number of frames

    def draw(self, surface, view_pos):
        self.remaining_screen_time -= 1
        if self.remaining_screen_time == 0:
            self.kill()

        xv, yv = view_pos
        pos_on_scr = (self.x - xv, self.y - yv)
        self.y -= 3
        rendered_text = self.game.font.render(self.text, True, self.color)
        surface.blit(rendered_text, pos_on_scr)


class PermanentText(Text):
    def __init__(self, text, position, game, color=(255, 255, 255)):
        super(PermanentText, self).__init__(text, position, game, color)

    def draw(self, surface, view_pos):
        pos_on_scr = (self.x, self.y)
        rendered_text = self.game.font.render(self.text, True, self.color)
        surface.blit(rendered_text, pos_on_scr)


class PictureLabel(pygame.sprite.Sprite):
    """assumed for permanent text only"""
    def __init__(self, main_text, image, game):
        super(PictureLabel, self).__init__(game.text_sprites)
        self.main_text = main_text
        self.image = image
        self.game = game

    def get_position(self):
        return self.main_text.get_position()

    def draw(self, surface, view_pos):
        x, y = self.get_position()
        pos_on_scr = (x - 50, y-20)
        surface.blit(self.image, pos_on_scr)



