import pygame
from math import *

pygame.font.init()

vec2 = pygame.math.Vector2
FPS = 60
BG_COLOR = "black"
GAME_SPEED = 100 # TIME BETWEEN TWO STEP IN THE GAME (IN MILLIS)


SIZE = 32
ROW_NUM, COL_NUM = 20, 20
RES = WIDTH, HEIGHT = vec2(SIZE*(COL_NUM), SIZE*(ROW_NUM))
CENTER = RES // 2
KEYS = KEY_RIGHT, KEY_UP, KEY_LEFT, KEY_DOWN = [pygame.K_d,
                                                pygame.K_z,
                                                pygame.K_q,
                                                pygame.K_s]

COLORS = {"0": "red", "1": "blue", "2": "green", "3": "yellow"}
START_POS = {"0": vec2(5*SIZE, 2*SIZE), # TopLeft
             "1": RES-vec2(5*SIZE, 2*SIZE), # BottomRight
             "2": vec2(WIDTH-2*SIZE, 5*SIZE), # TopRight
             "3": vec2(2*SIZE, HEIGHT-5*SIZE)} #BottomLeft
START_DIR = {"0": 0,
             "1": pi,
             "2": 3*pi/2,
             "3": pi/2}
START_LEN = 3

# GUI FONTS
FONT_GUI = pygame.font.Font('Fonts/PixelFont.TTF', 16)
FONT_GUI2 = pygame.font.Font('Fonts/PixelFont.TTF', 24)
FONT_GUI3 = pygame.font.Font('Fonts/PixelFont.TTF', 32)
FONT_MENU = pygame.font.Font('Fonts/PixelFont.TTF', 48)
FONT_GAMEOVER = pygame.font.Font('Fonts/PixelFont.TTF', 128)

# GUI OBJECTS ATTR
BORDER_BUTTON_SIZE = 2
BUTTON_MARGIN = 16
ACTIVE_COLOR_BUTTON = pygame.color.Color('gray5')
INACTIVE_COLOR_BUTTON = pygame.color.Color('gray0')
TEXT_COLOR_BUTTON = "white"
OUTLINE_COLOR_BUTTON = "white"

BORDER_ENTRY_SIZE = 8
ENTRY_MARGIN = 16
BACK_COLOR_ENTRY = "black"
OUTLINE_COLOR_ENTRY = "white"
TEXT_COLOR_ENTRY = "white"

BORDER_LABEL_SIZE = 4
LABEL_MARGIN = 16
BACK_COLOR_LABEL = "white"
OUTLINE_COLOR_LABEL = "black"
TEXT_COLOR_LABEL = "black"

BORDER_TABLE_SIZE = 2
TABLE_MARGIN = 16
BACK_COLOR_TABLE = pygame.color.Color('gray5')
HEADBACK_COLOR_TABLE = pygame.color.Color('gray0')
OVERFLY_COLOR_TABLE = pygame.color.Color('gray10')
OUTLINE_COLOR_TABLE = "white"
TEXT_COLOR_TABLE = "white"
