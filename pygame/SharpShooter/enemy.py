import pygame

pygame.init() # initialize pygame
w_width = 500 # window width
w_height = 500 # window height
screen = pygame.display.set_mode((w_width,w_height)) # set screen to display pygame
pygame.display.set_caption("Adding enemies") # set caption for the screen

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
    
    # draw enemy images based on movement
    def draw(self, screen):
        self.move()
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

    # movement
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.width + 100: # the enemy will move till end-width - the player won't touch the end of the screen because of the condition - to make him touch the screen we'll add + 20 pixels in the condition
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - 100: # since we added 20 in the if to reach end, we'll subract 20 so that it reaches the left end
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
# game display loop
def DrawInGameLoop():
    global bg_img
    screen.blit(bg_img, (0,0)) # blit is used to display images in pygame - if you run it will not get the full image - coz the dimensions of the window is not same as dimension of the image
    
    clock.tick(25) # this tells Pygame - "Run this loop at most 60 times per second." - This is called FPS (Frames Per Second).
    # Without clock.tick(60), your game loop runs as fast as your CPU allows (maybe 3000+ FPS).
    soldier.draw(screen)
    enemy.draw(screen)
    for bullet in bullets:
        bullet.draw()
    pygame.display.flip()

# creating objects
soldier = player(50,435,64,64) # soldier object
enemy = enemy(0, w_height-64, 64, 64, w_width) # enemy object
bullets = [] # bullet object
shoot = 0 # delay b/w bullets - to not stick together

# game loop
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    
    if shoot > 0: # check shoot is greater than 0, if yes adds one to it, untill it becomes 4
        shoot += 1
    if shoot > 3: # checks shoot is 4 or more and assigns it back to 0
        shoot = 0

    for bullet in bullets:
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

    # enemy.move() # calling move function of enemy to make it move
    DrawInGameLoop()

    
pygame.quit