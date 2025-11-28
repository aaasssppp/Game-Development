import pygame

pygame.init() # initialize pygame
w_width = 500 # window width
w_height = 500 # window height
screen = pygame.display.set_mode((w_width,w_height)) # set screen to display pygame
pygame.display.set_caption("Moving and animating sprites") # set caption for the screen

# creating object
x=50 # x cordinate of rect
y=435 # y cordinate of rect
width = 64 # height and width of rect
height = 64
vel = 5 # velocity of rect to move
clock = pygame.time.Clock() # creates a Clock object. - is used to control the speed of your game loop, so the game runs smoothly and consistently on all computers.

# jump variables
is_jump = False # jump logic is in notepad notes
jump_count = 10 # height at which the object jumps

bg_img = pygame.image.load("images/bg_img.jpeg") # since it is relative path (the image is present in our project directory)
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))

# character
left = False # moving left
right = False # moving right
walkCount = 0 # steps count

walkRight = [pygame.image.load(f'soldier/{i}.png') for i in range(1,10)]
walkLeft = [pygame.image.load(f'soldier/L{i}.png') for i in range(1,10)]
char = pygame.image.load('soldier/standing.png')

# game display loop
def DrawInGameLoop():
    global bg_img
    global walkCount
    screen.blit(bg_img, (0,0)) # blit is used to display images in pygame - if you run it will not get the full image - coz the dimensions of the window is not same as dimension of the image
    
    if walkCount+1 >= 27: # out of 9 images, when it reaches the last image, then it should start from the begining image - 3*9 = 27
        walkCount = 0
    if left: # if left key is clicked
        screen.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        screen.blit(walkRight[walkCount//3], (x,y)) # to make the movement smooth, we don't want the game to blited too fast - we'll make sure every image is shown 3 times before the next image is shown - so we multiply walk count by 3 results in 27 - floor div the walkRight(walkCount) by 3
        walkCount += 1
    else:
        screen.blit(char,(x,y))

    clock.tick(25) # this tells Pygame - "Run this loop at most 60 times per second." - This is called FPS (Frames Per Second).
    # Without clock.tick(60), your game loop runs as fast as your CPU allows (maybe 3000+ FPS).
    pygame.display.flip()

# game loop
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    
    keys = pygame.key.get_pressed() # returns bool, corresponds to all the keys of keyboard, initially it returns all false, once a key is pressed - its value becomes true, until it is pushed

    if keys[pygame.K_LEFT] and x>0:
        x-=vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x<w_width-width:
        x+=vel
        left = False
        right = True
    else:
        left = False
        right = False
        walkCount = 0
    if not(is_jump):
        # no need for the chracter to move up and down
        # if keys[pygame.K_UP] and y>0:
        #     y-=vel
        # if keys[pygame.K_DOWN] and y<w_height-height: # (window height - height of rect), is the max value the y cord of rect can take
        #     y+=vel
        if keys[pygame.K_SPACE]:
            is_jump = True
            right = False
            left = False
    else:
        if is_jump:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                y -= (jump_count ** 2)*neg*0.5
                jump_count -= 1
            else:
                jump_count=10
                is_jump=False

    DrawInGameLoop()

    
pygame.quit