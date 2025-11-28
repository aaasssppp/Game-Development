import pygame

pygame.init() # initialize pygame
w_width = 500 # window width
w_height = 500 # window height
screen = pygame.display.set_mode((w_width,w_height)) # set screen to display pygame
pygame.display.set_caption("Handling keyboard events") # set caption for the screen

# creating object
x=0 # x cordinate of rect
y=0 # y cordinate of rect
width = 50 # height and width of rect
height = 50
vel = 1 # velocity of rect to move
clock = pygame.time.Clock() # used to regulate the frame rate

# game loop
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    
    keys = pygame.key.get_pressed() # returns bool, corresponds to all the keys of keyboard, initially it returns all false, once a key is pressed - its value becomes true, until it is pushed
    if keys[pygame.K_UP]:
        y-=vel
    if keys[pygame.K_DOWN]:
        y+=vel
    if keys[pygame.K_LEFT]:
        x-=vel
    if keys[pygame.K_RIGHT]:
        x+=vel

    screen.fill("white") # fill the screen with white
    pygame.draw.rect(screen, "black", (x,y,width,height))
    clock.tick(60)
    pygame.display.flip()
pygame.quit