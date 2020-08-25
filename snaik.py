import random
import pygame

BACKGROUND_COLOR = '#403D3E'
SNAKE_COLOR = '#D97979'
FOOD_COLOR = '#F2167D'

SQUARE_BORDER_WIDTH = 2
SQUARE_SIDE_LENGTH = 20

SQUARE_TOTAL_SIDE_LENGTH = SQUARE_SIDE_LENGTH + SQUARE_BORDER_WIDTH * 2

HEIGHT = 30
WIDTH = 40

SCREEN_HEIGHT = HEIGHT * SQUARE_TOTAL_SIDE_LENGTH
SCREEN_WIDTH = WIDTH * SQUARE_TOTAL_SIDE_LENGTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snaik")

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y

class Square:
  def __init__(self, position, color):
    self.position = position
    self.__color = color

  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.position == other.position

  def draw(self, surface):
    pygame.draw.rect(
      surface,
      self.__color,
      (
        self.position.x * SQUARE_TOTAL_SIDE_LENGTH + SQUARE_BORDER_WIDTH,
        self.position.y * SQUARE_TOTAL_SIDE_LENGTH + SQUARE_BORDER_WIDTH,
        SQUARE_SIDE_LENGTH,
        SQUARE_SIDE_LENGTH
      )
    )

class Snake:
  DIRECTION = ('up', 'right', 'down', 'left')
  MOVEMENT = {'up': Point(0, -1), 'right': Point(1, 0), 'down': Point(0, 1), 'left': Point(-1, 0)}

  def __init__(self, position, direction='right'):
    self.__squares = [Square(position, SNAKE_COLOR)]
    self.__direction = direction
    self.is_alive = True

  def move(self, food):
    new_square = Square(self.__squares[-1].position + self.MOVEMENT[self.__direction], SNAKE_COLOR)

    if (new_square in self.__squares or
    new_square.position.x < 0 or new_square.position.x > WIDTH or
    new_square.position.y < 0 or new_square.position.y > HEIGHT):
      self.is_alive = False

    if new_square.position == food.square.position:
      food.eat()
    else:
      self.__squares.pop(0)

    self.__squares.append(new_square)

  def turn(self, direction):
    if (self.DIRECTION.index(self.__direction) != (self.DIRECTION.index(direction) + 2) % 4):
      self.__direction = direction

  def draw(self, surface):
    for square in self.__squares:
      square.draw(surface)

class Food:
  def __init__(self, position):
    self.square = Square(position, FOOD_COLOR)
    self.is_eaten = False

  def eat(self):
    self.is_eaten = True

  def draw(self, surface):
    if not self.is_eaten:
      self.square.draw(surface)

def draw_window(screen, snake, food):
  screen.fill(BACKGROUND_COLOR)

  if snake.is_alive:
    snake.draw(screen)
    food.draw(screen)

  pygame.display.update()

def main(win):
  snake = Snake(Point(WIDTH / 2, HEIGHT / 2))
  food = Food(Point(random.randrange(0, WIDTH), y = random.randrange(0, HEIGHT)))

  clock = pygame.time.Clock()

  run = True
  while run:
    pygame.time.delay(120)
    clock.tick(120)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          snake.turn('up')
        elif event.key == pygame.K_RIGHT:
          snake.turn('right')
        elif event.key == pygame.K_DOWN:
          snake.turn('down')
        elif event.key == pygame.K_LEFT:
          snake.turn('left')

    snake.move(food)

    if food.is_eaten:
      food = Food(Point(random.randrange(0, WIDTH), y = random.randrange(0, HEIGHT)))

    # Update your sprites
    draw_window(screen, snake, food)

main(screen)
