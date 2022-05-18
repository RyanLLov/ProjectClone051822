# game options/settings
TITLE = "WallJumper!"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12 
PLAYER_GRAVITY = 0.8

#starting platforms
PLATFORM_LIST = [(0,HEIGHT - 40, WIDTH, 40),
                (WIDTH/2 - 50, HEIGHT * (3/4),10,150),
                (125,HEIGHT - 350, 10, 75),
                (350,200,10,100),
                (175,100,10,120)
                ]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0,155,155)
BGCOLOR =LIGHTBLUE