import pygame

pygame.init() # initialize pygame
screen = pygame.display.set_mode((300,300),pygame.RESIZABLE) # set screen to display pygame - resizable makes the surface resizable
pygame.display.set_caption("Drawing shapes on surface") # set caption for the screen



# game loop
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

        # When the window is resized
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    screen.fill("white") # fill the screen with white
    
    pygame.draw.line(screen, "black", (0,0), (300,300), 5)
    pygame.draw.lines(screen,"orange", True, [(100,100),(200,100),(100,200)],4) # false for open, true for closed shape
    pygame.draw.rect(screen, "red", (50,50,100,100), 7)
    pygame.draw.circle(screen, "green", (200,150), 50, 1)
    pygame.draw.ellipse(screen, "yellow", (300, 100, 100, 50)) # 300,100 is centre - 100 is the width - 50 is the height
    pygame.draw.polygon(screen, "blue", ((250,75),(300,25),(350,75)),1)

    pygame.display.flip()

pygame.quit()

