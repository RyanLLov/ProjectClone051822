
import pygame as pg
from settings import *
from random import choice, randrange
vec = pg.math.Vector2

class Spritesheet:
    #utility class for loading and parsing spritesheets
    def __init__(self,filename)  :
        self.spritesheet = pg.image.load(filename).convert()
         
    def get_image(self,x,y,width,height):
        '''
        What this function does:
            * This function grab an image out of the larger spritesheet SpriteImages.png
        '''
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        image = pg.transform.scale(image,(width//2,height//2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0 
        self.load_images()
        self.image = self.game.spritesheet.get_image(119,1,100,133)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.position = vec(WIDTH//2 - 25,350 )
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def load_images(self):
        '''
        What this function does:
            * In this function we are loading the two images of my character, a standing image
                and a jumping image.
            * For frame in self.jumping_frames just changes the background of the image to clear
        '''
        self.jumping_frames = [self.game.spritesheet.get_image(119,1,100,133),
                               self.game.spritesheet.get_image(1,1,116,131)]
        for frame in self.jumping_frames:
            frame.set_colorkey(WHITE)
        
        self.jump_frames_loading = []
        for frame in self.jumping_frames:
            self.jump_frames_loading.append(pg.transform.flip(frame,True,False))
        
    def jump_cut(self):
        '''
        What this function does:
            * If the player doesn't hold the button down (just presses the button and instantly lets go)
            * The player's velocity in the Y direction goes up 3.
        '''
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3


    def jump(self):
        '''
        What this function does:
            * This function allows the player to jump only if they are on a platform.
            * It also plays the players jump sound. The jump velocity is 25
        '''
        # jump only if standing on a platform
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -25


    def update(self):
        '''
        What this function does:
            * Calls self.animate function
            * Updates the self.acc to the velocity of (0 in the X direction,
                and gravity in the Y direction)
            * This function also applies physics (acceleration, velocity, and friction)
            * If the player's position goes off screen to the right,
                the player will appear on the left and Vice Versa
        '''
        self.animate()
        self.acc = vec(0,PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        
        # applies friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #equation of motion physics 
        self.vel += self.acc
        self.position += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.position.x > WIDTH + self.rect.width / 2: 
            self.position.x = 0 - self.rect.width / 2
        if self.position.x < 0 - self.rect.width / 2:
            self.position.x = WIDTH + self.rect.width / 2
            
        self.rect.midbottom = self.position

    def animate(self):
        '''
        What this function does:
            * Animates the player image whenever the player jumps.
        '''
        now = pg.time.get_ticks()
        if self.vel.y < 0:
            self.jumping = True
        else:
            self.jumping = False

        if self.jumping:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame =  (self.current_frame + 1) % len(self.jumping_frames)
                self.image = self.jumping_frames[self.current_frame]

class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        '''
        What this function does:
            * Platform class that adds each platform to a spritegroup.
            * Has two images and calls the powerup class to randomly spawn at a certain
                spawn rate
        '''
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image(221,1,51,248),
                  self.game.spritesheet.get_image(274,1,47,246)]

        self.image = choice(images)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_RATE:
            PowerUps(self.game,self)


class PowerUps(pg.sprite.Sprite):
    def __init__(self,game,plat):
        '''
        What this function does:
            * Basic initialization of the powerUps class
            * Power up class displays the powerup(grapes image) sets the image background to clear
        '''
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['Boost'])
        self.image = self.game.spritesheet.get_image(414,1,124,114)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    
    def update(self):
        '''
        What this function does:
            * Puts the power up the top center of each platform
        '''
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        '''
        What this function does:
            * Mob class has 2 images for 1 mob(enemy) that it iterates through to show animation
        '''
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image1 = self.game.spritesheet.get_image(943,1,99,114)
        self.image1.set_colorkey(WHITE)
        self.image2 = self.game.spritesheet.get_image(1044,1,88,107)
        self.image2.set_colorkey(WHITE)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
            
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        '''
        What this function does:
            * Moves the mob in the x direction
            * If mob hits a certain Y position, it will do the opposite and vice
                versa in order to get a bobbing affect of the mob.
        '''
        self.rect.x += self.vx
        self.vy += self.dy
        
        
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.rect.centerx > -100:
            if self.dy < 0:
                self.image = self.image1
            else:
                self.image = self.image2
        elif self.rect.centerx < WIDTH + 100:
            if self.dy < 0:
                self.image = pg.transform.flip(self.image1,True,False)
            else:
                self.image = pg.transform.flip(self.image2,True,False)    
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()