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

  def __eq__(self, value):
    return self.__class__ == value.__class__ and self.x == value.x and self.y == value.y

class Snake:
  def __init__(self, position, direction='right'):
    self.squares = [position]
    self.direction = direction
    self.alive = True

  def move(self, food):
    new_square = Point(self.head().x, self.head().y)

    if self.direction == 'up' and new_square.y > 0:
      new_square.y -= 1
    elif self.direction == 'right' and new_square.x < WIDTH - 1:
      new_square.x += 1
    elif self.direction == 'down' and new_square.y < HEIGHT - 1:
      new_square.y += 1
    elif self.direction == 'left' and new_square.x > 0:
      new_square.x -= 1
    else:
      self.alive = False

    if new_square in self.squares:
      self.alive = False

    if new_square == food.position:
      food.eat()
    else:
      self.squares.pop(0)

    self.squares.append(new_square)

  def turn(self, direction):
    if ((direction == 'up' and self.direction != 'down') or
    (direction == 'right' and self.direction != 'left') or
    (direction == 'down' and self.direction != 'up') or
    (direction == 'left' and self.direction != 'right')):
      self.direction = direction

  def head(self):
    return self.squares[-1]

  def draw(self, screen):
    for square in self.squares:
      draw_square(screen, SNAKE_COLOR, square)

class Food:
  def __init__(self, position):
    self.position = position
    self.eaten = False

  def position(self):
    return (self.position)

  def eat(self):
    self.eaten = True

  def draw(self, screen):
    if not self.eaten:
      draw_square(screen, FOOD_COLOR, self.position)

def draw_square(surface, color, position):
  pygame.draw.rect(
    screen,
    color,
    (
      position.x * SQUARE_TOTAL_SIDE_LENGTH + SQUARE_BORDER_WIDTH,
      position.y * SQUARE_TOTAL_SIDE_LENGTH + SQUARE_BORDER_WIDTH,
      SQUARE_SIDE_LENGTH,
      SQUARE_SIDE_LENGTH
    )
  )

def draw_window(screen, snake, food):
  screen.fill(BACKGROUND_COLOR)

  if snake.alive:
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

    if food.eaten:
      food = Food(Point(random.randrange(0, WIDTH), y = random.randrange(0, HEIGHT)))

    # Update your sprites
    draw_window(screen, snake, food)

main(screen)
