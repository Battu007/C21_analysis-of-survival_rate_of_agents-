import pygame
import os
import sys
import time
import random
pygame.font.init()  # To show counter, font needs to be initialized

WIDTH, HEIGHT = 800, 600  # Set window width/height and name of window
# #The main window to show the running simulation
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#WIN = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Agent Simulation")

# Load assets
RED_AGENT = pygame.image.load(
	os.path.join(
		"Pygame_Simulation\\assets",
		"pixel_ship_red_small.png"))
# Lasers
RED_LASER = pygame.image.load(
	os.path.join(
		"Pygame_Simulation\\assets",
		"pixel_laser_red.png"))
# Backgrond
BG = pygame.transform.scale(
	pygame.image.load(
		os.path.join(
			"Pygame_Simulation\\assets",
			"background-black.png")),
	(WIDTH,
	 HEIGHT))

CIRCLE_SIZE = 250
CIRCLE = pygame.image.load(
	os.path.join(
		"Pygame_Simulation\\assets",
		"circle_opacity_{}.png".format(CIRCLE_SIZE))).convert_alpha()
		
def collide(obj1, obj2):  # Collide function is used to check for pixel perfect collisions using masks
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y)))


class Circle:
	def __init__(self, x, y):
		self.circle_img = CIRCLE
		self.mask = pygame.mask.from_surface(self.circle_img.convert_alpha())
		self.x = x
		self.y = y
		
	def update_coordinates(self, x, y):
		self.x = x
		self.y = y

	def draw(self, window, x, y):
		self.update_coordinates(x, y)
		window.blit(self.circle_img, (self.x, self.y))

	def get_width(self):
		return self.circle_img.get_width()

	def get_height(self):
		return self.circle_img.get_height()


# This full class defines agents, each with its own attributes
class Agent:
	def __init__(self, x, y, id, health=3):
		self.x = x  # X-coordinate for each of the agent present in the list
		self.y = y  # Y-coordinate for each of the agent present in the list
		self.health = health
		self.ship_img = RED_AGENT
		# Mask is used to check for pixel perfect collisions
		self.mask = pygame.mask.from_surface(self.ship_img.convert_alpha())
		self.max_health = health

		self.circle = Circle(self.x, self.y)

	def draw(self, window):  # To show/draw the agent on the screen
		# Draw agent image at its own x/y coordinate
		window.blit(self.ship_img, (self.x, self.y))
		self.healthbar(window)  # Also draw the healthbar for each agent
		"""
		Have to find the right divisor so the circle is drawn at the center of the drones.
		Right now it's working okay with CIRCLE_SIZE = [150, 200, 250, 300]
		"""
		divisior = 2.8
		self.circle.draw(window, self.x - int(self.circle.get_width()/divisior), self.y - int(self.circle.get_height()/divisior))

	def move(self, vel):  # To move the agent on the screen every loop
		self.y -= vel  # Since y increases as you move down in pygame screen, so we reduce y to move up

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()

	def healthbar(self, window):  # Healthbar for each of the agent
		pygame.draw.rect(window, (255, 0, 0),(self.x, self.y +
											 self.get_height() +
										 10, self.get_width(), 10))
		pygame.draw.rect(window, (0, 255, 0), (self.x, self.y +
											   self.get_height() +
											   10, int(self.get_width() *
											   (self.health /
												   self.max_health)), 10))

	def get_surrounding_agents(self, agents):
		list_of_surrounding_agents = list()
		for agent in agents:
			if agent.x == self.x and agent.y == self.y:
				continue
			else:
				if collide(self.circle, agent):
					list_of_surrounding_agents.append(agent)
				#print(list_of_surrounding_agents)
		print('--------------------')
		return list_of_surrounding_agents

# This full class defines the bullets/lasers


class Bullet:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.bullet_img = RED_LASER
		self.mask = pygame.mask.from_surface(self.bullet_img.convert_alpha())

	def draw(self, window):
		window.blit(self.bullet_img, (self.x, self.y))

	def move(self, vel):
		self.y += vel


def main():
	run = True  # To make the main loop run
	FPS = 60  # Pygame FPS
	counter = 0  # Count the number of agents surviving
	# Usint the font to display surviving agents
	main_font = pygame.font.SysFont("comicsans", int(WIDTH / 25))
	agents = []  # List to store all the agents on screen
	agent_vel = 3  # Agent velocity when moving up
	bullets = []  # List to store all the bullets on the screen
	bullet_vel = 5  # Enemy bullet velocity moving downwards
	# An object to help track time, will be used to run pygame on specific FPS
	clock = pygame.time.Clock()

	def redraw_window():  # This function can only be called in "main" Function. Basically updates window every frame
		# blit draws the image on the background at the given coordinates
		WIN.blit(BG, (0, 0))

		# Drawing counter on the screen
		counter_label = main_font.render(
			f"Agents Survived: {counter}", 1, (255, 255, 255))
		WIN.blit(counter_label, (10, 10))

		for agent in agents:
			# Every screen update, draw the agents present in the agents[] list
			# on the screen
			agent.draw(WIN)
			list_of_surrounding_agents = agent.get_surrounding_agents(agents)
			print(list_of_surrounding_agents)

		for bullet in bullets:  # Every screen update, draw the bullets present in the bullets[] list on screen
			bullet.draw(WIN)

		pygame.display.update()  # Updates the entire surface/screen every loop

	no_of_waves = 1  # The number of waves that will try to cross the line

	while run:
		# Means that for every second at most "FPS" frames should pass. Here,
		# FPS = 60
		clock.tick(FPS)
		wave_length = 5  # Number of agents present in one wave
		xpos = 200  # X-Position of the initial agent. Hard coded for now

		# Logic states, If there is no agent on the screen and the required
		# number of waves have not gone already, send in the next wave
		if len(agents) == 0 and no_of_waves > 0:
			for i in range(
					wave_length):  # initialising to run the loop "length" number of times to create the required number of agents
				# Start first agent at X=200, and thereafter at 100+ from
				# previous X pos.
				agent = Agent(
					x=xpos, y=random.randrange(
						HEIGHT, HEIGHT + 10), id=i)
				# Add the new initialized agent to the agent list
				agents.append(agent)

				xpos += 100  # incresing Xpos value for next agent
			no_of_waves -= 1  # Decreasing value after each wave sent

		xpos = 200  # Since we're using a grid patern, bullets should start at the same point as agents
		if len(bullets) == 0 and len(
				agents) != 0:  # Logic states, if there is no bullet present on screen and if there are still some surviving agents, make new bullets
			for i in range(
					wave_length):  # Create same number of bullets as number of agents
				# Start them at the same Xpos, but subtract its own size so it
				# centres on the grid and in the straight line with the agent
				bullet = Bullet(xpos - 15, 0)
				# This line is used to send in a random wave of bullets every
				# time
				if(random.randrange(0, 100)) % 2 == 0:
					# The bullet is only appended to the bullet_list
					# "bullets[]" if the condition is met.
					bullets.append(bullet)
					# It is done so that we can have random number of bullets
					# at random places every wave of bullets
				xpos += 100  # Increase Xpos value for next bullet

		for event in pygame.event.get():  # Incase someone presses a button
			if event.type == pygame.QUIT:  # If the button pressed is "X" in the top right to close the window, then the simulation should stop
				pygame.quit()
				sys.exit()
				run = False  # Stop the main while loop on closing

		# Loop to update position of every agent every frame (To make them move
		# up)
		for agent in agents[:]:
			agent.move(agent_vel)  # Move agent up with the velocity defined
			# A statement to see if the Agent crosses the line(which is y = 0),
			# then
			if agent.y < 0:
				counter += 1  # increase the count of agents survived
				# And remove the agent from the list of agents as it is now
				# offscreen
				agents.remove(agent)

		# Similar loop description as for agents but for bullets
		for bullet in bullets[:]:
			bullet.move(bullet_vel)
			if bullet.y > HEIGHT:  # If bullet goes offscreen when moving downwards, then
				# Remove the bullet from the list of bullets
				bullets.remove(bullet)
				# And since we're in the loop of moving all bullets, we check
				# if they collide with an agent
			for agent in agents:  # Checking for all agents in one go
				if collide(
						agent,
						bullet):  # If two objects (agent object and bullet object) collide as defined in the function above
					# print("Hit")								#Print console log "Hit" for testing
					# Once the bullet hits, we remove it from the simulation
					bullets.remove(bullet)
					# And the agent that the bullet hit gets 1 minus health.
					agent.health -= 1
				if agent.health == 0:  # We check if the agent has 0 hp, that means the agent died.
					# If agent is dead, we remove it from the screen
					agents.remove(agent)

		redraw_window()  # Finally, redraw_window function is called to update every object on the screen for the next frame

main()  # Calling main function to start running the simulation.
