from random import choice, randint

import pygame

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
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Описание классов игры.
class GameObject:
    """Базовый класс игры. От него наследуются основные объекты игры."""

    def __init__(self, body_color=None):
        """Инициализирует базовые атрибуты объекта.

        Args:
        position(tuple(x, y)): Начальное положение объекта в середине игрового
        поля.
        body_color(tuple(0, 0, 0)): Цвет объекта.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw():
        """Отрисовывает объекты игры. Будет переопределен в
        классах-наследниках.
        """
        pass


class Snake(GameObject):
    """Объект-змейка. Реализует логику движения, отрисовки и обработку событий
    поведения змейки в игре.

    Args:
    GameObject (object): класс-родитель.
    """

    def __init__(self, body_color=None):
        """Инициализирует базовый атрибут объекта.

        Args:
        body_color(tuple(0, 0, 0)): Цвет объекта.
        reset(method): Возврат змейки в исходное состояние.
        """
        super().__init__(body_color)
        self.reset()

    def move(self):
        """Обрабатывает движение и столкновения змейки с краями игрового поля
        и с частями самой змейки.
        """
        self.update_direction()
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        if new_head in self.positions:
            self.reset()
            return
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
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты положения головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет текущее направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


class Apple(GameObject):
    """Объект-яблоко. Задает координаты яблоку на игровом поле и отрисовывает
    яблоко на игровом поле.

    Args:
    GameObject (object): класс-родитель.
    """

    def __init__(self, body_color=None):
        """Инициализирует базовые атрибуты объекта.

        Args:
        body_color(tuple(0, 0, 0)): Цвет объекта.
        position(tuple(x, y)): Координаты положения яблока на поле.
        """
        super().__init__(body_color)
        self.position = tuple(self.randomize_position())

    def randomize_position(self):
        """Задает случайные координаты новому яблоку на игровом поле.

        Returns:
        Новые координаты яблока x и y.
        """
        self.rect_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.rect_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return self.rect_x, self.rect_y

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Отрабатывает нажатие пользователем кнопок Вверх, Вниз, Влево и Вправо
    на клавиатуре.

    Args:
    game_object (object): Объект игры.
    """
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
    """Запускает игру."""
    # Инициализация PyGame:
    pygame.init()
    # Cоздание экземпляров классов яблока и змейки.
    apple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)
    # Основной цикл игры.
    while True:
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
