import random
import pygame

class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y

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
    pygame.draw.rect(surface, self.__color, (
      self.position.x * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
      self.position.y * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
      self.SQUARE_SIDE_LENGTH,
      self.SQUARE_SIDE_LENGTH
    ))

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

  def move(self, key):
    if (key in self.DIRECTIONS and self.DIRECTIONS[key]['name'] != self.__direction['opposite']):
      self.__direction = self.DIRECTIONS[key]

    new_square = Square(self.COLOR, self.__squares[-1].position + self.__direction['movement'])

    if (new_square in self.__squares or
    new_square.position.x < 0 or new_square.position.x >= WIDTH or
    new_square.position.y < 0 or new_square.position.y >= HEIGHT):
      self.is_alive = False

    self.__squares.append(new_square)

    return new_square.position

  def shrink(self):
    self.__squares.pop(0)

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

pygame.font.init()
FONT = pygame.font.Font(pygame.font.get_default_font(), 60)

class Game:
  def __init__(self):
    self.__clock = pygame.time.Clock()
    self.__reset()

  def run(self):
    while True:
      pygame.time.delay(120)
      self.__clock.tick(120)

      self.__handle_events()
      self.__tick()
      self.__draw()

  def __handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      if self.snake.is_alive and event.type == pygame.KEYDOWN and event.key in Snake.DIRECTIONS:
        self.__next_direction = event.key
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        self.__reset()

  def __tick(self):
    if self.snake.is_alive:
      if self.snake.move(self.__next_direction) == self.food.square.position:
        self.food = Food()
      else:
        self.snake.shrink()

  def __reset(self):
    self.__next_direction = None
    self.snake = Snake(Point(WIDTH / 2, HEIGHT / 2))
    self.food = Food()

  def __draw(self):
    screen.fill(BACKGROUND_COLOR)

    if self.snake.is_alive:
      self.snake.draw(screen)
      self.food.draw(screen)
    else:
      text_label = FONT.render("Press Space to restart", 1, '#000000')
      screen.blit(text_label, (SCREEN_WIDTH / 2 - text_label.get_width() / 2, 500))

    pygame.display.update()

Game().run()
