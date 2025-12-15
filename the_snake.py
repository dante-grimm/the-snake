"""Модуль игры Змейка."""
import pygame
import random


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

SPEED = 20

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """Инициализирует игровой объект."""
        self.position = (0, 0)
        self.body_color = None

    def draw(self, surface):
        """Отрисовывает объект на поверхности."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        max_x = (SCREEN_WIDTH // CELL_SIZE) - 1
        max_y = (SCREEN_HEIGHT // CELL_SIZE) - 1
        x = random.randint(0, max_x) * CELL_SIZE
        y = random.randint(0, max_y) * CELL_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на поверхности."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = []
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        self.direction = self.next_direction

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction

        new_x = head_x + (dir_x * CELL_SIZE)
        new_y = head_y + (dir_y * CELL_SIZE)

        new_x = new_x % SCREEN_WIDTH
        new_y = new_y % SCREEN_HEIGHT

        new_head = (new_x, new_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на поверхности."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0],
                position[1],
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        start_x = (SCREEN_WIDTH // 2) // CELL_SIZE * CELL_SIZE
        start_y = (SCREEN_HEIGHT // 2) // CELL_SIZE * CELL_SIZE
        self.position = (start_x, start_y)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    snake = Snake()
    apple = Apple()

    while apple.position in snake.positions:
        apple.randomize_position()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        head_pos = snake.get_head_position()
        if head_pos in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
