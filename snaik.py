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
    new_square.position.x < 0 or new_square.position.x >= Game.WIDTH or
    new_square.position.y < 0 or new_square.position.y >= Game.HEIGHT):
      self.is_alive = False

    self.__squares.append(new_square)

    return new_square.position

  def shrink(self):
    self.__squares.pop(0)

  def draw(self, surface):
    for square in self.__squares:
      square.draw(surface)

class Game:
  BACKGROUND_COLOR = '#ffffff'
  FOOD_COLOR = '#377b3e'

  HEIGHT = 30
  WIDTH = 40
  SCREEN_HEIGHT = HEIGHT * Square.SQUARE_TOTAL_SIDE_LENGTH
  SCREEN_WIDTH = WIDTH * Square.SQUARE_TOTAL_SIDE_LENGTH

  def __init__(self):
    self.__screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    pygame.display.set_caption("Snaik")

    pygame.font.init()
    self.__font = pygame.font.Font(pygame.font.get_default_font(), 60)

    self.__clock = pygame.time.Clock()
    self.__reset()

  def run(self):
    while True:
      pygame.time.delay(120)
      self.__clock.tick(120)

      self.__handle_events()
      self.__tick()
      self.__draw()

  def __reset(self):
    self.__direction_key = None
    self.__snake = Snake(Point(self.WIDTH / 2, self.HEIGHT / 2))
    self.__generate_food()

  def __generate_food(self):
    self.__food = Square(self.FOOD_COLOR, Point(random.randrange(0, self.WIDTH), random.randrange(0, self.HEIGHT)))

  def __handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      elif event.type == pygame.KEYDOWN:
        if self.__snake.is_alive and event.key in Snake.DIRECTIONS:
          self.__direction_key = event.key
        elif not self.__snake.is_alive and event.key == pygame.K_SPACE:
          self.__reset()

  def __tick(self):
    if self.__snake.is_alive:
      if self.__snake.move(self.__direction_key) == self.__food.position:
        self.__generate_food()
      else:
        self.__snake.shrink()

  def __draw(self):
    self.__screen.fill(self.BACKGROUND_COLOR)

    if self.__snake.is_alive:
      self.__snake.draw(self.__screen)
      self.__food.draw(self.__screen)
    else:
      text_label = self.__font.render("Press Space to restart", 1, '#000000')
      self.__screen.blit(text_label, (self.SCREEN_WIDTH / 2 - text_label.get_width() / 2, 500))

    pygame.display.update()

Game().run()
