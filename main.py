from random import choice
import pygame
from pygame.locals import *
from pyautogui import alert
import os
from time import sleep

os.chdir('pygames/ReachTheEnd')
clock = pygame.time.Clock()
x = 125
y = 450
width = 50
height = 50


death_messages = ["You're Trash", "Imagine being so bad", "You were so close. \n Oh wait. You weren't", "hahahHAHAHAHAHHA \nJust stop playing"]
death_message = choice(death_messages)

alertbutton_strings = ["Bruh", "ok", "Whyyy", "Why must you hurt me in this way", "Pain", "I'm depressed now"]
alert_string = choice(alertbutton_strings)

pygame.init()
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reach The End")


class Player():
    def __init__(self, x, y, width, height):
        self.space = 0
        self.vel = 5
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hasImage = 1
        self.image = pygame.image.load("hah.png")

    def move(self, level):
        Right = 0
        Left = 0
        Up = 0
        Down = 0
        key_pressed = pygame.key.get_pressed()
        if (key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]) and self.x > 0:
            self.x -= self.vel
            Right = 1
        if (key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]) and self.x < SCREEN_WIDTH-(self.width):
            self.x += self.vel
            Left = 1
        if (key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]) and self.y > 0:
            self.y -= self.vel
            Up = 1
        if (key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]) and self.y < SCREEN_HEIGHT-(self.height):
            self.y += self.vel
            Down = 1
        if level >= 3 and key_pressed[pygame.K_SPACE] and self.space == 0:
            self.space = 1
            if Up == 1:
                self.y -= 125
                Up = 0
            if Down == 1:
                self.y += 125
                Down = 0
            if Left == 1:
                self.x += 125
                Left = 0
            if Right == 1:
                self.x -= 125
                Right = 0
            
        if self.space == 1 and not(key_pressed[pygame.K_SPACE]):
            self.space = 0

    def draw(self):
        if self.x <0:
            self.x = 0
        if self.y <0:
            self.y = 0
        if self.x > SCREEN_WIDTH-(self.width):
            self.x = SCREEN_WIDTH-(self.width)
        if self.y > SCREEN_HEIGHT-(self.height):
            self.y = SCREEN_HEIGHT-(self.height)
        if self.hasImage:
            image = pygame.transform.rotate(self.image, 0)
            image = image.get_rect(center=self.image.get_rect(
                topleft=(self.x, self.y)).center)
            image = pygame.transform.rotate(self.image, 0)
            image = pygame.transform.scale(
                self.image, (self.width, self.height))
            self.rect = pygame.Rect(
                self.x+5, self.y+5, self.width-10, self.height-10)
            WIN.blit(image, (self.x, self.y))
        else:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(WIN, (255, 255, 255), self.rect)

    def levelpos(self, level):
        if level == 1:
            self.x = 125
            self.y = 450
        if level == 2:
            self.x = 75
            self.y = 450
        if level == 3:
            self.x = SCREEN_WIDTH/2
            self.y = 375
        if level == 4:
            self.x = SCREEN_WIDTH-100
            self.y = 450
        if level == 5:
            self.x = 125
            self.y = 450
        if level == 6:
            self.x = 125
            self.y = 450
        if level == 7:
            self.x = 250
            self.y = 450
        # if level == 8:
        #     self.x = 125
        #     self.y = 450
        # if level == 9:
        #     self.x = 125
        #     self.y = 450
        # if level == 10:
        #     self.x = 125
        #     self.y = 450

player = Player(x, y, width, height)

class Enemy():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load("enemy.png")

    def charge(self, playerx, playery):
        tx, ty = playerx - self.x, playery - self.y
        stepx, stepy = (tx / 50, ty / 50)
        self.x += stepx
        self.y += stepy
    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        WIN.blit(self.image, self.rect)

    def collide(self, player: pygame.Rect):
        if pygame.Rect.colliderect(player, (self.x+15, self.y-15, self.width-15, self.height+15)):
            return True

    
class Reset():
    def __init__(self):
        self.run = False

    def ran(self):
        self.run = True

    def reset(self):
        self.run = False

resetobj = Reset()
enemy = Enemy(0, 0, 50, 50)
enemy2 = Enemy(450, 0, 50, 50)
class Levels():
    def __init__(self):
        self.written = 0
        self.CurrentLevel = 1
        self.levelObjects = list()
        self.reachedGoal = False
        self.levelSelected = True

    def level1(self):
        self.CurrentLevel = 1
        self.levelObjects = []
        self.reachedGoal = False
        obj1 = pygame.Rect(0, 0, 100, SCREEN_HEIGHT)
        self.levelObjects.append(obj1)
        obj2 = pygame.Rect(0, 0, SCREEN_WIDTH, 100)
        self.levelObjects.append(obj2)
        obj3 = pygame.Rect(200, 200, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.levelObjects.append(obj3)
        pygame.draw.rect(WIN, (255, 0, 0), obj1)
        pygame.draw.rect(WIN, (255, 0, 0), obj2)
        pygame.draw.rect(WIN, (255, 0, 0), obj3)
        self.goal = pygame.Rect(SCREEN_WIDTH-100, 100, 100, 100)
        pygame.draw.rect(WIN, (0, 255, 0), self.goal)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("WASD or Arrow", True, (255, 255,255))  
        WIN.blit(text, (250, 250))
        text = font.render(" keys to move", True, (255, 255, 255))
        WIN.blit(text, (250, 300))

    def level2(self):
        self.CurrentLevel = 2
        self.levelObjects = []
        self.reachedGoal = False
        self.goal = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        pygame.draw.rect(WIN, (0, 255, 0), self.goal)
        obj1 = pygame.Rect(0, 0, 50, SCREEN_HEIGHT)
        self.levelObjects.append(obj1)
        obj2 = pygame.Rect(0, 200, SCREEN_WIDTH-60, 50)
        self.levelObjects.append(obj2)
        obj3 = pygame.Rect(150, 325, 425, 500)
        self.levelObjects.append(obj3)
        obj4 = pygame.Rect(150, 0, SCREEN_WIDTH, 100)
        self.levelObjects.append(obj4)
        pygame.draw.rect(WIN, (255, 0, 0), obj1)
        pygame.draw.rect(WIN, (255, 0, 0), obj2)
        pygame.draw.rect(WIN, (255, 0, 0), obj3)
        pygame.draw.rect(WIN, (255, 0, 0), obj4)

    def level3(self):

        self.levelObjects = []
        self.reachedGoal = False
        self.currentLevel = 3
        self.goal = pygame.Rect(0, 0, SCREEN_WIDTH, 100)
        pygame.draw.rect(WIN, (0, 255, 0), self.goal)

        obj = pygame.Rect(0, 450, SCREEN_WIDTH, 100)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)
        obj = pygame.Rect(0, 0, 50, SCREEN_HEIGHT)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)
        obj = pygame.Rect(SCREEN_WIDTH-50, 0, 50, SCREEN_HEIGHT)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)
        obj = pygame.Rect(0, SCREEN_HEIGHT//2-10, SCREEN_WIDTH, 50)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Press space to dash", True, (255, 255,255))  
        WIN.blit(text, (150, 250))

    def level4(self):
        self.levelObjects = []
        self.reachedGoal = False
        self.currentLevel = 4
        self.goal = pygame.Rect(0, 0, SCREEN_WIDTH, 100)
        pygame.draw.rect(WIN, (0, 255, 0), self.goal)

        obj = pygame.Rect(0, 0, 50, SCREEN_HEIGHT)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)
        obj = pygame.Rect(SCREEN_WIDTH-50, 0, 50, SCREEN_HEIGHT)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)
        obj = pygame.Rect(SCREEN_WIDTH//2-25, 0, 50, SCREEN_HEIGHT)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)
        obj = pygame.Rect(0, 0, SCREEN_WIDTH//2, 150)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)
        obj = pygame.Rect(250, 250, SCREEN_WIDTH//2, 150)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)

    def level5(self):
        self.levelObjects = []
        self.reachedGoal = False
        self.currentLevel = 5
        self.goal = pygame.Rect(0, 0, SCREEN_WIDTH, 100)
        pygame.draw.rect(WIN, (0, 255, 0), self.goal)
        enemy.charge(player.x, player.y)
        enemy2.charge(player.x, player.y)


    def level6(self):
        if self.written == 0:
            enemy.y = 0
            enemy2.y = 0
            enemy.x = 50
            enemy2.x = SCREEN_WIDTH-50
            self.written = 1

        self.levelObjects = []
        self.reachedGoal = False
        self.currentLevel = 4
        self.goal = pygame.Rect(0, 0, SCREEN_WIDTH, 100)
        pygame.draw.rect(WIN, (0, 255, 0), self.goal)
        obj = pygame.Rect(255, 0, 50, SCREEN_HEIGHT)
        self.levelObjects.append(obj)
        pygame.draw.rect(WIN, (255, 0, 0), obj)
        
        enemy.charge(player.x, player.y)
        enemy2.charge(player.x, player.y)

    def level7(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Congratulations", True, (255, 255,255))  
        WIN.blit(text, (100, 250))
        text = font.render("You have completed the game", True, (255, 255, 255))
        WIN.blit(text, (10, 300))



    
    def collide(self, player: pygame.Rect):
        if self.CurrentLevel > 0:
            for i in self.levelObjects:
                if pygame.Rect.colliderect(player, i):
                    return True
            if pygame.Rect.colliderect(player, (self.goal.x+15, self.goal.y-15, self.goal.width-15, self.goal.height+15)):
                self.written = 0
                self.CurrentLevel += 1
                self.reachedGoal = True

def main():
    run = True
    levels = Levels()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and levels.CurrentLevel == 7:
                alert('Sayonara', 'Game Over', '', timeout=500)
                pygame.quit()
                run = False

        WIN.fill(0)
        
        player.move(levels.CurrentLevel)
        player.draw()
        enemy.draw()
        enemy2.draw()
        eval(f'levels.level{levels.CurrentLevel}()')
        if levels.collide(player.rect) == True or enemy.collide(player.rect) == True:
            sleep(0.1)
            alert(death_message, title="Yu hav deth", button=alert_string)
            run = False
        elif levels.reachedGoal == True:
            alert("You have reached the goal!", timeout=2000)
            player.levelpos(levels.CurrentLevel)
        pygame.display.update()

main()
input()
