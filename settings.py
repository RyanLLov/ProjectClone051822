# game options/settings
TITLE = "WallJumper!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "SpriteImages.png"


# Player properties
PLAYER_ACC = 0.75
PLAYER_FRICTION = -0.12 
PLAYER_GRAVITY = 0.98



# Game Properties
BOOST = 50
POW_SPAWN_RATE = 5
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2


#starting platforms
PLATFORM_LIST = [(0,HEIGHT - 40),
                (WIDTH/2 - 50, HEIGHT * (3/4)),
                (125,HEIGHT - 350),
                (350,200),
                (175,100)
                ]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TAN = (255,179,71)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0,155,155)
BGCOLOR =LIGHTBLUE