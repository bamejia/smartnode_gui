from win32api import GetSystemMetrics


# window variables
WINDOW_NAME = "Racing Game"
WINDOW_X_POS = 300
WINDOW_Y_POS = 100
WINDOW_W_RATIO = 5/8
WINDOW_L_RATIO = 7/8
# WINDOW_W, WINDOW_L = WINDOW_SIZE = round(GetSystemMetrics(0) * WINDOW_W_RATIO),\
#                                                           round(GetSystemMetrics(1) * WINDOW_L_RATIO)
# print(WINDOW_W, WINDOW_L, WINDOW_SIZE)


WINDOW_W, WINDOW_L = WINDOW_SIZE = 1024, 900
# WINDOW_W, WINDOW_L = WINDOW_SIZE = GetSystemMetrics(0), GetSystemMetrics(1)  # for windows

# title screen variables
TITLE_TEXT = "RACING GAME"
TITLE_TEXT_SIZE = 140
TITLE_FONT = None
AUTHOR_TEXT = "by bamxmejia"
AUTHOR_TEXT_SIZE = 80
AUTHOR_FONT = None
BUTTON_TEXTS = (
    "Single Player",
    "Local 2 Player",
    "Online MultiPlayer",
    "Exit"
)
BUTTON_TEXT_SIZE = 75
BUTTON_FONT = None


# colors
WHITE = (255, 255, 255)
VERY_LIGHT_GREY = (170, 170, 170)
BLACK = (0, 0, 0)
BLUE = (0, 0, 150)
TANISH_YELLOW = (255, 255, 100)
BRIGHT_RED = (255,0,0)
RED = (210, 0, 0)
DARK_RED = (125, 0, 0)
YELLOW = (255, 255, 0)
TANISH_GREY = (125, 125, 100)
ORANGE = (255, 120, 0)
DARK_ORANGE = (255, 120, 0)
LIGHT_GREY_BLUE = (125, 150, 150)
PEACH_PINK = (255, 152, 154)
PEACH = (255, 161, 100)
MID_DARK_PEACH = (255, 157, 0)
DARK_PEACH = (238, 138, 49)
BROWN = (185, 113, 62)
TURQOISE = (0, 152, 154)
GREEN = (0, 175, 0)
DARK_GREEN = (0, 100, 40)
TAN = (255, 195, 155)
