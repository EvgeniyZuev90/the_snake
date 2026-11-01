from random import randint
from typing import Optional, Tuple

import pygame

Point = Tuple[int, int]
Color = Tuple[int, int, int]

SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

UP: Point = (0, -1)
DOWN: Point = (0, 1)
LEFT: Point = (-1, 0)
RIGHT: Point = (1, 0)

BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)
BORDER_COLOR: Color = (93, 216, 228)
APPLE_COLOR: Color = (255, 0, 0)
SNAKE_COLOR: Color = (0, 255, 0)
DEFAULT_COLOR: Color = (255, 255, 255)

SPEED: int = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, body_color: Color = DEFAULT_COLOR) -> None:
        self.position: Point = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color: Color = body_color

    def draw(self) -> None:
        """Заготовка метода для отрисовки объекта."""


class Apple(GameObject):
    """Класс, описывающий яблоко и его отрисовку."""

    def __init__(self, body_color: Color = APPLE_COLOR) -> None:
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайное положение яблока на игровой сетке."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self) -> None:
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку  и ее управление и  отрисовку."""

    def __init__(self, body_color: Color = SNAKE_COLOR) -> None:
        super().__init__(body_color)
        self.reset()

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length: int = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction: Point = RIGHT
        self.next_direction: Optional[Point] = None
        self.last: Optional[Point] = None

    def update_direction(self) -> None:
        """Обновляет текущее направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> Point:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Обновляет позицию змейки, добавляя новую голову и удаляя хвост."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head: Point = (new_x, new_y)

        self.position = new_head
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self) -> None:
        """Отрисовывает  змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш для изменения направления змейки."""
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


def main() -> None:
    """Основной цикл игры."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
    