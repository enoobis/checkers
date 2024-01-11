import checkers as chs
import pygame
import kings

class board:

    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.reds = []
        self.blues = []

        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 1:
                    if i <= 2:
                        self.grid[i][j] = chs.checker(i, j, "Blue")
                        self.blues.append(self.grid[i][j])
                    elif i >= 5:
                        self.grid[i][j] = chs.checker(i, j, "Red")
                        self.reds.append(self.grid[i][j])

    def change_turn(self, selected):
        enemy_team = self.blues if selected.get_team() == "Red" else self.reds
        return next((enemy for enemy in enemy_team if enemy.is_alive()), None)

    def draw(self, surface, corner_x, corner_y, selected):
        for i in range(8):
            for j in range(8):
                color = (255, 255, 255) if (i + j) % 2 == 0 else (0, 0, 0)
                pygame.draw.rect(surface, color, (corner_x + i * 50, corner_y + j * 50, 50, 50))

                if self.is_occupied(i, j):
                    x, y = corner_x + i * 50 + 25, corner_y + j * 50 + 25
                    if selected and selected.get_loc() == (i, j):
                        pygame.draw.circle(surface, (255, 195, 0), (x, y), 15)
                    self.grid[i][j].draw(surface, x, y)

    def get_checker(self, row, col):
        return self.grid[row][col]

    def is_game_over(self):
        return not self.reds or not self.blues

    def is_occupied(self, row, col):
        return 0 <= row <= 7 and 0 <= col <= 7 and self.grid[row][col] is not None

    def is_valid_jump(self, color):
        for my_checker, enemy_team in ((self.blues, self.reds), (self.reds, self.blues)):
            for my_piece in my_checker:
                if color == my_piece.get_team() and any(self.jump(my_piece, enemy, False) for enemy in enemy_team):
                    return True
        return False

    def jump(self, jumper, enemy, perform_move):
        if jumper.jump(enemy):
            e_r, e_c = enemy.get_loc()
            row, col = jumper.get_loc()
            r_displacement = 1 if jumper.get_team() == "Blue" else -1
            c_displacement = -(col - e_c)
            if jumper.is_king():
                r_displacement = -(row - e_r)
            
            if not self.is_occupied(row + 2 * r_displacement, col + 2 * c_displacement):
                if perform_move:
                    jumper.set_loc(row + 2 * r_displacement, col + 2 * c_displacement)
                    self.grid[row][col], self.grid[row + 2 * r_displacement][col + 2 * c_displacement] = None, jumper
                    enemy.defeat()
                return True
        return False

    def king(self, row, col, color):
        king = kings.King(row, col, color)
        self.grid[row][col] = king

        for team in (self.blues, self.reds):
            for i, piece in enumerate(team):
                if piece.get_loc() == (row, col):
                    team[i] = king
                    break

        return king

    def move(self, mover, row, col):
        if self.is_occupied(row, col):
            return False
        old_row, old_col = mover.get_loc()

        if mover.move(row, col):
            self.grid[old_row][old_col], self.grid[row][col] = None, mover
            return True
        return False

    def reset(self):
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] is not None and not self.grid[i][j].is_alive():
                    self.grid[i][j] = None
        self.reds = [piece for piece in self.reds if piece.is_alive()]
        self.blues = [piece for piece in self.blues if piece.is_alive()]

    def valid_extra_jump(self, checker):
        enemy_team = self.blues if checker.get_team() == "Red" else self.reds
        return any(self.jump(checker, enemy, False) and enemy.is_alive() for enemy in enemy_team)


