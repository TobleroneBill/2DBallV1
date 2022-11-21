import math
import sys
import pygame  # importing pygame module for gaming & sys for system management
from pygame.locals import *  # not sure what this does but assume it adds all modules in pygame

# Idea - Brutal Peggle

pygame.init()  # initializes pygame
WINDOW = (1024, 576)
clock = pygame.time.Clock()
logo = pygame.image.load('C://Users//JOE//Desktop//Everything Can Die//Stuff//BrutalLogo.png')
pygame.display.set_icon(logo)
pygame.display.set_caption('Brutal Peggle')
screen = pygame.display.set_mode(WINDOW, 0, 32)  # Initalize window

# ball values
bLocX = int(WINDOW[0] / 2)  # Inital Spawn locations
bLocY = 20
Gravity = -2    # was -9, but was way too high at 60 fps
drag = 0.6      # changes how air resist effects the ball
power = 60  # How much the ball moves when clicked


def pythagoras(a,b):
    a2 = a * a
    b2 = b * b
    return math.sqrt(a2+b2)

# Ball class
class Ball:
    def __init__(self, x, y, size):  # Constructor
        self.x = x
        self.y = y
        self.velX = 0
        self.velY = 0
        self.size = size
        self.half_size = int(size / 2)
        self.rect = pygame.Rect(self.x, self.y, size, size)
        self.centerx = 0
        self.centery = 0
        self.deciding = True
        self.gravity = True

    def move(self):  # movement
        self.centerx = self.x + self.half_size
        self.centery = self.y + self.half_size
        self.draw()
        self.rect.x = self.x
        self.rect.y = self.y
        self.physics()
        self.x += self.velX
        self.y += self.velY

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        pygame.draw.line(screen, (255, 0, 0), (self.centerx, self.centery), (self.centerx + 20, self.centery), 2)
        pygame.draw.line(screen, (0, 255, 0), (self.centerx, self.centery), (self.centerx, self.centery + 20), 2)
        if self.deciding:
            pygame.draw.line(screen, (100, 100, 100), (self.centerx, self.centery), pygame.mouse.get_pos(), 2)

    def physics(self):
        lowerLimit = 1
        lowerLimitX = 0.3
        if self.gravity:        #if gravity is on
            if self.velX > lowerLimitX:     # adds drag to x
                self.velX -= drag
            elif self.velX < -lowerLimitX:
                self.velX += drag
        elif not self.gravity:          # if no gravity, velocity is 0 when too low
            if self.velX > lowerLimitX:  # adds drag to x
                self.velX -= drag
            elif self.velX < -lowerLimitX:
                self.velX += drag
            else:
                self.velX = 0
            pass

        if self.velY > lowerLimit:      # adds drag to y
            self.velY -= drag
        elif self.velY < -lowerLimit:
            self.velY += drag
        elif not self.gravity:      # if gravity is off, then velocity y gets set to 0 when it gets too low
            self.velY = 0
            pass

        if self.gravity:            # adds gravity value if enabled
            self.velY -= Gravity

        self.wallCollisions()


    # Had to learn some vector maths for this; calculates direction of mouse click and add force in that direction
    def setVelocity(self):
        x, y = pygame.mouse.get_pos()  # not important, needed for origin point
        centerLocations = (self.x + self.half_size),(self.y + self.half_size)
        distance = (x - centerLocations[0], y - centerLocations[1])  # get the distance of the player click
        # Pythagoras to calculate the magnitude between ball and the mouse click. to be normalized later
        # pythagoras
        magnitude = pythagoras(distance[0],distance[1])

        if not distance[0] == 0 or distance[1] == 0:
            normal = (distance[0] / magnitude,
                      distance[1] / magnitude)  # formula for normal is endVector / magnitude (length of vector)

            # Debug string. use at 12 fps to actually see whats going on lol
            print(f'distance: {distance}\n'
                 f'normalized: {normal}')
            pygame.draw.line(screen, (255, 0, 0), (centerLocations[0], centerLocations[1]),
                             (centerLocations[0] + normal[0] * 100, centerLocations[1] + normal[1] * 100), 3)  # draws line
            self.velX += normal[0] * power      # add force in direction multiplied by power (so I can tune values)
            self.velY += normal[1] * power

            finalVals = (self.velX + (normal[0] * power), self.velY + (normal[1] * power))
            print(f'finalVals: {finalVals}')



        else:       #cant divide by 0 so can be awkward
            print(f'{distance} makes 0 for some reason')

    def wallCollisions(self):
        if self.x <= 0:
            self.velX *= -1
            self.x = 1
        if self.x >= WINDOW[0] - self.size:
            self.velX *=-1
            self.x = WINDOW[0] - self.size

        if self.y < 0:
            self.velY *= -1
            self.y = 1
        if self.y >= WINDOW[1] - self.size:
            self.velY *= -1
            self.y = WINDOW[1] - self.size

        pass


'''
# Block class
class Block:
    def __init__(self, x, y, size, color, hp):
        self.x = x
        self.y = y
        self.color = color
        self.hp = hp
        self.rect = pygame.Rect(x, y, size, int(size / 2))

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
'''

# ball
ball = Ball(bLocX, 40, 20)
bColor = (123, 123, 23)
#block = Block(255, 255, 200, bColor, 1)

# debug text
font = pygame.font.SysFont(pygame.font.get_fonts()[12], 12)

while True:  # loop
    screen.fill((0, 0, 0))  # for screen updates
    ball.move()  # Look at class for explanation
    #block.draw()  # Test for collision
    debugText = f'xVel: {ball.velX}, yVel: {ball.velY} x: {ball.x} y: {ball.y}'
    text = font.render(debugText, False, (255, 255, 255))
    textrect = text.get_rect()
    screen.blit(text, textrect)

#    print(f'ball xVel: {ball.velX}, yVel: {ball.velY}')

    events = pygame.event.get()
    for event in events:  # Checks events from inputs
        if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:  # if press x, or escape key
            pygame.quit()  # quit pygame window
            sys.exit()  # force stop application
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[K_SPACE]:
                print('Deciding')
            if pygame.key.get_pressed()[K_k]:
                ball.gravity = not ball.gravity
                print('gravity off')
        if event.type == pygame.KEYUP:
            if not pygame.key.get_pressed()[K_SPACE]:
                print('finished deciding')
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball.setVelocity()

    pygame.display.update()  # updates screen
    clock.tick(60)  # sets to 60 ticks/fps

