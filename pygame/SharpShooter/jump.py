import pygame

pygame.init() # initialize pygame
w_width = 500 # window width
w_height = 500 # window height
screen = pygame.display.set_mode((w_width,w_height)) # set screen to display pygame
pygame.display.set_caption("Adding Jump logic") # set caption for the screen

# creating object
x=0 # x cordinate of rect
y=0 # y cordinate of rect
width = 50 # height and width of rect
height = 50
vel = 5 # velocity of rect to move
clock = pygame.time.Clock() # creates a Clock object. - is used to control the speed of your game loop, so the game runs smoothly and consistently on all computers.

# jump variables
is_jump = False
jump_count = 10 # height at which the object jumps

# game loop
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    
    keys = pygame.key.get_pressed() # returns bool, corresponds to all the keys of keyboard, initially it returns all false, once a key is pressed - its value becomes true, until it is pushed

    if not(is_jump):
        if keys[pygame.K_UP] and y>0:
            y-=vel
        if keys[pygame.K_DOWN] and y<w_height-height: # (window height - height of rect), is the max value the y cord of rect can take
            y+=vel
        if keys[pygame.K_SPACE]:
            is_jump = True
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
    if keys[pygame.K_LEFT] and x>0:
        x-=vel
    if keys[pygame.K_RIGHT] and x<w_width-width:
        x+=vel

    screen.fill("white") # fill the screen with white
    pygame.draw.rect(screen, "black", (x,y,width,height))
    clock.tick(60) # this tells Pygame - "Run this loop at most 60 times per second." - This is called FPS (Frames Per Second).
    # Without clock.tick(60), your game loop runs as fast as your CPU allows (maybe 3000+ FPS).
    pygame.display.flip()
pygame.quit