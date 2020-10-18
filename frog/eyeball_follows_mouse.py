import pygame
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 480
HEIGHT = 360
FPS = 60

# Variables for drawing
# The pupil
k_radius = 295
scale = 3

# Initialise Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epic Py Game")
clock = pygame.time.Clock()


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


def pupil_point(center_point, point_2, bounding_rect, k_radius, scale):
    ''' 
    returns the coordinates of a point that:
        - lies on the circle with center "center_point"
          circle has radius proportional to "k_radius"
        - lies on the line between center_point and point_2
        - lies in the rect "boudning_rect"
        - lies within an error margin of scale

    '''
    m, c = line((center_point[0], center_point[1]), point_2)

    short_x = 10000
    short_y = 10000
    short_dis = 100000
    # searches all points withing bounding rect
    for x in range(bounding_rect[0], bounding_rect[0] + bounding_rect[2]):
        for y in range(bounding_rect[1], bounding_rect[1] + bounding_rect[3]):

            # if point lies on the equation of the circle x**2 + y**2 = r**2
            if (x-center_point[0])**2 + (y-center_point[1])**2 >= k_radius - scale and \
               (x-center_point[0])**2 + (y-center_point[1])**2 <= k_radius + scale:

                # and if it lies on the line y = mx + c
                if 1 >= (m * x + c) / y and \
                        -1 <= (m * x + c) / y:

                    # and it is the closest point to point_2
                    if dispoints(x, y, point_2[0], point_2[1]) < short_dis:
                        short_x = x
                        short_y = y
                        short_dis = dispoints(x, y, point_2[0], point_2[1])
    return short_x, short_y


done = False
while not done:

    clock.tick(FPS)
    screen.fill(WHITE)
    loc = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if pygame.mouse.get_pressed()[0]:
            print(f"Left Mouse Click at {loc}")

    # DRAW STUFF

    # Fly
    fly_pos = [350, 250]
    fly_pos = loc
    pygame.draw.circle(screen, BLACK, fly_pos, 4)

    # Eyeball
    eye_rect = [WIDTH//3, HEIGHT//3, 50, 70]
    pygame.draw.ellipse(screen, GREEN, eye_rect)

    # Eye Center
    eye_center = [int(eye_rect[0]) + int(eye_rect[2])//2,
                  int(eye_rect[1]) + int(eye_rect[3])//2]

    # Draw pupil
    pupil_x, pupil_y = pupil_point(
        eye_center, fly_pos, eye_rect, k_radius, scale)
    pygame.draw.circle(screen, BLACK, (pupil_x, pupil_y), 4)

    pygame.display.update()
pygame.quit()
