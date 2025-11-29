import pygame
import time
import random

pygame.init()

w_width = 500
w_height = 500
window = pygame.display.set_mode((w_width,w_height))
pygame.display.set_caption("Adding menu and buttons")

# game variable
clock = pygame.time.Clock()
font = pygame.font.SysFont("helvetica",50,1,1)
bg_speed = 5
font2 = pygame.font.SysFont("helvatica", 20,1)
score = 0
level = 1
next_level = 5

# importing image
car_img = pygame.image.load("CarRace/img/car1.png")
grass = pygame.image.load("CarRace/img/grass.jpg")
yellow_line = pygame.image.load("CarRace/img/yellow_line.jpg")
white_line = pygame.image.load("CarRace/img/white_line.jpg")
enemy_car_images = [pygame.image.load("CarRace/img/car2.png"), pygame.image.load("CarRace/img/car3.png")]
bg = pygame.image.load("CarRace/img/bg.jpeg")
bg = pygame.transform.scale(bg, (w_width,w_height))

# displaying text on the screen
def text_display(score, level):
    score_text = font2.render("score: " + str(score), 1, "black")
    window.blit(score_text, (0,0))
    level_text  = font2.render("level " + str(level), 1, "black")
    window.blit(level_text, (w_width-level_text.get_width(),0)) # get_width function will retrive the width of an element, similarly we have get_height

# Font settings
font3 = pygame.font.SysFont(None,30)

# Button class
class Button():
    def __init__(self,x,y,width,height,text,action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self):
        if self.is_hovered:
            pygame.draw.rect(window,"gray",self.rect)
        else:
            pygame.draw.rect(window, "white", self.rect) # button
        pygame.draw.rect(window, "black", self.rect, 3) # button border
        text_surface = font3.render(self.text, True, "black") # Renders the text to a new Surface called text_surface
        text_rect = text_surface.get_rect(center=self.rect.center) # Creates a Rect for the text_surface and positions it so its center matches the center of the button (self.rect.center).
        window.blit(text_surface, text_rect)

    def perform_action(self):
        self.action()

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

def start_game():
    # car class
    class Car():
        def __init__(self,x,y):
            self.x = x
            self.y = y
            self.width = 28
            self.height = 54
            self.vel = 4
        
        def draw(self,window):
            window.blit(car_img, (self.x,self.y))

    # enemy car class
    class EnemyCar(Car):
        def __init__(self, x, y, img):
            self.x = x
            self.y = y
            self.img = img
            self.width = 28
            self.height = 69
            self.vel = 2
            #self.vel = 3 + score*0.2 # speed increases based on score
        
        def move(self):
            self.y += self.vel

        def draw(self, window):
            window.blit(self.img, (self.x,self.y))

    # create a list of enemy cars
    enemy_cars = []

    def is_overlapping(new_car, car):
        return not (
            new_car.x + new_car.width < car.x or
            new_car.x > car.x + car.width or
            new_car.y + new_car.height < car.y or
            new_car.y > car.y + car.height
        )

    # create enemy cars and add them to the list
    for i in range(3):
        while True:
            x = random.randint(100, 400-28)
            y = random.randint(-500, -50)
            img = random.choice(enemy_car_images)
            new_car = EnemyCar(x, y, img)

            overlap = False
            for car in enemy_cars:
                if is_overlapping(new_car, car):
                    overlap = True
                    break

            if not overlap:
                enemy_cars.append(new_car)
                break
    # drawing background
    def drawing_background():
        # calculate the y position for each background element based on the scrolling speed
        bg_y = pygame.time.get_ticks() // bg_speed # get_ticks finds the time from the starting of the game - For every bg_speed milliseconds, bg_y increases by 1 pixel.

        # Logic: there are two screens when one goes down and forms a empty space the other which is present above will takes place on it so that it will be like a perfect rotational movement
        # Draw the background elements at their corresponding positions
        window.blit(grass, (0,bg_y%w_height-w_height))
        window.blit(grass, (420, bg_y%w_height-w_height))
        window.blit(white_line, (90, bg_y%w_height-w_height))
        window.blit(white_line, (405,bg_y%w_height-w_height))
        window.blit(yellow_line, (225,bg_y%w_height-w_height))
        window.blit(yellow_line, (225,(bg_y+100)%w_height-w_height))
        window.blit(yellow_line, (225,(bg_y+200)%w_height-w_height))
        window.blit(yellow_line, (225,(bg_y+300)%w_height-w_height))
        window.blit(yellow_line, (225,(bg_y+400)%w_height-w_height))

        # Draw the background elements at their corresponding positions for the bottom part
        window.blit(grass, (0,bg_y%w_height))
        window.blit(grass, (420, bg_y%w_height))
        window.blit(white_line, (90, bg_y%w_height))
        window.blit(white_line, (405,bg_y%w_height))
        window.blit(yellow_line, (225,bg_y%w_height))
        window.blit(yellow_line, (225,(bg_y+100)%w_height))
        window.blit(yellow_line, (225,(bg_y+200)%w_height))
        window.blit(yellow_line, (225,(bg_y+300)%w_height))
        window.blit(yellow_line, (225,(bg_y+400)%w_height))

    # drawing on the window surface
    def DrawInGameLoop():
        clock.tick(60) # 60 FPS
        window.fill((136,134,134)) # similar to gray - window.fill("gray")
        drawing_background()
        maincar.draw(window)

        # draw all enemy cars
        for enemy_car in enemy_cars:
            enemy_car.draw(window)
        
        text_display(score,level)

        pygame.display.flip()
        
    # creating objects
    maincar = Car(250,250)

    # crash condition
    def crash():
        global score, level, next_level, bg_speed
        text = font.render("CAR CRASHED", 1, "black")
        window.blit(text, (95,250))
        pygame.display.flip()
        time.sleep(2) # its better than pygame's delay function coz delay function will delay the game but the sleep function will completly makes the game sleep (everything stop executing)
        
        # re-initializing score, level etc
        score = 0
        level = 1
        next_level = 5
        bg_speed = 5

        # reset the position of the main car
        maincar.x = 250
        maincar.y = 250

        # reset the position and speed of all enemy cars
        for enemy_car in enemy_cars:
            enemy_car.x = random.randint(100, 400 - 28)
            enemy_car.y = random.randint(-500, -50)
            enemy_car.img = random.choice(enemy_car_images)
            enemy_car.vel = 2

        game_loop()

    # game loop
    run = True
    def game_loop():
        nonlocal run
        global next_level, score, level, bg_speed
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if not run:
                # GAME WINDOW CLOSED → CLOSE PYGAME SAFELY
                pygame.quit()
                quit()

            if maincar.x < 100 or maincar.x > 400-maincar.width:
                crash()

            # adding difficulty levels
            if score >= next_level:
                level += 1
                next_level += 5
                # incrase player car speed
                # maincar.vel += 0.5
                # increase enemy speed
                for enemy_car in enemy_cars:
                    enemy_car.vel += 1
                #increase background scroll speed
                if bg_speed > 1:
                    bg_speed -= 1
                else:
                    bg_speed = 1 # max difficulty level
                # Add extra enemy every 2nd level
                # if level % 2 == 0:
                #     x = random.randint(100, 400 - 20)
                #     y = random.randint(-500, -50)
                #     img = random.choice(enemy_car_images)
                #     enemy_cars.append(EnemyCar(x, y, img))

            # handling keyboard events
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and maincar.x > 0:
                maincar.x -= maincar.vel
            elif keys[pygame.K_RIGHT] and maincar.x < w_width-maincar.width:
                maincar.x += maincar.vel

            if keys[pygame.K_UP] and maincar.y > 0:
                maincar.y -= maincar.vel
            elif keys[pygame.K_DOWN] and maincar.y < w_height-maincar.height:
                maincar.y += maincar.vel

            # move all enemy cars
            for enemy_car in enemy_cars:
                enemy_car.move()

                # check for collision with main car
                if (enemy_car.x < maincar.x + maincar.width and
                    enemy_car.x + enemy_car.width > maincar.x and
                    enemy_car.y < maincar.y + maincar.height and
                    enemy_car.y + enemy_car.height > maincar.y):
                    crash()

                # if enemy car goes off the screen, reset its position
                if enemy_car.y > w_height:
                    enemy_car.x = random.randint(100, 400-28)
                    enemy_car.y = random.randint(-500, -50)
                    enemy_car.img = random.choice(enemy_car_images)
                    # enemy_car.vel = 2
                    score += 1
                    enemy_car.vel += 0.2 # the car's speed is incremented when it goes off

            DrawInGameLoop()
    game_loop()
    pygame.quit()

# Quit the game function
def quit_game():
    pygame.quit()

# Create buttons
start_button = Button(200,200,100,100,"Start",start_game)
quit_button = Button(200,320,100,100,"Quit",quit_game)

# Menu loop
menu_running = True
while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # x pressed to quit
            menu_running = False
            quit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN: # mouse button pressed
            mouse_pos = pygame.mouse.get_pos()
            if start_button.rect.collidepoint(mouse_pos):
                menu_running = False
                start_button.perform_action()
            elif quit_button.rect.collidepoint(mouse_pos):
                menu_running = False
                quit_button.perform_action()
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            start_button.check_hover(mouse_pos)
            quit_button.check_hover(mouse_pos)

    window.blit(bg, (0,0))

    start_button.draw()
    quit_button.draw()

    pygame.display.flip()