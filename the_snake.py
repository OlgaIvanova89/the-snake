from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_COORDINATES = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Словарь для смены направления:
KEY_DIRECTIONS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

# Цвета объектов игры:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
PINK_COLOR = (255, 0, 155)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый объект игры.

    Обеспечивает общую логику инициализации Змейки и Яблока.
    """

    def __init__(self, position=CENTER_COORDINATES, body_color=PINK_COLOR):
        """Инициализирует базовые атрибуты объекта.

        Args:
        position(tuple(x, y)): Начальное положение объекта в середине игрового
        поля.
        body_color(tuple(0, 0, 0)): Цвет объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объекты игры.

        Будет переопределен в классах-наследниках.
        """
        raise NotImplementedError

    def draw_cell(self, position, color=None, border_color=BORDER_COLOR):
        """Отрисовывает одну ячейку по заданной позиции.

        Args:
            position (tuple(x, y)): Координаты положения ячейки.
            color (tuple, (0, 0, 0)): Необязательный параметр цвета (RGB).
        """
        cell_color = color or self.body_color
        cell_rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, cell_color, cell_rect)
        pg.draw.rect(screen, border_color, cell_rect, 1)


class Snake(GameObject):
    """Объект-змейка.

    Реализует логику движения, отрисовки и обработку событий
    поведения змейки в игре.

    Args:
    GameObject (object): класс-родитель.
    """

    def __init__(self, position=CENTER_COORDINATES, body_color=PINK_COLOR):
        """Инициализирует базовый атрибут объекта.

        Args:
        body_color(tuple(0, 0, 0)): Цвет объекта.
        reset(method): Возврат змейки в исходное состояние.
        """
        super().__init__(position, body_color)
        self.reset()

    def move(self):
        """Обрабатывает движение и столкновения змейки с краями игрового поля
        и с частями самой змейки.
        """
        self.update_direction()
        current_head_x, current_head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head_x = (current_head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (current_head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)

        # Удаление последнего сегмента змейки при движении.
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Возвращает змейку в исходное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.next_direction = None
        self.last = None
        self.direction = choice(DIRECTIONS)

    def draw(self):
        """Отрисовывает тело змейки."""
        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(
                self.last,
                BOARD_BACKGROUND_COLOR,
                BOARD_BACKGROUND_COLOR
            )

        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position())

    def get_head_position(self):
        """Возвращает координаты положения головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет текущее направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


class Apple(GameObject):
    """Объект-яблоко.

    Задает координаты яблоку на игровом поле и отрисовывает
    яблоко на игровом поле.

    Args:
    GameObject (object): класс-родитель.
    """

    def __init__(
        self,
        position=CENTER_COORDINATES,
        body_color=PINK_COLOR
    ):
        """Инициализирует базовые атрибуты объекта.

        Args:
        body_color(tuple(0, 0, 0)): Цвет объекта.
        position(tuple(x, y)): Координаты положения яблока на поле.
        banned_positions(list): Список занятых змейкой координат поля.
        """
        super().__init__(position, body_color)

    def randomize_position(self, banned_positions):
        """Задает случайные координаты новому яблоку на игровом поле.

        Координаты генеририуются до тех пор, пока не будут выбраны свободные
        координаты.

        Args:
        banned_positions(list): Список занятых змейкой координат поля.

        Returns:
        Новые координаты яблока x и y.
        """
        while True:
            rect_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            rect_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (rect_x, rect_y)
            if new_position not in banned_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position)


def handle_keys(game_object):
    """Отрабатывает нажатие пользователем кнопок Вверх, Вниз, Влево и Вправо
    на клавиатуре.

    Args:
    game_object (object): Объект игры.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            game_object.next_direction = KEY_DIRECTIONS.get(
                (game_object.direction, event.key),
                game_object.direction
            )


def main():
    """Запускает игру."""
    pg.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake(body_color=SNAKE_COLOR)
    apple = Apple(body_color=APPLE_COLOR)
    apple.randomize_position(snake.positions)
    apple.draw()
    while True:
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
