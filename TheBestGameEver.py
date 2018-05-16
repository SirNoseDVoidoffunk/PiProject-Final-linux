'''
Python Snake Game on a Rasbery pi 3

Team Rocket:
Kyle, Sem, Hansel, Pat
'''

import sys, random, pygame, dumbmenu as dm
from pygame import *	#needed to reference keys directly instead of pygame.K_xxxx

#directional constants
DIRECTION_UP = 1
DIRECTION_DOWN = 0
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 2

#look up table for keys and directions, we can add joystic movement as well
KEY_DIRECTION = {
	K_w: DIRECTION_UP,		K_UP:    DIRECTION_UP,   
	K_s: DIRECTION_DOWN,	K_DOWN:  DIRECTION_DOWN, 
	K_a: DIRECTION_LEFT,	K_LEFT:  DIRECTION_LEFT, 
	K_d: DIRECTION_RIGHT,	K_RIGHT: DIRECTION_RIGHT,
}

#color constants in RGB
SNAKE_HEAD_COLOR = (250, 120, 120)
SNAKE_BODY_COLOR = (100, 250, 100)
APPLE_COLOR = (250, 50, 50)
BACKGROUND_COLOR = (0, 0, 0)
WHITE = (255,255,255)

#grid size constant
GRID = (66, 60) # X, Y

#snake based constants
SNAKE_START_LENGTH = 5          # Initial snake length in segments
SNAKE_START_LOC = (int(GRID[0]/2), int(GRID[1]/2))    # Initial snake location

# Gams speed
STARTING_FPS = 4
FPS_INCREMENT_FREQUENCY = 100

#snake class
#init with a starting point as a tupple and length in number of grid squares
class Snake:
    def __init__ (self, start, length):
        self.startLength = length
        self.start = start
        self.reset()

    #reset snake to original state
    def reset(self):
        self.snakeBits = []
        self.direction = DIRECTION_UP

        for n in range(0, self.startLength):
            self.snakeBits.append((self.start[0], self.start[1] + n))

    #change directions if not in opposite direciton
    def change_direction(self, direction):
        if not (self.direction == 0 and direction == 1 or
            self.direction == 1 and direction == 0 or
            self.direction == 2 and direction == 3 or
            self.direction == 3 and direction == 2):
        	self.direction = direction

    # Returns the head of the snake
    def getHead(self):
        return self.snakeBits[0]

    # Returns the tail of the snake
    def getTail(self):
        return self.snakeBits[len(self.snakeBits) - 1]

    #return the entire snake
    def getSnake(self):
    	return self.snakeBits

    #return only tail
    def getSnakeTail(self):
    	return self.snakeBits[1:]

    #move the snake by 1 block in a direction
    def move_snake(self):
        head = self.getHead();
        newHead = ()

        if self.direction == 0: newHead = (head[0], head[1] + 1)
        if self.direction == 1: newHead = (head[0], head[1] - 1)
        if self.direction == 2: newHead = (head[0] + 1, head[1])
        if self.direction == 3: newHead = (head[0] - 1, head[1])

        self.snakeBits.pop()
        self.snakeBits.insert(0, newHead)

    #add bits to the end of the snake
    def add_bit(self):
        tail = self.getTail();
        bit = ()

        if self.direction == 0: bit = (tail[0], tail[1] + 1)
        if self.direction == 1: bit = (tail[0], tail[1] - 1)
        if self.direction == 2: bit = (tail[0] + 1, tail[1])
        if self.direction == 3: bit = (tail[0] - 1, tail[1])

        self.snakeBits.append(bit)

    #check if the head is located in the same cell as another bit of the snake
    def check_collision(self):
        if len([bit for bit in self.snakeBits if bit == self.getHead()]) > 1:
            return True
        else:
            return False

#snake food
class Food:
	def __init__(self):
		self.location = (0,0)
		self.foods = []

	#reset to starting position
	def reset(self):
		self.location = (0,0)
		self.foods = []

	#method to spawn food at random location
	def spawn(self, snake):
		if len(self.foods) < 1:
			self.location = self.__randomLocation()
			#check if it spawns on snake, else relocate
			while self.location in snake.getSnake() or self.location in self.foods:
				self.location = self.__randomLocation()
			self.foods.append(self.location)

	#check if any of the foods is eaten if so remove from foods
	def is_eaten(self, snake):
		eaten = True
		if snake.getHead() in self.foods:
			self.foods.pop(self.foods.index(snake.getHead()))
		else:
			eaten = False
		return eaten

	#returns all foods alive
	def get_foods(self):
		return self.foods

	#private method for food spawns
	def __randomLocation(self):
		randX = random.randint(3,GRID[0]-3)
		randY = random.randint(3,GRID[1]-3)
		return (randX, randY)

class Game:
	def __init__(self, window, screen, clock, font):
		self.window = window
		self.screen = screen
		self.clock = clock
		self.font = font
		self.windowSize = self.window.get_size()

		self.fps = STARTING_FPS
		self.ticks = 0
		self.playing = False
		self.menu = True
		self.score = 0
		self.world = Rect((0,0), GRID)

		self.nextDirection = DIRECTION_UP
		#create a snake
		self.snake = Snake(SNAKE_START_LOC, SNAKE_START_LENGTH)
		#create food
		self.food = Food()
		#spawn the food
		self.food.spawn(self.snake)

	#game loop
	def play(self, events):
		self.playing = True
		self.menu = False

		if self.playing:
			self.input(events)
			self.update()
			self.draw()
		else: 
			self.playing = False
			self.menu = True

		self.clock.tick(self.fps)

		#increase game speed
		self.ticks += 1
		if self.ticks % FPS_INCREMENT_FREQUENCY == 0: self.fps += 1

		return self.playing
	
	#draw the game objects
	def draw(self):
		self.screen.fill(BACKGROUND_COLOR)

		blockSize = (int(self.windowSize[0]/GRID[0]),int(self.windowSize[1]/GRID[1]))

		pygame.draw.rect(self.screen, SNAKE_HEAD_COLOR, (blockSize[0] * (self.snake.getHead()[0]-1), blockSize[1] * (self.snake.getHead()[1]-1), blockSize[0], blockSize[1]))
		for snake in self.snake.getSnakeTail():
			pygame.draw.rect(self.screen, SNAKE_BODY_COLOR, (blockSize[0] * (snake[0]-1), blockSize[1] * (snake[1]-1), blockSize[0], blockSize[1]))
		for food in self.food.get_foods():
			pygame.draw.rect(self.screen, APPLE_COLOR, (blockSize[0] * (food[0]-1), blockSize[1] * (food[1]-1), blockSize[0], blockSize[1]))

		self.screen.blit(self.font.render("Score: " + '{:08d}'.format(self.score), 1, (255, 255, 255)), (int(self.windowSize[0]/2.5), 20))
		pygame.display.flip()

	#display main menu
	def main_menu(self):
		self.playing = False
		self.menu = True
		self.mainmenufont = pygame.font.Font('arcadeclassic.ttf', 56)

		while not self.playing and self.menu:
			self.screen.fill(BACKGROUND_COLOR)
			pygame.display.update()
			logo = pygame.image.load("rocket.png").convert_alpha()
			snake = pygame.image.load("snake.png").convert_alpha()
			logo = pygame.transform.rotate(logo, 15)

			self.screen.blit(logo,(170, 70))
			self.screen.blit(snake,((int(self.windowSize[0]/2)+52, int(self.windowSize[1]/2-200))))
			self.screen.blit(self.mainmenufont.render("Snake", 1, (255, 255, 255)), (int(self.windowSize[0]/7)+52, int(self.windowSize[1]/7)))
			self.screen.blit(self.mainmenufont.render("Classic", 1, (255, 255, 255)), (int(self.windowSize[0]/7), int(self.windowSize[1]/7)+70))
			pygame.display.flip()

			choise = dm.dumbmenu(self.screen, 
				['Start Game',
				'How To Play',
				'Quit Game'],
				int(self.windowSize[0]/7)-70,int(self.windowSize[1]/2)-70,'freesansbold',32,.7,WHITE,WHITE, True)
			if choise == 0:
				while self.play(pygame.event.get()):
					pass
				self.game_over()
			if choise == 1:
				#do in draw
				self.screen.blit(self.font.render("Use the arrow keys to control your snake. Eat as many apples as you can to grow as long as possible. But don't hit the wall, or eat your tail!", 1, (255, 255, 255)), (500, 500))
				pygame.display.flip()
			if choise == 2:
				self.menu = False
				pygame.quit()
				sys.exit()

	#game end state
	def game_over(self):
		while True:
			self.screen.fill((150, 0, 0))
			self.screen.blit(self.font.render("Game over!", 1, (255, 255, 255)), (int(self.windowSize[0]/3)+190, int(self.windowSize[1]/2) - 40))
			self.screen.blit(self.font.render("Your score is: " + str(self.score), 1, (255, 255, 255)), (int(self.windowSize[0]/3)+130, int(self.windowSize[1]/2)))
			self.screen.blit(self.font.render("Press Escape to return to main menu", 1, (255, 255, 255)), (int(self.windowSize[0]/3)-60, int(self.windowSize[1]/2) + 40))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
					self.reset()
	
	#reset the game
	def reset(self):
		self.snake.reset()
		self.food.reset()
		self.food.spawn(self.snake)
		self.nextDirection = DIRECTION_UP
		self.fps = STARTING_FPS
		self.score = 0
		self.main_menu()

	#listen for input events to change movement
	def input(self, events):
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			#movement
			elif event.type == pygame.KEYDOWN and event.key in KEY_DIRECTION:
				self.nextDirection = KEY_DIRECTION[event.key]
			#back to main menu, i can't be bothered to figure out pauses
			elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
				self.reset()

	#update the game after each second
	def update(self):
		self.snake.change_direction(self.nextDirection)
		self.snake.move_snake()

		if self.food.is_eaten(self.snake):
			self.snake.add_bit()
			self.food.spawn(self.snake)
			for n in range(0, int(self.score/200)):
				self.food.spawn(self.snake)
			self.score += 50
			#score code
		if self.snake.check_collision() or self.snake.getHead()[0] < 1 or self.snake.getHead()[1] < 1 or self.snake.getHead()[0] > GRID[0] or self.snake.getHead()[1] > GRID[1]:
			#game over screen
			self.playing = False


#main function to call the game
def main():
	pygame.init()

	pygame.display.set_caption('PyGame Snake')

	window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	screen = pygame.display.get_surface()
	clock = pygame.time.Clock()
	font = pygame.font.Font('arcadeclassic.ttf', 20)
	game = Game(window, screen, clock, font)
	game.main_menu()

if __name__ == '__main__':
	main()