import pygame
import random # for placing apples randomly

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
snake_x = round((window_width/2)/snake_block_size)*snake_block_size # initail cordinates of snake 
snake_y = round((window_height/2)/snake_block_size)*snake_block_size # after div by 20 and round and mult by 20 makes it allign with the game grid 
snake_x_change = 0 # defines by which the snake moves in x direction (left or right)
snake_y_change = 0 # defines by which the snake moves in y direction (up or down)

# Set up the food
food_block_size = 20
food_x = round(random.randrange(0,window_width-food_block_size)/food_block_size)*food_block_size
food_y = round(random.randrange(0,window_height-food_block_size)/food_block_size)*food_block_size

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

    # Move the snake
    snake_x += snake_x_change # update the x and y cordinate of snake's head
    snake_y += snake_y_change

    # Check for collision with the food
    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(0,window_width - food_block_size) / snake_block_size) * snake_block_size
        food_y = round(random.randrange(0,window_height - food_block_size) / snake_block_size) * snake_block_size
        snake_length += 1

    # update the snake_list
    snake_head = [] # it will store list values Eg. [[x1,y1],[x2,y2]]
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    # check for collision with teh walls
    if snake_x < 0 or snake_x >= window_width or snake_y < 0 or snake_y >= window_height:
        run = False

    # Set the game speed
    clock = pygame.time.Clock()
    clock.tick(snake_speed) # snake_speed is set to 15, i.e 15 FPS 
    pygame.time.delay(100) # delay for the user to input - otherwise before the user input has read the game will be ended

    # Draw the game objects
    window.fill("white") # white screen
    pygame.draw.rect(window, "green", [food_x, food_y, food_block_size, food_block_size])
    draw_snake(snake_block_size, snake_list) # draw snake
    pygame.display.flip() # update the window after drawing on the screen

    # GEt the user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_x_change = -snake_block_size
        snake_y_change = 0
    elif keys[pygame.K_RIGHT]:
        snake_x_change = snake_block_size
        snake_y_change = 0
    elif keys[pygame.K_UP]:
        snake_x_change = 0
        snake_y_change = -snake_block_size
    elif keys[pygame.K_DOWN]:
        snake_x_change = 0
        snake_y_change = snake_block_size

pygame.quit()