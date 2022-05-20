import pygame as pg
import random
from settings import *
from Sprites import *
from os import path

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        #load high score
        self.dir = path.dirname(__name__)
        with open(path.join(self.dir,HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0



    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # checks if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms,False)
            if hits:
                self.player.position.y = hits[0].rect.top
                self.player.vel.y = 0 
        
       
        # if player reachers top 1/4 of screen
        if self.player.rect.top <= HEIGHT/4:
            self.player.position.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top>= HEIGHT:
                    plat.kill()
                    self.score += 10

        # Die/ End game
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y,10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False


        #spawn new platforms to keep same average number of platforms
        while len(self.platforms) < 4:
            width = random.randrange(80,120)
            #Platform(x,y,width,height)
            p = Platform(random.randrange(20, WIDTH - width),
                         random.randrange(-75,0),
                         10,width)
            self.platforms.add(p)
            self.all_sprites.add(p)


            


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),22,WHITE,WIDTH / 2, 30)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE,48, WHITE, WIDTH / 2 ,HEIGHT / 4)
        self.draw_text("WASD to move, SPACE BAR to jump", 22, WHITE,
                        WIDTH / 2, HEIGHT / 2)
        self.draw_text ("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * (3 / 4))
        pg.display.flip()
        self.wait_for_key() 

    def show_gameover_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("Game Over! You died",48, WHITE, WIDTH / 2 ,HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE,
                        WIDTH / 2, HEIGHT / 2)
        self.draw_text ("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * (3 / 4))
        pg.display.flip()
        self.wait_for_key() 



    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type ==pg.KEYUP:
                    waiting = False
    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midbottom = (x,y)
        self.screen.blit(text_surface,text_rect)
#main running loop for game
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_gameover_screen()

pg.quit()
