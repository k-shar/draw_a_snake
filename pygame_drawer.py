import pygame

WIDTH = 480
HEIGHT = 360
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 191, 0)
GREY = (50, 50, 50)
DARK_GREEN = (52, 150, 60)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Game")
clock = pygame.time.Clock()

x, y = pygame.mouse.get_pos()
head_x, head_y = x, y
eye1_x, eye1_y = -100, -100
eye2_x, eye2_y = -100, -100
pupil1_x, pupil1_y = -100, -100
pupil2_x, pupil2_y = -100, -100
tongue_x, tongue_y = -100, -100
tip_tongue_x, tip_tongue_y = -100, -100

clicks = 0
done = False
while not done:
	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONUP:
			clicks += 1
			print(pygame.mouse.get_pos())
	# Code
	if clicks == 0:
		x, y = pygame.mouse.get_pos()
		head_x = x
		head_y = y

	if clicks == 1:
		x, y = pygame.mouse.get_pos()
		eye1_x = x
		eye1_y = y

	if clicks == 2:
		x, y = pygame.mouse.get_pos()
		eye2_x = x
		eye2_y = y
	
	if clicks == 3:
		x, y = pygame.mouse.get_pos()
		pupil1_x = x
		pupil1_y = y
	
	if clicks == 4:
		x, y = pygame.mouse.get_pos()
		pupil2_x = x
		pupil2_y = y	

	if clicks == 5:
		tongue_x = head_x
		tongue_y = head_y
		tip_tongue_x = x
		tip_tongue_y = y
		x, y = pygame.mouse.get_pos()


	screen.fill(WHITE)

	# Head
	pygame.draw.ellipse(screen, BLACK, [head_x-5, head_y-5, 160, 110])
	pygame.draw.ellipse(screen, BLACK, [head_x+25/2-5, head_y+55, 135, 60])
	pygame.draw.ellipse(screen, YELLOW, [head_x, head_y, 150, 100])
	pygame.draw.ellipse(screen, GREEN, [head_x+12.5, head_y+60, 125, 50])
	pygame.draw.ellipse(screen, GREY, [head_x+14.5, head_y+65, 120, 40])

	# Eye 1
	pygame.draw.ellipse(screen, BLACK, [eye1_x, eye1_y-5, 50, 70])
	pygame.draw.ellipse(screen, DARK_GREEN, [eye1_x, eye1_y, 50, 60])
	pygame.draw.ellipse(screen, WHITE, [eye1_x+5, eye1_y+10, 40, 40])
	# Eye 2
	pygame.draw.ellipse(screen, BLACK, [eye2_x, eye2_y-5, 50, 70])
	pygame.draw.ellipse(screen, DARK_GREEN, [eye2_x, eye2_y, 50, 60])
	pygame.draw.ellipse(screen, WHITE, [eye2_x+5, eye2_y+10, 40, 40])


	# Pupils
	pygame.draw.ellipse(screen, BLACK, [pupil1_x, pupil1_y, 10, 10])
	pygame.draw.ellipse(screen, BLACK, [pupil2_x, pupil2_y, 10, 10])

	# Tongue
	pygame.draw.polygon(screen, RED, [
									(tip_tongue_x, tip_tongue_y),
									(tongue_x+35, tongue_y + 85),
									(tongue_x+120, tongue_y + 82), 
									(tip_tongue_x+25, tip_tongue_y)
									])
	
	pygame.display.flip()
pygame.quit()