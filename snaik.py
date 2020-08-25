import random
import pygame

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y

class Square:
  SQUARE_BORDER_WIDTH = 2
  SQUARE_SIDE_LENGTH = 20

  SQUARE_TOTAL_SIDE_LENGTH = SQUARE_SIDE_LENGTH + SQUARE_BORDER_WIDTH * 2

  def __init__(self, color, position):
    self.__color = color
    self.position = position

  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.position == other.position

  def draw(self, surface):
    pygame.draw.rect(
      surface,
      self.__color,
      (
        self.position.x * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
        self.position.y * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
        self.SQUARE_SIDE_LENGTH,
        self.SQUARE_SIDE_LENGTH
      )
    )

class Snake:
  COLOR = '#000000'

  DIRECTIONS = {
    pygame.K_UP: {'name': 'up', 'movement': Point(0, -1), 'opposite': 'down'},
    pygame.K_RIGHT: {'name': 'right', 'movement': Point(1, 0), 'opposite': 'left'},
    pygame.K_DOWN: {'name': 'down', 'movement': Point(0, 1), 'opposite': 'up'},
    pygame.K_LEFT: {'name': 'left', 'movement': Point(-1, 0), 'opposite': 'right'}
  }

  def __init__(self, position, direction='right'):
    self.__squares = [Square(self.COLOR, position)]
    self.__direction = self.DIRECTIONS[pygame.K_RIGHT]
    self.is_alive = True

  def move(self, food):
    new_square = Square(self.COLOR, self.__squares[-1].position + self.__direction['movement'])

    if (new_square in self.__squares or
    new_square.position.x < 0 or new_square.position.x >= WIDTH or
    new_square.position.y < 0 or new_square.position.y >= HEIGHT):
      self.is_alive = False

    if new_square.position != food.square.position:
      self.__squares.pop(0)

    self.__squares.append(new_square)

    return new_square.position

  def turn(self, key):
    if (self.DIRECTIONS[key]['name'] != self.__direction['opposite']):
      self.__direction = self.DIRECTIONS[key]

  def draw(self, surface):
    for square in self.__squares:
      square.draw(surface)

class Food:
  COLOR = '#377b3e'

  def __init__(self):
    self.square = Square(self.COLOR, Point(random.randrange(0, WIDTH), y = random.randrange(0, HEIGHT)))

  def draw(self, surface):
    self.square.draw(surface)

BACKGROUND_COLOR = '#ffffff'

HEIGHT = 30
WIDTH = 40

SCREEN_HEIGHT = HEIGHT * Square.SQUARE_TOTAL_SIDE_LENGTH
SCREEN_WIDTH = WIDTH * Square.SQUARE_TOTAL_SIDE_LENGTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snaik")

def draw_window(screen, snake, food):
  screen.fill(BACKGROUND_COLOR)

  if snake.is_alive:
    snake.draw(screen)
    food.draw(screen)

  pygame.display.update()

def main(win):
  snake = Snake(Point(WIDTH / 2, HEIGHT / 2))
  food = Food()

  clock = pygame.time.Clock()

  run = True
  next_directions = []
  while run:
    pygame.time.delay(120)
    clock.tick(120)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break

      if (event.type == pygame.KEYDOWN and event.key in Snake.DIRECTIONS):
        next_directions.append(event.key)

    if (len(next_directions) > 0):
      snake.turn(next_directions.pop())

    if snake.move(food) == food.square.position:
      food = Food()

    # Update your sprites
    draw_window(screen, snake, food)

main(screen)
