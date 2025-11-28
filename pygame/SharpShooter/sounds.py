import pygame

pygame.init() # initialize pygame
w_width = 500 # window width
w_height = 500 # window height
screen = pygame.display.set_mode((w_width,w_height)) # set screen to display pygame
pygame.display.set_caption("Adding sound effects") # set caption for the screen

clock = pygame.time.Clock() # creates a Clock object. - is used to control the speed of your game loop, so the game runs smoothly and consistently on all computers.
bg_img = pygame.image.load("images/bg_img.jpeg") # since it is relative path (the image is present in our project directory)
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))
# soldier
walkRight = [pygame.image.load(f'soldier/{i}.png') for i in range(1,10)]
walkLeft = [pygame.image.load(f'soldier/L{i}.png') for i in range(1,10)]
char = pygame.image.load('soldier/standing.png')
# enemy
moveLeft = [pygame.image.load(f'enemy/L{i}.png') for i in range(1,10)]
moveRight = [pygame.image.load(f'enemy/R{i}.png') for i in range(1,10)]
# text
font = pygame.font.SysFont("helvatica", 30, 1, 1)
score = 0
# sound
bulletSound = pygame.mixer.Sound("sounds/Bulletsound.mp3")
hitSound = pygame.mixer.Sound("sounds/Hit.mp3")
music = pygame.mixer.music.load("sounds/music.mp3") # different class to load music
pygame.mixer.music.play(-1)# to specify the number of times the music you want to play - -1 to play repeatedly
pygame.mixer.music.set_volume(0.3) # to set the volume of the music

# projectiles
class projectile():
    def __init__(self, x, y, radius, color, direction, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = direction*vel # direction should be multiplied - otherwise the soldier will shoot in only one direction

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)

# creating soldier and his functions
class player():
    def __init__(self, x, y, width, height):
        self.x=x # x cordinate of rect
        self.y=y # y cordinate of rect
        self.width = width # height and width of rect
        self.height = height
        self.vel = 5 # velocity of rect to move
        # jump variables
        self.is_jump = False # jump logic is in notepad notes
        self.jump_count = 10 # height at which the object jumps
        # character
        self.left = False # moving left
        self.right = False # moving right
        self.walkCount = 0 # steps count
        self.standing = True # standing or not - for the standing direction
        # hitbox
        self.hitbox = (self.x,self.y,self.width,self.height) # a rectange surrounding the character to detect collision - adding and subracting values are to make the collision box precise - experimental values
        self.hit = pygame.Rect(self.hitbox) # is a bulitin function of pygame which is commonly used in collision detection and rectangle positioning

    def draw(self, screen):
        if self.walkCount+1 >= 27: # out of 9 images, when it reaches the last image, then it should start from the begining image - 3*9 = 27
            self.walkCount = 0
        if not(self.standing):
            if self.left: # if left key is clicked
                screen.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x,self.y)) # to make the movement smooth, we don't want the game to blited too fast - we'll make sure every image is shown 3 times before the next image is shown - so we multiply walk count by 3 results in 27 - floor div the walkRight(walkCount) by 3
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x,self.y)) # to make the movement smooth, we don't want the game to blited too fast - we'll make sure every image is shown 3 times before the next image is shown - so we multiply walk count by 3 results in 27 - floor div the walkRight(walkCount) by 3
            else:
                screen.blit(walkLeft[0], (self.x,self.y))
        
        self.hitbox = (self.x,self.y,self.width,self.height) # writing here, so that the values are upadated according to the current position
        # pygame.draw.rect(screen, "black", self.hitbox, 2)
        self.hit = pygame.Rect(self.hitbox)

    def touch(self):
        hitSound.play()# hit sound play
        self.x = 0
        self.y = w_height - self.height # if we stop the code till this - the jump logic keeps decreasing self.y and never resets the vertical velocity if the player is already on the ground after a collision. - So the moment you collide while mid-air: - touch() forces you to ground (y = 436) - Jump logic is still active OR jump_count is at a wrong value - Gravity code continues pushing the player downward - → Player goes below screen
        self.is_jump = False
        self.jump_count = 10


# Enemy
class enemy():
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0 # which image in the walking animation is displayed
        self.vel = 3 # enemy's vel
        self.path = [x,end] # the path of enemy - enemy moves from x to end
        self.hitbox = (self.x+20,self.y,self.width-40,self.height-4)
        self.hit = pygame.Rect(self.hitbox)
        self.health = 9
        self.visible = True # enemy alive or not

    # draw enemy images based on movement
    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount+1 >= 27: # out of 9 images, when it reaches the last image, then it should start from the begining image - 3*9 = 27
                self.walkCount = 0
            #if not(self.standing): no need for this, coz the character will be constantly moving in the screen
                # The main difference b/2 player and enemy is that the enemy will be constantly moving no the screen - wheras the player can stand in stationary - i.e you don't need to press any key to make the enemy move
            # no need for key checks
            if self.vel > 0: # if enemy got possitive vel - moving in positive direction - we display elts from walk right
                screen.blit(moveRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else: # else display elts from walkLeft
                screen.blit(moveLeft[self.walkCount//3], (self.x,self.y)) # to make the movement smooth, we don't want the game to blited too fast - we'll make sure every image is shown 3 times before the next image is shown - so we multiply walk count by 3 results in 27 - floor div the walkRight(walkCount) by 3
                self.walkCount += 1

            self.hitbox = (self.x+20,self.y,self.width-40,self.height-4) # writing here, so that the values are upadated according to the current position
            # pygame.draw.rect(screen, "black", self.hitbox, 2) # no need to show the hitbox
            self.hit = pygame.Rect(self.hitbox)
            pygame.draw.rect(screen, "grey", (self.hitbox[0],self.hitbox[1]+3, 50, 10),0) # Entire healthbar - 3 is an offset value so that the health bar won't touches the enemy
            pygame.draw.rect(screen, "green", (self.hitbox[0],self.hitbox[1]+3, 50-(5.5*(9-self.health)), 10),0) # remaining health bar

    # movement
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.width + 20: # the enemy will move till end-width - the player won't touch the end of the screen because of the condition - to make him touch the screen we'll add + 20 pixels in the condition
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - 20: # since we added 20 in the if to reach end, we'll subract 20 so that it reaches the left end - 20 is a experimental value only
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def touch(self):
        hitSound.play()# hit sound play
        if self.health > 0:
            self.health -= 1 
        else:
            self.visible = False

# game display loop
def DrawInGameLoop():
    global bg_img
    screen.blit(bg_img, (0,0)) # blit is used to display images in pygame - if you run it will not get the full image - coz the dimensions of the window is not same as dimension of the image
    
    clock.tick(25) # this tells Pygame - "Run this loop at most 60 times per second." - This is called FPS (Frames Per Second).
    # Without clock.tick(60), your game loop runs as fast as your CPU allows (maybe 3000+ FPS).
    soldier.draw(screen)
    text = font.render("Score: " + str(score), 1, "red") # to render font on a surface - 1 sets the True value for sharpening edges of the characters
    screen.blit(text,(0,10))
    enemy.draw(screen)
    for bullet in bullets:
        bullet.draw()
    pygame.display.flip()

# creating objects
soldier = player(250,435,64,64) # soldier object
enemy = enemy(0, w_height-64, 64, 64, w_width) # enemy object
bullets = [] # bullet object
shoot = 0 # delay b/w bullets - to not stick together

# game loop
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    if enemy.visible:
        if soldier.hit.colliderect(enemy.hit):
            enemy.vel *= -1
            soldier.touch()

    if shoot > 0: # check shoot is greater than 0, if yes adds one to it, untill it becomes 4
        shoot += 1
    if shoot > 3: # checks shoot is 4 or more and assigns it back to 0
        shoot = 0

    for bullet in bullets:
        if enemy.visible:
            # collision of bullet on enemy
            if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y - bullet.radius > enemy.hitbox[1]: # bullet is in horizontal range of the enemy
                if bullet.x - bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]: # bullet is in vertical range - intersection is - the bullet is in the enemy
                    bullets.pop(bullets.index(bullet)) # remove the bullet from the list - coz it is no longer there after hitting the enemy
                    score += 1
                    enemy.touch()

        if bullet.x < 500 and bullet.x > 0: # centre of bullet - if it is inside the window
            bullet.x += bullet.vel # change the bullet position occording to velocity
        else: # if it goes out of window
            bullets.pop(bullets.index(bullet)) # remove the bullet from the list

    keys = pygame.key.get_pressed() # returns bool, corresponds to all the keys of keyboard, initially it returns all false, once a key is pressed - its value becomes true, until it is pushed

    # If Space key is pressed
    if keys[pygame.K_SPACE] and shoot == 0: # check if shoot is 0 (space pressed for the first time), if yes bullet is projected else game loop runs until the shoot becomes 0 (delay)
        if soldier.right:
            direction = 1 # vel is negative, bullet moves left side
        else:
            direction = -1 # vel is positive, bullet moves right side

        if len(bullets) < 5:# bullet limit - max no. of bullet a player can shoot at a time
            bulletSound.play()# Bullet sound play
            bullets.append(projectile((soldier.x+soldier.width//2),(soldier.y+soldier.width//2),6,"black",direction,5))
        shoot = 1 # is shoot is 0, it becomes one and the game loop runs until it becomes 4 (which is made by the loop in the begining)
    
    # If left key is pressed
    if keys[pygame.K_LEFT] and soldier.x>0:
        soldier.x-=soldier.vel
        soldier.left = True
        soldier.right = False
        soldier.standing = False
    # If left key is pressed
    elif keys[pygame.K_RIGHT] and soldier.x<w_width-soldier.width:
        soldier.x+=soldier.vel
        soldier.left = False
        soldier.right = True
        soldier.standing = False
    # If none of the functional key is pressed
    else:
        soldier.standing = True
        soldier.walkCount = 0
    if not(soldier.is_jump):
        # no need for the chracter to move up and down
        # if keys[pygame.K_UP] and y>0:
        #     y-=vel
        # if keys[pygame.K_DOWN] and y<w_height-height: # (window height - height of rect), is the max value the y cord of rect can take
        #     y+=vel
        if keys[pygame.K_UP]:
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:
        if soldier.is_jump:
            if soldier.jump_count >= -10:
                neg = 1
                if soldier.jump_count < 0:
                    neg = -1
                soldier.y -= (soldier.jump_count ** 2)*neg*0.5
                soldier.jump_count -= 1
            else:
                soldier.jump_count=10
                soldier.is_jump=False
    # condition that will never allow the player to go below the ground
    if soldier.y > w_height - soldier.height:
        soldier.y = w_height - soldier.height
    # enemy.move() # calling move function of enemy to make it move
    DrawInGameLoop()

    
pygame.quit