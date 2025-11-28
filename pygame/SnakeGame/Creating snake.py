import pygame

pygame.init()

# Set up the game window
window_width = 500
window_height = 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Set up the snake
snake_block_size = 20 # each block has a width and height of 20 px
snake_speed = 15 # speed that the snake moves
snake_list = [] # body of snake
snake_length = 1 # initally the snake body occupies only 1 block
snake_x = window_width/2 # initail cordinates of snake
snake_y = window_height/2
snake_x_change = 0 # defines by which the snake moves in x direction (left or right)
snake_y_change = 0 # defines by which the snake moves in y direction (up or down)

# Define the function to draw the snake
def draw_snake(snake_block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(window, "black", [block[0], block[1], snake_block_size, snake_block_size]) # block has 2 values x,y which represents the cordinates of the block (body)

# game loop
run = True
while run:
    for event in pygame.event.get(): # getting input(key or screen) from user
        if event.type == pygame.QUIT: # is user touch x to exit
            run = False

    # update the snake_list
    snake_head = [] # it will store list values Eg. [[x1,y1],[x2,y2]]
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_list.append(snake_head)

    # Set the game speed
    clock = pygame.time.Clock()
    clock.tick(snake_speed) # snake_speed is set to 15, i.e 15 FPS 

    # Draw the game objects
    window.fill("white") # white screen
    draw_snake(snake_block_size, snake_list) # draw snake
    pygame.display.flip() # update the window after drawing on the screen

pygame.quit()