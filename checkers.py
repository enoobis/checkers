import pygame
import math

class checker:
    def __init__(self, row, col, color):
        self.row, self.col, self.color = row, col, color
        self.active, self.king = True, False

    def defeat(self):
        self.active = False

    def draw(self, surface, x, y):
        pygame.draw.circle(surface, self.get_team(), (x, y), 10)

    def get_loc(self):
        return self.row, self.col

    def get_team(self):
        return self.color

    def is_alive(self):
        return self.active

    def is_king(self):
        return self.king

    def is_new_king(self):
        return (self.get_team() == "Blue" and self.row == 7) or (self.get_team() == "Red" and self.row == 0)

    def is_valid_move(self, new_r, new_c):
        if self.color == "Blue":
            return math.fabs(self.col - new_c) == 1 and new_r - 1 == self.row

        if self.color == "Red":
            return math.fabs(self.col - new_c) == 1 and new_r + 1 == self.row

    def jump(self, enemy):
        e_r, e_c = enemy.get_loc()
        row, col = self.get_loc()

        if (self.get_team() == "Red" or self.is_king()) and e_r + 1 == row and row - 2 >= 0:
            if math.fabs(col - e_c) == 1:
                return (col - e_c == 1 and e_r != 0 and e_c != 0) or (e_r != 0 and e_c != 7)

        if (self.get_team() == "Blue" or self.is_king()) and e_r - 1 == row and row + 2 <= 7:
            if math.fabs(col - e_c) == 1:
                return (col - e_c == 1 and e_r != 7 and e_c != 0) or (e_r != 7 and e_c != 7)

        return False

    def move(self, row, col):
        if self.is_valid_move(row, col):
            self.set_loc(row, col)
            return True
        return False

    def set_loc(self, row, col):
        self.row, self.col = row, col