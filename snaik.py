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

class Snake:
  def __init__(self, x, y, direction):
    self.squares = [(x, y)]
    self.direction = direction
    self.alive = True

  def move(self, food):
    x, y = self.head()

    if self.direction == 'up' and y > 0:
      y -= 1
    elif self.direction == 'right' and x < WIDTH - 1:
      x += 1
    elif self.direction == 'down' and y < HEIGHT - 1:
      y += 1
    elif self.direction == 'left' and x > 0:
      x -= 1
    else:
      self.alive = False

    if (x, y) in self.squares:
      self.alive = False

    if self.head() == food.position():
      food.eat()
    else:
      self.squares.pop(0)

    self.squares.append((x, y))

  def turn(self, direction):
    if ((direction == 'up' and self.direction != 'down') or
    (direction == 'right' and self.direction != 'left') or
    (direction == 'down' and self.direction != 'up') or
    (direction == 'left' and self.direction != 'right')):
      self.direction = direction

  def head(self):
    return self.squares[-1]

  def draw(self, screen):
    for (x, y) in self.squares:
      pygame.draw.rect(
        screen,
        SNAKE_COLOR, (
          x * SQUARE_TOTAL_SIDE_LENGTH + SQUARE_BORDER_WIDTH,
          y * SQUARE_TOTAL_SIDE_LENGTH + SQUARE_BORDER_WIDTH,
          SQUARE_SIDE_LENGTH,
          SQUARE_SIDE_LENGTH
        )
      )

class Food:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.eaten = False

  def position(self):
    return (self.x, self.y)

  def eat(self):
    self.eaten = True

  def draw(self, screen):
    if not self.eaten:
      pygame.draw.rect(
        screen,
        FOOD_COLOR, (
          self.x * SQUARE_TOTAL_SIDE_LENGTH + SQUARE_BORDER_WIDTH,
          self.y * SQUARE_TOTAL_SIDE_LENGTH + SQUARE_BORDER_WIDTH,
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
  snake = Snake(WIDTH / 2, HEIGHT / 2, 'right')
  food = Food(random.randrange(0, WIDTH), random.randrange(0, HEIGHT))

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
      food = Food(random.randrange(0, WIDTH), random.randrange(0, HEIGHT))

    # Update your sprites
    draw_window(screen, snake, food)

main(screen)
