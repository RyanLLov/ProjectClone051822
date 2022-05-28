# PixelBear Art by https://opengameart.org/content/pixel-bear-infinite-jumper-app-game
# Jump and Run (inGameMusic.ogg) by https://opengameart.org/content/jump-and-run-8-bit

import pygame as pg
import random
from settings import *
from spriteImages import *
from os import path 


class Game:
    def __init__(self):
        # initialize game window, etc
        '''
        What this function does:
            *Initializes pygame
            *creates the screen with sizes WIDTH and HEIGHT
            *changes the name of the screen
            *creates the frames per second for the game
            *changes the Font of the text

        '''
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self): 
        '''
        What this function does:    
            * File directory for Images and joins it to the Highscore file
            * File directory for Sounds and joins it with the folder sounds
            * We are then able to read, write, and update the high score of the player
            * Loads in the Player's jump sound
        '''
        #load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir,"Images")
        with open(path.join(self.dir,HS_FILE), 'w') as f:
            try: 
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.spritesheet = Spritesheet(path.join(img_dir,SPRITESHEET))
        #load sounds
        self.Sounds_dir = path.join(self.dir, 'Sounds')
        self.jump_sound = pg.mixer.Sound(path.join(self.Sounds_dir, 'JumpSound.ogg'))


    def new(self):
        # start a new game
        '''
        What this function does:
            * Initializes all the sprite groups
            * Runs through the PLATFORM_LIST
            * Calls the platform Class to create the platforms
            * Loads the in game music
        '''
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self,*plat)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.Sounds_dir, 'inGameMusic.ogg'))
        self.run()

    def run(self):
        '''
        What this function does:
            *This function calls other functions
                * events
                * update
                * draw
            * It also sets all music to loop and fades out after 1000 milliseconds
        '''
        # Game Loop
        pg.mixer.music.play(loops=-1) 
        self.playing = True
        while self.playing:
            self .clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)

    def update(self):
        '''
        *What this function does:
            * This function updates all the sprites in the game.
            * It checks when to spawn a mob, when the player collides with a mob,
            * Checks to see if the player hits a platform
            * Checks if the player reaches a certain height limit 
                to increase the scrolling of the game.
            * It also checks to see if the player got a power up
            * Checks to see if the player dies, it should end the game.
            * There is also a random platform generation in this function

        '''
        # Game Loop - Update
        self.all_sprites.update()

        # Spawn a mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.randrange(-500,500):
            self.mob_timer = now
            Mob(self)

        #mob collision
        mob_hits = pg.sprite.spritecollide(self.player,self.mobs, False)
        if mob_hits: 
            self.playing = False


        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.position.x < lowest.rect.right + 10 and \
                    self.player.position.x > lowest.rect.left - 10:
                    self.player.position.y = lowest.rect.top
                    self.player.vel.y += 0.25 
                    self.player.jumping = False
            
        # if player reachers top 1/4 of screen
        if self.player.rect.top <= HEIGHT/4:
            self.player.position.y += max(abs(self.player.vel.y),2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.rect.top>= HEIGHT:
                    plat.kill() 
                    self.score += 10

        # if player gets a powerup
        pow_hits = pg.sprite.spritecollide(self.player,self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'Boost':
                self.player.vel.y = -BOOST
                self.player.jumping = False
            
        # Die/ End game
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y,10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        #spawn new platforms to keep same average number of platforms
        while len(self.platforms) < 6:
            width = random.randrange(80,120)
            #Platform(x,y,width,height)
            Platform(self, random.randrange(20, WIDTH - width),
                         random.randrange(-75,0) )

    def events(self):
        '''
        What this function does:
            * This function takes in the users input from Space and QUIT
            * If they hit the close button the game ends.
            * If they push down the space button, or if they hold the space
                button for a longer duration
        '''
        # Game Loop - events
        for event in pg.event.get():
            # check for cl osing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut() 

    def draw(self):
        '''
        What this function does:
            * Function draws(blits) all sprites onto the screen
            * Flips all the images that have been drawn
        '''
        # Game Loop - draw 
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),22,WHITE,WIDTH / 2, 30)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        '''
        Start menu function:
            * In the start menu, we automatically start playing the menu song.
            * Setting the background color and drawing/sizing the text.
            * Music Fades out when we press any button to start the game
        '''
        # game splash/start screen
        # pg.mixer.music.load(path.join(self.Sounds_dir, 'StartMenu.mp3'))
        # pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE,48, WHITE, WIDTH / 2 ,HEIGHT / 4)
        self.draw_text("WASD to move, SPACE BAR to jump", 22, WHITE,
                        WIDTH / 2, HEIGHT / 2)
        self.draw_text("Directions:",15, WHITE, WIDTH / 2 , HEIGHT * (1/3) - 35)
        self.draw_text("A moves left",15, WHITE, WIDTH / 2 , HEIGHT*(1/3) - 20)
        self.draw_text("D moves right",15, WHITE, WIDTH / 2 , HEIGHT*(1/3)- 5)
        self.draw_text("Space jumps up",15, WHITE, WIDTH / 2 , HEIGHT*(1/3) + 10)

        self.draw_text ("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * (3 / 4))
        self.draw_text("High Score: " + str(self.highscore),22,WHITE,WIDTH/2 , 35)

        pg.display.flip()
        self.wait_for_key() 
        pg.mixer.music.fadeout(1000)

    def show_gameover_screen(self):
        '''
        Game Over screen:
            * Displays itself whenever the character dies.
            * There is also music on this screen that loops and plays the same music as
                the menu. 
            * Displays the game over text and asks to see if the player
                would like to play again.
            * Displays the players Highscore from the highscore file.
        '''
        # game over/continue
        if not self.running:
            return
        # pg.mixer.music.load(path.join(self.Sounds_dir, 'StartMenu.mp3'))
        #pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("Game Over! You died",48, WHITE, WIDTH / 2 ,HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE,
                        WIDTH / 2, HEIGHT / 2)

        self.draw_text("Directions:",15, WHITE, WIDTH / 2 , HEIGHT * (1/3) - 35)
        self.draw_text("A moves left",15, WHITE, WIDTH / 2 , HEIGHT*(1/3) - 20)
        self.draw_text("D moves right",15, WHITE, WIDTH / 2 , HEIGHT*(1/3)- 5)
        self.draw_text("Space jumps up",15, WHITE, WIDTH / 2 , HEIGHT*(1/3) + 10)
        
        self.draw_text ("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * (3 / 4))
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir,HS_FILE),'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore),22,WHITE,WIDTH/2 , HEIGHT / 2 + 40)
 
        pg.display.flip()
        self.wait_for_key() 
        pg.mixer.music.fadeout(1000)

    def wait_for_key(self):
        '''
        What this function does:
            * This is used to see if the player has pushed any button to start
                the game.
    
        '''
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
        '''
        What this function does:    
            * Draws text with the font and renders the font at a certain x/y position
        '''
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
