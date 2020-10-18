import pygame
import math
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (52, 150, 60)
BLUE = (0, 0, 255)

# To add a fly, add the flys color
# to this list
fly_colors = [RED, BLUE, BLACK]

WIDTH = 480
HEIGHT = 360
FPS = 60

# Variables for drawing
# The pupil
k_radius = 50
scale = 40

# Initialise Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epic Py Game")
clock = pygame.time.Clock()


class Fly:

    def __init__(self, color):
        self.color = color
        self.fly_x = random.randint(20, WIDTH - 20)
        self.fly_y = random.randint(20, HEIGHT - 20)
        self.fly_change = [5, 5]

        self.fly_change[0] *= random.choice([-1, 1])
        self.fly_change[1] *= random.choice([-1, 1])

    def drawFly(self):

        pygame.draw.ellipse(screen, self.color, [self.fly_x, self.fly_y, 20, 10])
        pygame.draw.line(screen, self.color, (self.fly_x+2, self.fly_y+8), (self.fly_x, self.fly_y+12), 3)
        pygame.draw.line(screen, self.color, (self.fly_x+5, self.fly_y+8), (self.fly_x+5, self.fly_y+12), 3)
        pygame.draw.line(screen, self.color, (self.fly_x+18, self.fly_y+8), (self.fly_x+22, self.fly_y+12), 4)
        pygame.draw.line(screen, self.color, (self.fly_x+8, self.fly_y+8), (self.fly_x+12, self.fly_y+12), 4)

        # Make fly bounce off walls
        if self.fly_x >= WIDTH or self.fly_x <= 0:
            self.fly_change[0] *= -1

        if self.fly_y >= HEIGHT or self.fly_y <= 0:
            self.fly_change[1] *= -1

        # Move Fly
        self.fly_x += self.fly_change[0]
        self.fly_y += self.fly_change[1]


class Eye:
    eye_color = GREEN

    def __init__(self, size):
        self.size = size

    def pupil_point(self, point_2):
        ''' 
        returns the coordinates of a point that:
            - lies on the circle with center "center_point"
              circle has radius proportional to "k_radius"
            - lies on the line between center_point and point_2
            - lies in the rect "boudning_rect"
            - lies within an error margin of scale
        '''
        m, c = LinAlgebra.line((self.center[0], self.center[1]), point_2)

        short_x = 10000
        short_y = 10000
        short_dis = 100000
        # searches all points withing bounding rect
        for x in range(self.rect[0], self.rect[0] + self.rect[2]):
            for y in range(self.rect[1], self.rect[1] + self.rect[3]):

                # if point lies on the equation of the circle x**2 + y**2 = r**2
                if (x-self.center[0])**2 + (y-self.center[1])**2 >= k_radius - scale and \
                   (x-self.center[0])**2 + (y-self.center[1])**2 <= k_radius + scale:

                    # and if it lies on the line y = mx + c
                    if 1 >= (m * x + c) / y and \
                            -1 <= (m * x + c) / y:

                        # and it is the closest point to point_2
                        if LinAlgebra.dispoints(x, y, point_2[0], point_2[1]) < short_dis:
                            short_x = x
                            short_y = y
                            short_dis = LinAlgebra.dispoints(x, y, point_2[0], point_2[1])
        return short_x, short_y

    def whereToLook(self):
        ''' Calculates which fly is closest '''

        closest_x = 10000
        closest_y = 10000
        short_dis = 100000

        for fly in fly_list:

            if LinAlgebra.dispoints(fly.fly_x, fly.fly_y, self.center[0], self.center[1]) <= short_dis:
                closest_x = fly.fly_x
                closest_y = fly.fly_y
                short_dis = LinAlgebra.dispoints(fly.fly_x, fly.fly_y, self.center[0], self.center[1])
                closest_fly_coords = [fly.fly_x, fly.fly_y]

        return closest_fly_coords

    def drawEye(self, pos):

        self.center = [int(pos[0]) + int(self.size[0])//2,
                       int(pos[1]) + int(self.size[1])//2]
        # Draw Eyeball
        self.rect = [pos[0], pos[1], self.size[0], self.size[1]]

        pygame.draw.ellipse(screen, BLACK, [pos[0]+0, pos[1]-5, 50, 70])
        pygame.draw.ellipse(screen, DARK_GREEN, [pos[0]+0, pos[1]+00, 50, 60])
        pygame.draw.ellipse(screen, WHITE, [pos[0]+5, pos[1]+10, 40, 40])

        look = self.whereToLook()
        # Draw pupil
        pupil_x, pupil_y = self.pupil_point(look)
        pygame.draw.circle(screen, BLACK, (pupil_x, pupil_y), 4)


class Face:
    def drawFace(self, pos):
        pygame.draw.ellipse(screen, BLACK, [pos[0]-5, pos[1]-5, 160, 110])
        pygame.draw.ellipse(screen, BLACK, [pos[0]+25//2-5, pos[1]+55, 135, 60])
        pygame.draw.ellipse(screen, GREEN, [pos[0], pos[1], 150, 100])
        pygame.draw.ellipse(screen, GREEN, [pos[0]+12, pos[1]+60, 125, 50])

        pygame.draw.ellipse(screen, GREY, [pos[0]+14, pos[1]+65, 120, 40])


class Tongue:
    pass


class LinAlgebra():
    def line(point_1, point_2):
        ''' Find the equation of a line between two points '''
        X, Y = point_1[0], -1 * point_1[1]
        x, y = point_2[0], -1 * point_2[1]
        if (X - x) != 0:
            m = (Y - y) / (X - x)
            c = Y - (m * X)
            return m, c
        return 0, 0

    def midpoint(X, Y, x, y):
        ''' find the midpoint of a line given 2 points'''
        x = (X + x) // 2
        y = (Y + y) // 2
        return x, y

    def dispoints(X, Y, x, y):
        ''' find the distance between 2 points using pythagoras'''
        return math.sqrt((X-x)**2 + (Y-y)**2)


# Fly
fly_list = []
for i in range(len(fly_colors)):
    fly_list.append(Fly(fly_colors[i]))


# initialise face parts
# draw them offscreen
face = Face()
face_loc = (-1000, -1000)

eye_1 = Eye([50, 70])
eye_1_loc = (-1000, -1000)

eye_2 = Eye([50, 70])
eye_2_loc = (-1000, -1000)

tongue = Tongue()


clicks = 0
done = False
while not done:

    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicks += 1
            print(f"CLICK at {loc}")

    loc = pygame.mouse.get_pos()

    # DRAW STUFF

    # Add face part on each new click
    if clicks == 0:
        face_loc = loc
    if clicks == 1:
        eye_1_loc = loc
    if clicks == 2:
        eye_2_loc = loc

    # draw face parts
    # (will be drawn offscreeen until click)
    face.drawFace(face_loc)
    eye_1.drawEye(eye_1_loc)
    eye_2.drawEye(eye_2_loc)

    for fly in fly_list:
        fly.drawFly()

    pygame.display.update()
pygame.quit()
