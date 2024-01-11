import pygame
import board


def game_loop():
    pygame.display.set_caption('checkers')
    screen_size = (500, 550)
    board_offset = 50
    game = board.board()
    selected = game.get_checker(0, 1)

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    in_game = True
    jump_count = 0

    black = (0, 0, 0)
    font = pygame.font.Font("freesansbold.ttf", 22)

    text = font.render('end-turn', True, black)
    text_rect = text.get_rect()
    text_rect.center = (250, 500)

    menu_text = font.render("game-over", True, black)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (250, 500)

    while in_game and not game.is_game_over():

        screen.fill((0, 0, 0))
        game.reset()
        game.draw(screen, board_offset, board_offset, selected)
        pygame.draw.rect(screen, (255, 0, 0), (185, 475, 125, 50))
        screen.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 450 <= pos[0] <= 575 and 450 <= pos[1] <= 500:
                    if jump_count > 0:
                        selected = game.change_turn(selected)
                        jump_count = 0
                col = (pos[1] - board_offset) // 50
                row = (pos[0] - board_offset) // 50
                if game.is_occupied(row, col):
                    if selected.get_team() == game.get_checker(row, col).get_team():
                        selected = game.get_checker(row, col)
                    else:
                        if game.jump(selected, game.get_checker(row, col), True):
                            jump_count += 1
                            if selected.is_new_king():
                                row, col = selected.get_loc()
                                selected = game.king(row, col, selected.get_team())
                            if not game.valid_extra_jump(selected):
                                selected = game.change_turn(selected)
                                jump_count = 0
                else:
                    if (row + col) % 2 == 1:
                        if not game.is_valid_jump(selected.get_team()):
                            if game.move(selected, row, col):
                                if selected.is_new_king():
                                    row, col = selected.get_loc()
                                    selected = game.king(row, col, selected.get_team())
                                selected = game.change_turn(selected)

    pygame.draw.rect(screen, (0, 255, 0), (185, 475, 125, 50))
    screen.blit(menu_text, menu_rect)
    pygame.display.update()


game_loop()
in_menu = True

while in_menu:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            in_menu = False

        if action.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 450 <= mouse_pos[0] <= 575 and 450 <= mouse_pos[1] <= 500:
                game_loop()

