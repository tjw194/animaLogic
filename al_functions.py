import pygame
import sys
import random
from pygame.locals import *
from config import *


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
    for i in range(board_width):
        l1.append(animals[i])
    l2 = []
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


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move ==LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getSpotClicked(board, x, y):
    # from teh x, y coordinates get the x, y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TITLESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def drawTile (tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley
    # optionally a few pixels over determined by adjx and adj
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def make_text(font_object, text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text
    text_surf = font_object.render(text, True, color, bgcolor)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return (text_surf, text_rect)


def draw_board(display_surface, font_object, board, message):
    display_surface.fill(bg_color)
    if message:
        text_surf, text_ref = make_text(font_object, message, message_color, bg_color, 5, 5)

        display_surface.blit(text_surf, text_ref)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                draw_tile(tilex, tiley, board[tilex][tiley])

    left, top = get_top_left_of_tile(0, 0)
    width = board_width * tile_size
    height = board_height * tile_size
    pygame.draw.rect(display_surface, border_color, (left - 5, top - 5, width + 11, height +11), 4)

    display_surface.blit(RESET_SURF, RESET_RECT)
    display_surface.blit(NEW_SURF, NEW_RECT)
    display_surface.blit(SOLVE_SURF, SOLVE_RECT)
    display_surface.blit(UNDO_SURF, UNDO_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # note this function does not check if the move is valid
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # from a starting configuration make numSlides number of moves
    # and animate these moves
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)

    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', int(TILESIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return  (board, sequence)


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse
    revAllMoves = allMoves[:]
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove == RIGHT
        slideAnimation(board, oppositeMove, '', int(TITLESIZE / 2))
        makeMove(board, oppositeMove)


