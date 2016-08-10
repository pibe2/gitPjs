class GameSpecs:
    SCREEN_SIZE = (1000, 900)
    BLOCK_SIZE = (64, 64)
    WORLD_SIZE = (0, 0)
    Y_GROUND = 805
    FPS = 60
    # pixel convention: down is +
    GRAVITY = 1600
    JUMP_VEL = -1000
    NUM_FRAMES_PER_IMAGE = 6

    @staticmethod
    def init(bg_image_size):
        GameSpecs.WORLD_SIZE = bg_image_size


# makeshift enums for ImageSize and X direction
class ImageSize:
    SMALL = 0
    LARGE = 1

class Direction:
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    HORIZONTAL = 4
    VERTICAL = 6

class Utils:
    # so integer truncation doesn't leave us with 0
    @staticmethod
    def custom_int_round(raw_val):
        if int(raw_val) == 0 and raw_val != 0:
            if raw_val > 0:
                return 1
            else:
                return -1
        else:
            return int(raw_val)


