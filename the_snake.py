"""Курсовой проект: модуль игры 'Змейка'."""
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Центр экрана:
DISPLAY_CENTRE = (320, 240)

# Занятые клетки игрового поля:
taken_positions: list[tuple] = []

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Игровой объект для наследования."""

    def __init__(self):
        """Метод ввода данных игрового объекта."""
        self.position = DISPLAY_CENTRE
        self.body_color = None

    def draw(self):
        """Пустой метод отрисовки."""
        raise NotImplementedError


class Apple(GameObject):
    """'Яблоко', дочерний игровой объект."""

    def __init__(self):
        """Метод ввода данных объекта 'Яблоко'."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод выбора случаного расположения объекта 'Яблоко'."""
        while True:
            new_position = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                            (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
            if new_position not in taken_positions:
                self.position = new_position
                return self.position

    def draw(self):
        """Метод отрисовки объекта 'Яблоко'."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """'Змейка', дочерний игровой объект."""

    def __init__(self):
        """Метод ввода данных объекта 'Змейка'."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод получения расположения головы Змейки."""
        return self.positions[0]

    def draw(self):
        """Метод отрисовки объекта 'Змейка'."""
        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод движения объекта 'Змейка'."""
        head_coordinate_x, head_coordinate_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head_x = (head_coordinate_x
                      + GRID_SIZE * direction_x) % SCREEN_WIDTH
        new_head_y = (head_coordinate_y
                      + GRID_SIZE * direction_y) % SCREEN_HEIGHT
        self.positions.insert(0, (new_head_x, new_head_y))
        self.last = self.positions[-1]
        while len(self.positions) > self.length:
            del self.positions[-1]
        global taken_positions
        taken_positions = self.positions

    def update_direction(self):
        """Метод обновления направления движения Змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод перезапуска объекта 'Змейка'."""
        for position in self.positions[1:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        for _ in self.positions[1:-1]:
            _ = None
        self.length = 1
        self.positions[0] = DISPLAY_CENTRE
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(game_object):
    """Метод обработки действий игрока."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главный метод, инициализация игры."""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position()
        snake.draw()
        apple.draw()
        if snake.positions[0] in snake.positions[1:-1]:
            snake.reset()
        pg.display.update()


if __name__ == '__main__':
    main()
