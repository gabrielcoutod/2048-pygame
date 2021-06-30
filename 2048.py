import pygame
from enum import Enum
import random


class Game2048:
    """
    Implementation of 2048 with pygame.
    0   1   2   3
    4   5   6   7
    8   9   10  11
    12  13  14  15
    """
    SCREEN_COLOR = (208, 116, 58)  # color of the screen
    TEXT_COLOR = (0, 0, 0)  # color of text
    WIN_BACKGROUND = (208, 116, 58)  # background color of the win message
    LOSE_BACKGROUND = (208, 116, 58)  # background color of the lose message
    GRID_POS = (151, 51)  # position of the grid
    RES = (800, 600)  # resolution of the screen
    LOSE_SIZE = 50  # lose message size
    WIN_SIZE = 50  # win message size
    NUMBERS_SIZE = 32  # size of the numbers on the grid
    SQUARE_SIZE = 105  # size of the square
    NUMBER_CELLS = 16  # number of cells on the grid
    NO_VALUE = 0  # indicates that there isn't a value on the cell
    NUMBER_ROWS = 4  # number of rows
    NUMBER_COLUMNS = 4  # number of columns
    SCORE_SIZE = 32  # size of the score
    SCORE_CENTER = (400, 570)  # center of the score message

    # position of the cells
    CELLS_POS = [(14 + 105 * i + 16 * i + 151, 51 + 15 + 105 * j + 16 * j)
                 for j in range(4) for i in range(4)]

    class State(Enum):
        """
        Possible states of the game.
        """
        game = 1
        lose = 2
        win = 3

    class Keys(Enum):
        """
        Indicates keys in the game.
        """
        no_key = -1
        left = 1
        right = 2
        up = 3
        down = 4
        enter = 5
        esc = 6

    def __init__(self):
        """
        Initializes the game.
        """
        # initializes pygame
        pygame.init()
        # initializes the screen
        self.screen = pygame.display.set_mode(Game2048.RES)
        self.grid_img = pygame.image.load("grid.png")
        pygame.display.set_caption("2048")
        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)
        # initializes the grid
        self.grid = [Game2048.NO_VALUE for i in range(Game2048.NUMBER_CELLS)]
        self.random_number()
        self.random_number()
        # initializes game variables
        self.state = Game2048.State.game
        self.running = True
        self.game_score = 0

    def random_number(self):
        """
        Puts a random number on an empty cell.
        """
        empty = [i for i in range(Game2048.NUMBER_CELLS) if self.grid[i] == Game2048.NO_VALUE]
        if empty:
            index = random.choice(empty)
            val = 2 if random.randint(1, 10) <= 9 else 4
            self.grid[index] = val

    def event(self):
        """
        Updates the game based on the pressed keys.
        """
        for event in pygame.event.get():
            key = self.key_pressed(event) if event.type == pygame.KEYDOWN else Game2048.Keys.no_key

            if event.type == pygame.QUIT or key == Game2048.Keys.esc:
                self.running = False
            elif key == Game2048.Keys.enter:
                self.state = Game2048.State.game
                self.reset()
            elif self.state == Game2048.State.game:
                if key == Game2048.Keys.left:
                    if self.left(self.grid):
                        self.random_number()
                elif key == Game2048.Keys.right:
                    if self.right(self.grid):
                        self.random_number()
                elif key == Game2048.Keys.up:
                    if self.up(self.grid):
                        self.random_number()
                elif key == Game2048.Keys.down:
                    if self.down(self.grid):
                        self.random_number()

    def left(self, grid: list) -> bool:
        """
        Moves the grid to the left. Returns True if any number moved, False if all cells
        stayed at the same position.
        """
        moved = False
        changed = []
        for i in range(Game2048.NUMBER_ROWS):
            for j in range(Game2048.NUMBER_COLUMNS - 1):
                index = 4 * i + j + 1
                if grid[index] != Game2048.NO_VALUE:
                    while index > 4 * i and grid[index - 1] == Game2048.NO_VALUE:
                        grid[index - 1] = grid[index]
                        grid[index] = Game2048.NO_VALUE
                        index -= 1
                        moved = True
                    if index > 4 * i and grid[index - 1] == grid[index] and index - 1 not in changed:
                        grid[index - 1] = 2 * grid[index]
                        self.game_score += 2 * grid[index]
                        grid[index] = Game2048.NO_VALUE
                        moved = True
                        changed.append(index - 1)
        return moved

    def right(self, grid: list) -> bool:
        """
        Moves the grid to the right. Returns True if any number moved, False if all cells
        stayed at the same position.
        """
        moved = False
        changed = []
        for i in range(Game2048.NUMBER_ROWS):
            for j in range(Game2048.NUMBER_COLUMNS - 1):
                index = 4 * i + 2 - j
                if grid[index] != Game2048.NO_VALUE:
                    while index + 1 < 4 * (i + 1) and grid[index + 1] == Game2048.NO_VALUE:
                        grid[index + 1] = grid[index]
                        grid[index] = Game2048.NO_VALUE
                        index += 1
                        moved = True
                    if index + 1 < 4 * (i + 1) and grid[index + 1] == grid[index] and index + 1 not in changed:
                        grid[index + 1] = 2 * grid[index]
                        self.game_score += 2 * grid[index]
                        grid[index] = Game2048.NO_VALUE
                        moved = True
                        changed.append(index + 1)
        return moved

    def up(self, grid: list) -> bool:
        """
        Moves the grid up. Returns True if any number moved, False if all cells
        stayed at the same position.
        """
        moved = False
        changed = []
        for i in range(Game2048.NUMBER_COLUMNS):
            for j in range(Game2048.NUMBER_ROWS - 1):
                index = 4 + i + 4 * j
                if grid[index] != Game2048.NO_VALUE:
                    while index - 4 >= i and grid[index - 4] == Game2048.NO_VALUE:
                        grid[index - 4] = grid[index]
                        grid[index] = Game2048.NO_VALUE
                        index -= 4
                        moved = True
                    if index - 4 >= i and grid[index - 4] == grid[index] and index - 4 not in changed:
                        grid[index - 4] = 2 * grid[index]
                        self.game_score += 2 * grid[index]
                        grid[index] = Game2048.NO_VALUE
                        moved = True
                        changed.append(index - 4)
        return moved

    def down(self, grid: list) -> bool:
        """
        Moves the grid down. Returns True if any number moved, False if all cells
        stayed at the same position.
        """
        moved = False
        changed = []
        for i in range(Game2048.NUMBER_COLUMNS):
            for j in range(Game2048.NUMBER_ROWS - 1):
                index = 8 + i - 4 * j
                if grid[index] != Game2048.NO_VALUE:
                    while index + 4 <= i + 12 and grid[index + 4] == Game2048.NO_VALUE:
                        grid[index + 4] = grid[index]
                        grid[index] = Game2048.NO_VALUE
                        index += 4
                        moved = True
                    if index + 4 <= i + 12 and grid[index + 4] == grid[index] and index + 4 not in changed:
                        grid[index + 4] = 2 * grid[index]
                        self.game_score += 2 * grid[index]
                        grid[index] = Game2048.NO_VALUE
                        moved = True
                        changed.append(index + 4)
        return moved

    def start(self):
        """
        Starts the game.
        """
        while self.running:  # runs game
            self.screen.fill(Game2048.SCREEN_COLOR)  # fills background

            if 2048 in self.grid:  # checks if won the game
                self.state = Game2048.State.win
            elif Game2048.NO_VALUE not in self.grid and self.no_moves():  # checks if lost the game
                self.state = Game2048.State.lose
            self.event()  # checks the events
            self.draw_state()  # draws according to the state
            pygame.display.update()  # updates the display

    def no_moves(self) -> bool:
        """
        Checks if the player with a full grid can make more moves.
        """
        backup_grid = self.grid[:]
        score_backup = self.game_score
        if self.left(backup_grid) or self.right(backup_grid) or self.up(backup_grid) or self.down(backup_grid):
            self.game_score = score_backup
            return False
        return True

    def numbers(self):
        """
        Draws the numbers on the grid.
        """
        font = pygame.font.Font('freesansbold.ttf', Game2048.NUMBERS_SIZE)

        for i in range(Game2048.NUMBER_CELLS):
            if self.grid[i] != Game2048.NO_VALUE:
                text = font.render(f"{self.grid[i]}", True, Game2048.TEXT_COLOR, ())
                rect = text.get_rect()
                rect.center = (Game2048.CELLS_POS[i][0] + Game2048.SQUARE_SIZE / 2,
                               Game2048.CELLS_POS[i][1] + Game2048.SQUARE_SIZE / 2)

                self.screen.blit(text, rect)

    def reset(self):
        """
        Resets the game to play again.
        """
        self.grid = [Game2048.NO_VALUE for i in range(Game2048.NUMBER_CELLS)]
        self.random_number()
        self.random_number()
        self.game_score = 0

    def draw_state(self):
        """
        Draws on the screen according to the current state.
        """
        self.draw_grid()
        self.numbers()
        self.score()
        if self.state == Game2048.State.lose:
            self.lose()
        elif self.state == Game2048.State.win:
            self.win()

    def score(self):
        """
        Draws the score on the screen.
        """
        self.button(Game2048.SCORE_SIZE, f"SCORE: {self.game_score:010}", Game2048.TEXT_COLOR, Game2048.SCREEN_COLOR,
                    Game2048.SCORE_CENTER)

    def key_pressed(self, event: pygame.event.Event) -> Keys:
        """
        Checks and returns the key pressed.
        """
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            return Game2048.Keys.enter
        if event.key == pygame.K_ESCAPE:
            return Game2048.Keys.esc
        if event.key == pygame.K_LEFT:
            return Game2048.Keys.left
        if event.key == pygame.K_RIGHT:
            return Game2048.Keys.right
        if event.key == pygame.K_UP:
            return Game2048.Keys.up
        if event.key == pygame.K_DOWN:
            return Game2048.Keys.down

        return Game2048.Keys.no_key

    def draw_grid(self):
        """
        Draws the game grid.
        """
        self.screen.blit(self.grid_img, Game2048.GRID_POS)

    def win(self):
        """
        Draws the win message on the screen.
        """
        self.button(Game2048.WIN_SIZE, "YOU WIN", Game2048.TEXT_COLOR, Game2048.WIN_BACKGROUND,
                    (Game2048.RES[0] / 2, Game2048.RES[1] / 2))

    def lose(self):
        """
        Draws the lose message on the screen.
        """
        self.button(Game2048.LOSE_SIZE, "YOU LOSE", Game2048.TEXT_COLOR, Game2048.LOSE_BACKGROUND,
                    (Game2048.RES[0] / 2, Game2048.RES[1] / 2))

    def button(self, font_size: int, text: str, text_color: tuple, back_color: tuple, center: tuple):
        """
        Draws a button on the screen with back_color being the background color, center being the center of the
        rectangle, text being the text that will be written on the button, text_color the color of the text and
        font_size the size of the text.
        """
        font = pygame.font.Font('freesansbold.ttf', font_size)
        rect_text = font.render(text, True, text_color, back_color)
        rect = rect_text.get_rect()
        rect.center = center
        self.screen.blit(rect_text, rect)


if __name__ == '__main__':
    Game2048().start()  # starts the game
