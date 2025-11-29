import pygame
import time
import random

pygame.init()

w_width = 500
w_height = 500
window = pygame.display.set_mode((w_width,w_height))
pygame.display.set_caption("Car race background")

# game variable
clock = pygame.time.Clock()
font = pygame.font.SysFont("helvetica",50,1,1)

# importing image
car_img = pygame.image.load("CarRace/img/car1.png")
grass = pygame.image.load("CarRace/img/grass.jpg")
yellow_line = pygame.image.load("CarRace/img/yellow_line.jpg")
white_line = pygame.image.load("CarRace/img/white_line.jpg")
enemy_car_images = [pygame.image.load("CarRace/img/car2.png"), pygame.image.load("CarRace/img/car3.png")]

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
    
    def move(self):
        self.y += self.vel

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

# create a list of enemy cars
enemy_cars = []

# create enemy cars and add them to the list
for i in range(3):
    x = random.randint(100, 400-20) # between 2 white lines
    y = random.randint(-500,-50) # the cars should not spawn like zombies (if we give values b/w 0 and window_width) - so the car should be spawned some where above the window starts and then it should reach window
    img = random.choice(enemy_car_images)
    enemy_car = EnemyCar(x,y,img)
    enemy_cars.append(enemy_car)

# drawing background
def drawing_background():
    window.blit(grass, (0,0))
    window.blit(grass, (420,0)) # the width of image is 80 - to position is correctly we are placing it at 420 (500-80)
    window.blit(white_line, (90,0))
    window.blit(white_line, (405,0))
    window.blit(yellow_line, (225,0))
    window.blit(yellow_line, (225,100))
    window.blit(yellow_line, (225,200))
    window.blit(yellow_line, (225,300))
    window.blit(yellow_line, (225,400))

# drawing on the window surface
def DrawInGameLoop():
    clock.tick(60) # 60 FPS
    window.fill((136,134,134)) # similar to gray - window.fill("gray")
    drawing_background()
    maincar.draw(window)

    # draw all enemy cars
    for enemy_car in enemy_cars:
        enemy_car.draw(window)

    pygame.display.flip()
    
# creating objects
maincar = Car(250,250)

# crash condition
def crash():
    text = font.render("CAR CRASHED", 1, "black")
    window.blit(text, (95,250))
    pygame.display.flip()
    time.sleep(2) # its better than pygame's delay function coz delay function will delay the game but the sleep function will completly makes the game sleep (everything stop executing)
    
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
    global run
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if maincar.x < 100 or maincar.x > 400-maincar.width:
            crash()

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
                enemy_car.vel = 2

        DrawInGameLoop()
game_loop()
pygame.quit()