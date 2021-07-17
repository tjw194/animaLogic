# create the constants
board_width = 4
board_height = 4

# take user input for board size
board_size = input('Enter integer for board size (e.g. "4" for 4x4 board): ')
if board_size:
    board_size = int(board_size)
    board_width = board_size
    board_height = board_size

tile_size = 80 * (4 / board_height)
icon_size = int(0.8 * tile_size)

window_width = 800

window_height = 640

# num of rows needed to display all picked tiles
panel_rows = ((board_height*board_width) // (window_width // tile_size)) + 1
panel_height = panel_rows * tile_size
fps = 30

# color pallete - rgb values
black = (0, 0, 0)
white = (255, 255, 255)
dark_khaki = (168, 184, 92)
dark_green = (0, 176, 29)
magic_mint = (153, 255, 187)
dark_blue = (0, 25, 50)

bg_color = dark_khaki
tile_color = black
text_color = white
border_color = dark_green
font_size = 36
tile_font_size = 12

button_color = white
button_text_color = black
message_color = white

# creating a margin equal to half of a tile size?
x_margin = int((window_width - (tile_size * board_width + (board_width - 1))) / 2)
y_margin = int((window_height - panel_height - (tile_size * board_height + (board_height - 1))) - 10)

# set up piece icons
icon_path = 'images/piece_images/'
piece_icons = {'axolotl': 'axolotl.png',
               'cat': 'cat.png',
               'elephant': 'elephant.png',
               'bird': 'bird.png',
               'unicorn': 'unicorn.png',
               'flamingo': 'flamingo.png',
               'fish': 'fish.png',
               'pig': 'pig.png',
               'cow': 'cow.png',
               'duck': 'duck.png',
               'haunter': 'haunter.png',
               'man': 'man.png',
               'turtle': 'turtle.png',
               'black': 'black.png',
               'cursola': 'cursola.png',
               'snake': 'snake.png',
               'frog': 'frog.png',
               'jellyfish': 'jellyfish.png',
               'tadpole': 'tadpole.png',
               'bunny': 'bunny.png',
               'gloom': 'gloom.png',
               'camel': 'camel.png',
               'giraffe': 'giraffe.png',
               'hippo': 'hippo.png',
               'monkey': 'monkey.png',
               'lion': 'lion.png'}

# enter the piece information
animals = [animal for animal in piece_icons.keys()]
colors = ['tomato', 'green', 'royalblue', 'yellow', 'orange2', 'purple4', 'gray', 'pink', 'saddlebrown', 'peachpuff', 'white', 'paleturquoise']


