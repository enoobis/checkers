import pygame
import math
import checkers as chs

class king(chs.checker):

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True

    def draw(self, surface, x, y):
        super().draw(surface, x, y)

        white = (255, 255, 255)
        king_font = pygame.font.Font('freesansbold.ttf', 12)
        king_text = king_font.render('K', True, white)
        king_rect = king_text.get_rect(center=(x, y))
        surface.blit(king_text, king_rect)

    def is_valid_move(self, new_r, new_c):
        row, col = self.get_loc()
        return math.fabs(col - new_c) == 1 and math.fabs(row - new_r) == 1
