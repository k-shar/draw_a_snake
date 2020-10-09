import pygame
import random
import time

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
TEXT = (255, 0, 0)
TEXT_BG = (255, 255, 255)

# Initialise Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Game")
clock = pygame.time.Clock()

# Set text for instructions
font = pygame.font.Font('freesansbold.ttf', 32) 
instructions = font.render('', True, RED, BLUE) 
instructionsRect = instructions.get_rect()  
instructionsRect.center = (50, 50) 

# Set text for fly status
font = pygame.font.Font('freesansbold.ttf', 32) 
status = font.render('', True, GREEN, BLUE) 
statusRect = instructions.get_rect()  
statusRect.center = (50, 100)

# Set text for Total
total_flys_caught = 0
fly_held = False
total = font.render(f'Flys Eaten: {total_flys_caught}!', True, BLUE, TEXT_BG)
totalRect = instructions.get_rect()  
totalRect.center = (WIDTH - 300, HEIGHT - 50) 

x, y = pygame.mouse.get_pos()
head_x, head_y = x, y
eye1_x, eye1_y = -100, -100
eye2_x, eye2_y = -100, -100
pupil1_x, pupil1_y = -100, -100
pupil2_x, pupil2_y = -100, -100
tongue_x, tongue_y = -100, -100
tip_tongue_x, tip_tongue_y = -100, -100
line_x, line_y = -100, -100

fly_x = -100
fly_y = -100
fly_x_change = 7
fly_y_change = 5
catch_range = 20
mouth_catch_range = catch_range//2
random_fly_x = random.randint(20, WIDTH - 20)
random_fly_y = random.randint(20, HEIGHT - 20)
eating_fly = False
cooldown = 30

clicks = 0
done = False
while not done:
	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONUP:
			clicks += 1
	# Code
	if clicks == 0:
		instructions = font.render('Place Frog Head!', True, TEXT, TEXT_BG) 
		x, y = pygame.mouse.get_pos()
		head_x = x
		head_y = y

	if clicks == 1:
		instructions = font.render('Place Frog Eye 1!', True, TEXT, TEXT_BG) 
		x, y = pygame.mouse.get_pos()
		eye1_x = x
		eye1_y = y

	if clicks == 2:
		instructions = font.render('Place Frog Eye 2!', True, TEXT, TEXT_BG) 
		x, y = pygame.mouse.get_pos()
		eye2_x = x
		eye2_y = y
	
	if clicks == 3:
		instructions = font.render('Place Frog Pupil 1!', True, TEXT, TEXT_BG) 
		x, y = pygame.mouse.get_pos()
		pupil1_x = x
		pupil1_y = y
	
	if clicks == 4:
		instructions = font.render('Place Frog Pupil 2!', True, TEXT, TEXT_BG) 
		x, y = pygame.mouse.get_pos()
		pupil2_x = x
		pupil2_y = y	
		fly_x = random_fly_x
		fly_y = random_fly_y

	if clicks >= 5:
		instructions = font.render('Catch And Eat The Fly!', True, TEXT, TEXT_BG) 
		tongue_x = head_x
		tongue_y = head_y
		line_x = x
		line_y = y
		tip_tongue_x = x
		tip_tongue_y = y
		x, y = pygame.mouse.get_pos()

		if fly_x >= WIDTH or fly_x <= 0:
			fly_x_change *= -1

		if fly_y >= HEIGHT or fly_y <= 0:
			fly_y_change *= -1

		fly_x += fly_x_change
		fly_y += fly_y_change

	# Check if mouse is near Fly

	if  pygame.mouse.get_pos()[0] >= fly_x - catch_range and \
		pygame.mouse.get_pos()[0] <= fly_x + catch_range and \
		pygame.mouse.get_pos()[1] >= fly_y - catch_range and \
		pygame.mouse.get_pos()[1] <= fly_y + catch_range:
		fly_x = x
		fly_y = y
		fly_held = True
	else:
		fly_held = False

	# If fly is held and near mout
	if  pygame.mouse.get_pos()[0] >= tongue_x+35 - mouth_catch_range and \
		pygame.mouse.get_pos()[0] <= tongue_x+120 + mouth_catch_range and \
		pygame.mouse.get_pos()[1] >= tongue_y+85 - mouth_catch_range and \
		pygame.mouse.get_pos()[1] <= tongue_y+82 + mouth_catch_range and\
		fly_held:
		if not eating_fly:
			total_flys_caught += 1
		status = font.render('Fly Eaten!', True, GREEN, TEXT_BG)
		total = font.render(f'Flys Eaten: {total_flys_caught}!', True, BLUE, TEXT_BG)
		eating_fly = True


	if eating_fly:
		if cooldown <= 0:
			fly_x = random.randint(20, WIDTH - 20)
			fly_y = random.randint(20, HEIGHT - 20)
			eating_fly = False
			status = font.render('', True, GREEN, TEXT_BG)
			cooldown = 30
		else:
			cooldown -= 1
	screen.fill(WHITE)

	# Blit text
	screen.blit(instructions, instructionsRect)
	screen.blit(total, totalRect)
	screen.blit(status, statusRect)

	# Head
	pygame.draw.ellipse(screen, BLACK, [head_x-5, head_y-5, 160, 110])
	pygame.draw.ellipse(screen, BLACK, [head_x+25/2-5, head_y+55, 135, 60])
	pygame.draw.ellipse(screen, GREEN, [head_x, head_y, 150, 100])
	pygame.draw.ellipse(screen, GREEN, [head_x+12.5, head_y+60, 125, 50])
	if not eating_fly:
		pygame.draw.ellipse(screen, GREY, [head_x+14.5, head_y+65, 120, 40])
	else:
		pygame.draw.ellipse(screen, GREEN, [head_x+14.5, head_y+65, 120, 40])

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
	pygame.draw.line(screen, BLACK, (line_x+12.5, line_y), (tongue_x+77.5, tongue_y+83.5), width=1)

	# Fly
	pygame.draw.ellipse(screen, BLACK, [fly_x, fly_y, 20, 10])
	pygame.draw.line(screen, BLACK, (fly_x+2, fly_y+8), (fly_x, fly_y+12), width=3)
	pygame.draw.line(screen, BLACK, (fly_x+5, fly_y+8), (fly_x+5, fly_y+12), width=3)
	pygame.draw.line(screen, BLACK, (fly_x+18, fly_y+8), (fly_x+22, fly_y+12), width=4)
	pygame.draw.line(screen, BLACK, (fly_x+8, fly_y+8), (fly_x+12, fly_y+12), width=4)
	pygame.display.flip()
pygame.quit()
