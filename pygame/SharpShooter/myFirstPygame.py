import pygame

pygame.init() # initialize pygame
screen = pygame.display.set_mode((300,300)) # set screen to display pygame
screen.fill("white") # fill the screen with white
pygame.display.set_caption("My first pygame program") # set caption for the screen

# game loop
done = True
while done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = False

    pygame.display.flip()