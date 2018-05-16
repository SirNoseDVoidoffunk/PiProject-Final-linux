#this is where most or all of the code for the game will be contained
#We'll start by commenting the game and then fill in the rest with code later.
#open a game window
#show main menu screen
        #option to play
        #option for how to play
        #option high scores
        #game options
            #sound
            #game speed
            #start-length

        #create game objects
            #movable area
            #score
            #snake
            #apples - of different types
        #set stage for game
            #place snake
            #place the apple
    #main game loop begins
        #move snake
        #check for user input and adjust direction accordingly
        #when you eat an apple
            #increment score
            #add length to snake body
            #place new apple
        #check for collision with wall or self
            #if a collision occurs
                #end main game loop
    #show game over screen
    #ask user for name to save high score
    #display top scores
    #ask user to play again

print("Hello World!")
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
SNAKE_HEAD_COLOR = (250, 50, 50)
SNAKE_BODY_COLOR = (250, 250, 250)
APPLE_COLOR = (50, 250, 50)
BACKGROUND_COLOR = (0, 0, 0)
WHITE = (255,255,255)

#grid size constant
GRID = (50, 50) # X, Y

#snake based constants
SNAKE_START_LENGTH = 5          # Initial snake length in segments
SNAKE_START_LOC = (25, 25)    # Initial snake location

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

class Food:
	def __init__(self):
		self.location = (0,0)
		self.foods = []

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
		randX = random.randint(0,GRID[0])
		randY = random.randint(0,GRID[1])
		return (randX, randY)

# class Score:
# 	def __init__(self)
# 		self.score = []
# 	def get_scores(self)
# 		return self.score
# 	def add_score(self, score)
#		self.score.append(score)

class Game:
	def __init__(self, window, screen, clock, font):
		self.window = window
		self.screen = screen
		self.clock = clock
		self.font = font

		self.fps = STARTING_FPS
		self.ticks = 0
		self.playing = False
		self.menu = True
		self.score = 0
		self.world = Rect((0,0), GRID)

		self.nextDirection = DIRECTION_UP
		self.snake = Snake(SNAKE_START_LOC, SNAKE_START_LENGTH)
		self.food = Food()
		self.food.spawn(self.snake)

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

		self.ticks += 1
		if self.ticks % FPS_INCREMENT_FREQUENCY == 0: self.fps += 1

		return self.playing
		
	def draw(self):
		self.screen.fill(BACKGROUND_COLOR)

		windowSize = self.window.get_size()
		blockSize = (int(windowSize[0]/GRID[0]),int(windowSize[1]/GRID[1]))

		pygame.draw.rect(self.screen, SNAKE_HEAD_COLOR, (blockSize[0] * (self.snake.getHead()[0]-1), blockSize[1] * (self.snake.getHead()[1]-1), blockSize[0], blockSize[1]))
		for snake in self.snake.getSnakeTail():
			pygame.draw.rect(self.screen, SNAKE_BODY_COLOR, (blockSize[0] * (snake[0]-1), blockSize[1] * (snake[1]-1), blockSize[0], blockSize[1]))
		for food in self.food.get_foods():
			pygame.draw.rect(self.screen, APPLE_COLOR, (blockSize[0] * (food[0]-1), blockSize[1] * (food[1]-1), blockSize[0], blockSize[1]))

		self.screen.blit(self.font.render("Score: " + '{:09d}'.format(self.score), 1, (255, 255, 255)), (150, 20))
		pygame.display.flip()

	def main_menu(self):
		self.playing = False
		self.menu = True
		self.mainmenufont = pygame.font.Font('arcadeclassic.ttf', 56)

		while not self.playing and self.menu:
			self.screen.fill(BACKGROUND_COLOR)
			pygame.display.update()
			# pygame.key.set_repeat(500,30)
                        
			self.screen.blit(self.mainmenufont.render("Snake", 1, (255, 255, 255)), (500, 500))
			self.screen.blit(self.mainmenufont.render("Classic", 1, (255, 255, 255)), (500, 700))
			pygame.display.flip()

			choise = dm.dumbmenu(self.screen, 
				['Start Game',
				'How To Play',
				'Quit Game'],
				64,64,'freesansbold',32,.7,WHITE,WHITE, True)
			if choise == 0:
				while self.play(pygame.event.get()):
					pass
				self.game_over()
			if choise == 1:
				#do in draw
				print ("Use the arrow keys to control your snake. Eat as many apples as you can to grow as long as possible. But don't hit the wall, or eat your tail!")
			if choise == 2:
				self.menu = False
				pygame.quit()
				sys.exit()

	def game_over(self):
		while True:
			self.screen.fill((255, 0, 0))
			self.screen.blit(self.font.render("Game over!", 1, (255, 255, 255)), (150, 150))
			self.screen.blit(self.font.render("Your score is: " + str(self.score), 1, (255, 255, 255)), (140, 180))
			self.screen.blit(self.font.render("Press Escape to return to main menu", 1, (255, 255, 255)), (20, 200))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
					self.reset()
		
	def reset(self):
		self.snake.reset()
		self.food.reset()
		self.food.spawn(self.snake)
		self.nextDirection = DIRECTION_UP
		self.fps = STARTING_FPS
		self.score = 0
		self.main_menu()

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

	def update(self):
		self.snake.change_direction(self.nextDirection)
		self.snake.move_snake()

		if self.food.is_eaten(self.snake):
			self.snake.add_bit()
			self.food.spawn(self.snake)
			self.score += 50
			#score code
		if self.snake.check_collision() or self.snake.getHead()[0] < 1 or self.snake.getHead()[1] < 1 or self.snake.getHead()[0] > GRID[0] or self.snake.getHead()[1] > GRID[1]:
			#game over screen
			self.playing = False



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

# def main():
# 	pygame.init()

# 	size = width, height = 500, 500
# 	window = pygame.display.set_mode(size)
# 	pygame.display.set_caption('Best Snake Game')

# 	done = False
# 	color = (225, 255, 255)
# 	x = 30
# 	y = 30

# 	clock = pygame.time.Clock()

# 	while not done:
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				done = True

# 		pressed = pygame.key.get_pressed()
# 		if pressed[pygame.K_UP]: y -= 3
# 		if pressed[pygame.K_DOWN]: y += 3
# 		if pressed[pygame.K_LEFT]: x -= 3
# 		if pressed[pygame.K_RIGHT]: x += 3

# 		window.fill((0, 0, 0))
# 		pygame.draw.rect(window, color, pygame.Rect(x, y, 60, 60))

# 		pygame.display.flip()
# 		clock.tick(60)
