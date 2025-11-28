import pygame
import random # for placing apples randomly

pygame.init()

# Set up the game window
window_width = 500
window_height = 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Set up the fonts
font_style = pygame.font.SysFont("helvetica", 30, 0, 1)
font_style2 = pygame.font.SysFont("helvetica", 50, 1, 1)

# Function to display the score
def display_score(score):
    score_text = font_style.render("Score: " + str(score), 1, "black") # 1 stands for antialias to be true - smooth text - else if set to 0 - then sharp pixelated text
    window.blit(score_text, [0,0])

# Display game over
def display_game_over():
    game_over_text = font_style2.render("GAME OVER", 1, "black")
    window.blit(game_over_text, (150,225))
    pygame.display.flip()

# Set up the snake
snake_block_size = 20 # each block has a width and height of 20 px
snake_speed = 25 # speed that the snake moves
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
        # Generate a new position for the food
        food_on_snake = True
        while food_on_snake:
            food_x = round(random.randrange(0,window_width - food_block_size) / snake_block_size) * snake_block_size
            food_y = round(random.randrange(0,window_height - food_block_size) / snake_block_size) * snake_block_size
            food_on_snake = False
            for block in snake_list:
                if block[0] == food_x and block[1] == food_y:
                    food_on_snake = True
                    break
        snake_length += 1 

    # update the snake_list
    snake_head = [] # it will store list values Eg. [[x1,y1],[x2,y2]]
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    # check for collision with the walls
    if snake_x < 0 or snake_x >= window_width or snake_y < 0 or snake_y >= window_height:
        display_game_over()
        pygame.time.delay(1000) # delay to show the Game over message for 1 sec and close the game
        run = False
    # if snake_x < 0:
    #     snake_x = window_width
    # elif snake_x >= window_width:
    #     snake_x = 0
    # elif snake_y < 0:
    #     snake_y = window_height
    # elif snake_y >= window_height:
    #     snake_y = 0

    # Set the game speed
    clock = pygame.time.Clock()
    clock.tick(snake_speed) # snake_speed is set to 15, i.e 15 FPS 
    pygame.time.delay(100) # delay for the user to input - otherwise before the user input has read the game will be ended

    # Check for collison with the snake's body
    for block in snake_list[:-1]: # for every part in the snake's list excluding the head
        if block == snake_head: # if any block == the head of the snake
            display_game_over()
            pygame.time.delay(1000)
            run = False

    # Draw the game objects
    window.fill("white") # white screen
    pygame.draw.rect(window, "green", [food_x, food_y, food_block_size, food_block_size])
    draw_snake(snake_block_size, snake_list) # draw snake
    display_score(snake_length-1)
    pygame.display.flip() # update the window after drawing on the screen

    # GEt the user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake_x_change != snake_block_size: # the second check is for not letting the snake to turn 180 degree
        snake_x_change = -snake_block_size
        snake_y_change = 0
    elif keys[pygame.K_RIGHT] and snake_x_change != -snake_block_size:
        snake_x_change = snake_block_size
        snake_y_change = 0
    elif keys[pygame.K_UP] and snake_y_change != snake_block_size:
        snake_x_change = 0
        snake_y_change = -snake_block_size
    elif keys[pygame.K_DOWN] and snake_y_change != -snake_block_size:
        snake_x_change = 0
        snake_y_change = snake_block_size

pygame.quit()