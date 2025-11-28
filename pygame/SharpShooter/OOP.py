import pygame

pygame.init() # initialize pygame
w_width = 500 # window width
w_height = 500 # window height
screen = pygame.display.set_mode((w_width,w_height)) # set screen to display pygame
pygame.display.set_caption("Moving and animating sprites") # set caption for the screen

clock = pygame.time.Clock() # creates a Clock object. - is used to control the speed of your game loop, so the game runs smoothly and consistently on all computers.
bg_img = pygame.image.load("images/bg_img.jpeg") # since it is relative path (the image is present in our project directory)
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))
walkRight = [pygame.image.load(f'soldier/{i}.png') for i in range(1,10)]
walkLeft = [pygame.image.load(f'soldier/L{i}.png') for i in range(1,10)]
char = pygame.image.load('soldier/standing.png')

# creating object
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

    def draw(self, screen):
        if self.walkCount+1 >= 27: # out of 9 images, when it reaches the last image, then it should start from the begining image - 3*9 = 27
            self.walkCount = 0
        if self.left: # if left key is clicked
            screen.blit(walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            screen.blit(walkRight[self.walkCount//3], (self.x,self.y)) # to make the movement smooth, we don't want the game to blited too fast - we'll make sure every image is shown 3 times before the next image is shown - so we multiply walk count by 3 results in 27 - floor div the walkRight(walkCount) by 3
            self.walkCount += 1
        else:
            screen.blit(char,(self.x,self.y))
# game display loop
def DrawInGameLoop():
    global bg_img
    screen.blit(bg_img, (0,0)) # blit is used to display images in pygame - if you run it will not get the full image - coz the dimensions of the window is not same as dimension of the image
    
    clock.tick(25) # this tells Pygame - "Run this loop at most 60 times per second." - This is called FPS (Frames Per Second).
    # Without clock.tick(60), your game loop runs as fast as your CPU allows (maybe 3000+ FPS).
    soldier.draw(screen)
    pygame.display.flip()

soldier = player(50,435,64,64)

# game loop
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    
    keys = pygame.key.get_pressed() # returns bool, corresponds to all the keys of keyboard, initially it returns all false, once a key is pressed - its value becomes true, until it is pushed

    if keys[pygame.K_LEFT] or keys[pygame.K_a] and soldier.x>0:
        soldier.x-=soldier.vel
        soldier.left = True
        soldier.right = False
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and soldier.x<w_width-soldier.width:
        soldier.x+=soldier.vel
        soldier.left = False
        soldier.right = True
    else:
        soldier.left = False
        soldier.right = False
        soldier.walkCount = 0
    if not(soldier.is_jump):
        # no need for the chracter to move up and down
        # if keys[pygame.K_UP] and y>0:
        #     y-=vel
        # if keys[pygame.K_DOWN] and y<w_height-height: # (window height - height of rect), is the max value the y cord of rect can take
        #     y+=vel
        if keys[pygame.K_SPACE]:
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

    DrawInGameLoop()

    
pygame.quit