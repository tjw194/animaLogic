import copy
from pygame import mixer
import pygame
import sys
import random
from pygame.locals import *
from config import *

all_moves = []

# initialize pygame
pygame.init()
fps_clock = pygame.time.Clock()
display_surf = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('AnimaLogic')
icon = pygame.image.load('./images/giraffe (1).png')
pygame.display.set_icon(icon)
basic_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', font_size)
small_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', tile_font_size)

# background with river, lake and bridge
background = pygame.image.load('./images/background2.png')

assist_mode = False
on_track = True


def make_text(text, color, bg_color, top, left):
    # create the Surface and Rect objects for some text
    text_surf = basic_font.render(text, True, color, bg_color)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return (text_surf, text_rect)


# store the option buttons and their rectangles in OPTIONS
undo_surf, undo_rect = make_text('Undo Move', text_color, tile_color, window_width - 220, window_height - panel_height - 240)
reset_surf, reset_rect = make_text('Reset', text_color, tile_color, window_width - 220, window_height - panel_height - 180)
solve_surf, solve_rect = make_text('Solve', text_color, tile_color, window_width - 220, window_height - panel_height - 120)
new_surf, new_rect = make_text('New Game', text_color, tile_color, window_width - 220, window_height - panel_height - 60)
assist_surf, assist_rect = make_text(str(on_track), text_color, tile_color, 0, window_height - panel_height - 60)


def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()

        pygame.event.post(event)


def get_pieces():
    l1 = []
    random.shuffle(animals)
    for i in range(board_width):
        l1.append(animals[i])
    l2 = []
    random.shuffle(colors)
    for i in range(board_height):
        l2.append(colors[i])
    pieces = []
    for a in l1:
        for c in l2:
            pieces.append(c + ' ' + a)
    return pieces


def get_starting_board(pieces, shuffle=True):
    # return a board data structure
    # given list of pieces
    # shuffled or unshuffled

    if shuffle:
        random.shuffle(pieces)

    board = []
    for x in range(board_width):
        column = []
        for y in range(board_height):
            column.append(pieces.pop(0))

        board.append(column)

    return board


def get_options(board):
    # gets available choices for a given board - does not check validity
    options = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] is not None:
                options.append(board[x][y])
                break
    return options


def valid_move(choice, board):
    if choice is None:
        return False
    options = get_options(board)
    color = choice.split(' ')[0]
    animal = choice.split(' ')[1]

    if choice in options:
        if all_moves:
            match = all_moves[-1]
            if color == match.split(' ')[0] or animal == match.split(' ')[1]:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def get_left_top_of_tile(tile_x, tile_y):
    left = x_margin + (tile_x * tile_size) + (tile_x - 1)
    top = y_margin + (tile_y * tile_size) + (tile_y - 1)
    return (left, top)


def get_left_top_of_panel_tile(order):
    # get left top pixel location of the nth tile in the panel

    # checking if tile needs to wrap to next row
    row = order // (window_width // tile_size)

    left = (order % (window_width // tile_size)) * tile_size
    top = (window_height - panel_height) + row * tile_size

    return (left, top)



def get_spot_clicked(board, x, y):
    # from teh x, y coordinates get the x, y board coordinates
    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            left, top = get_left_top_of_tile(tile_x, tile_y)
            tile_rect = pygame.Rect(left, top, tile_size, tile_size)
            if tile_rect.collidepoint(x, y):
                return (tile_x, tile_y)
    return (None, None)


def draw_tile(tile_x, tile_y, piece, adjx=0, adjy=0):
    # draw a tile at board coordinates tile_x and tile_y
    # optionally a few pixels over determined by adjx and adj

    # parse piece info
    color = piece.split(' ')[0]
    animal = piece.split(' ')[1]

    left, top = get_left_top_of_tile(tile_x, tile_y)
    pygame.draw.rect(display_surf, color, (left + adjx + 2, top + adjy, tile_size - 4, tile_size))

    animal_icon = pygame.image.load(icon_path + piece_icons[animal])
    animal_icon = pygame.transform.scale(animal_icon, (icon_size, icon_size))

    img_rect = animal_icon.get_rect()
    img_rect.center = left + int(tile_size / 2) + adjx, top + int(tile_size / 2) + adjy
    display_surf.blit(animal_icon, img_rect)


def draw_picked_tile(order, piece, adjx=0, adjy=0):
    # draw a tile at panel coordinates tile_x and tile_y
    # optionally a few pixels over determined by adjx and adj

    # parse piece info
    color = piece.split(' ')[0]
    animal = piece.split(' ')[1]

    # checking if tile needs to wrap to next row
    row = order // (window_width // tile_size)

    left = (order % (window_width // tile_size)) * tile_size
    top = (window_height - panel_height) + row * tile_size

    pygame.draw.rect(display_surf, color, (left + adjx, top + adjy, tile_size, tile_size))
    icon = pygame.image.load(icon_path + piece_icons[animal])
    icon = pygame.transform.scale(icon, (icon_size, icon_size))

    img_rect = icon.get_rect()
    img_rect.center = left + int(tile_size / 2) + adjx, top + int(tile_size / 2) + adjy
    display_surf.blit(icon, img_rect)


def animate_tile(tile_x, tile_y, speed, piece, adjx=0, adjy=0):
    # animate tile move to panel

    # get starting and ending pixel locations
    left_start, top_start = get_left_top_of_tile(tile_x, tile_y)
    left_end, top_end = 320, -1.75 * tile_size  # moving approximately to the bridge and just off screen

    # parse piece info
    color = piece.split(' ')[0]
    animal = piece.split(' ')[1]

    base_surf = display_surf.copy()
    for i in range(speed):
        display_surf.blit(base_surf, (0, 0))

        left = int(left_start + ((left_end - left_start) * (i / speed)))
        top = int(top_start + ((top_end - top_start) * (i / speed)))

        pygame.draw.rect(display_surf, color, (left + adjx + 2, top + adjy, tile_size - 4, tile_size))

        animal_icon = pygame.image.load(icon_path + piece_icons[animal])
        animal_icon = pygame.transform.scale(animal_icon, (icon_size, icon_size))

        img_rect = animal_icon.get_rect()
        img_rect.center = left + int(tile_size / 2) + adjx, top + int(tile_size / 2) + adjy
        display_surf.blit(animal_icon, img_rect)

        pygame.display.update()
        fps_clock.tick(fps)

def draw_board(board, message):
    display_surf.fill(bg_color)
    display_surf.blit(background, (0, 20))
    if message:
        text_surf, text_ref = make_text(message, message_color, button_text_color, 5, 5)

        display_surf.blit(text_surf, text_ref)

    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            if board[tile_x][tile_y]:
                draw_tile(tile_x, tile_y, board[tile_x][tile_y])

    left, top = get_left_top_of_tile(0, 0)
    width = board_width * tile_size
    height = board_height * tile_size
    pygame.draw.rect(display_surf, border_color, (left - 5, top - 5, width + 11, height + 11), 4)

    display_surf.blit(reset_surf, reset_rect)
    display_surf.blit(new_surf, new_rect)
    display_surf.blit(solve_surf, solve_rect)
    display_surf.blit(undo_surf, undo_rect)

    # assist mode display
    if assist_mode:
        display_surf.blit(assist_surf, assist_rect)

    # draw panel to hold picked tiles
    pygame.draw.rect(display_surf, tile_color, pygame.Rect(0, window_height - panel_height, window_width, panel_height), 3)
    for _, move in enumerate(all_moves):
        draw_picked_tile(_, move)


paths = []


def pathfinder(board, path=[]):
    options = get_options(board)

    if not path:
        pot_paths = copy.deepcopy(options)
    else:
        choice = path[-1]
        pot_paths = []
        for option in options:
            if (choice.split(' ')[0] == option.split(' ')[0]) or (choice.split(' ')[1] == option.split(' ')[1]):
                pot_paths.append(option)
    # base case
    if not pot_paths:
        paths.append(path)
        return paths
    else:
        for choice in pot_paths:
            new_board = copy.deepcopy(board)
            new_path = copy.deepcopy(path)
            new_path.append(choice)
            for x in range(len(board)):
                for y in range(len(board[x])):
                    if choice == board[x][y]:
                        new_board[x][y] = None
            pathfinder(new_board, new_path)


solutions = []


def solver():
    for path in paths:
        if len(path) == board_width * board_height:
            solutions.append(path)
    return solutions, len(solutions), len(paths)


def main():

    global all_moves, paths, solutions, assist_surf, assist_rect, assist_mode

    while not solutions:
        main_board = get_starting_board(get_pieces())
        pathfinder(main_board)
        solutions, num_sols, num_paths = solver()

        # print(num_sols, num_paths)

    # background sound
    if music in ['y', 'yes', 'Yes']:
        mixer.music.load('./sounds/animaLogic.wav')
        mixer.music.play(-1)

    win_state = False
    on_track = True
    # save a copy for undo and reset functions
    start_board = copy.deepcopy(main_board)

    while True:  # main game loop

        # update solveable status for assist mode
        assist_surf, assist_rect = make_text(str(on_track), text_color, tile_color, 20, window_height - panel_height - 60)

        msg = f'The are {num_sols} solution(s) out of {num_paths} paths'  # contains the message to show in the upper left

        # print True if current path is solveable
        if len(all_moves) > 0:
            for solution in solutions:
                if solution[0:len(all_moves)] == all_moves:
                    on_track = True
                    break
                else:
                    on_track = False

        # when puzzle is solved
        if len(all_moves) == board_width * board_height:
            msg = 'Solved!'
            if not win_state:
                win_state = True
                win_sound = mixer.Sound('./sounds/applause.wav')
                win_sound.set_volume(0.5)
                win_sound.play()

        draw_board(main_board, msg)

        # clicking on the buttons
        check_for_quit()
        for event in pygame.event.get():
            # toggle assist mode
            if event.type == KEYDOWN:
                if event.key == pygame.K_a:
                    if assist_mode == False:
                        assist_mode = True
                    else:
                        assist_mode = False

            if event.type == MOUSEBUTTONUP:

                spot_x, spot_y = get_spot_clicked(main_board, event.pos[0], event.pos[1])

                if (spot_x, spot_y) == (None, None):

                    # check if the user clicked on an option button
                    if reset_rect.collidepoint(event.pos):
                        win_state = False
                        main_board = copy.deepcopy(start_board)
                        draw_board(main_board, msg)
                        all_moves = []
                    elif new_rect.collidepoint(event.pos):
                        win_state = False
                        paths = []
                        solutions = []
                        while not solutions:
                            main_board = get_starting_board(get_pieces())
                            pathfinder(main_board)
                            solutions, num_sols, num_paths = solver()

                            # print(num_sols, num_paths)
                        start_board = copy.deepcopy(main_board)

                        all_moves = []
                    elif solve_rect.collidepoint(event.pos):
                        win_state = True
                        solved_moves = solutions[random.randint(0, len(solutions)-1)]
                        for move in solved_moves:
                            for x in range(len(start_board)):
                                for y in range(len(start_board[x])):
                                    if move == start_board[x][y]:
                                        spot_x = x
                                        spot_y = y
                            main_board[spot_x][spot_y] = None
                            draw_board(main_board, msg)
                            animate_tile(spot_x, spot_y, 5, move)
                        all_moves = solved_moves
                        draw_board(main_board, msg)
                    elif undo_rect.collidepoint(event.pos):
                        if len(all_moves) > 0:
                            last_move = all_moves.pop(-1)
                            for x in range(len(start_board)):
                                for y in range(len(start_board[x])):
                                    if last_move == start_board[x][y]:
                                        main_board[x][y] = last_move
                else:
                    # make sure choice is valid
                    if valid_move(main_board[spot_x][spot_y], main_board):

                        # make the click sound
                        click_sound = mixer.Sound('./sounds/click.wav')
                        click_sound.set_volume(0.5)
                        click_sound.play()

                        # grab the chosen piece
                        piece = main_board[spot_x][spot_y]

                        # update board, list of moves and send tile to the bridge
                        main_board[spot_x][spot_y] = None
                        draw_board(main_board, msg)
                        all_moves.append(piece)
                        animate_tile(spot_x, spot_y, 10, piece)



        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
