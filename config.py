# create the constants
board_width = 4
board_height = 4
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

bg_color = dark_blue
tile_color = black
text_color = white
border_color = dark_green
font_size = 40
tile_font_size = 12

button_color = white
button_text_color = black
message_color = white

# creating a margin equal to half of a tile size?
x_margin = int((window_width - (tile_size * board_width + (board_width - 1))) / 2)
y_margin = int((window_height - panel_height - (tile_size * board_height + (board_height - 1))) - 10)

# set up piece icons
icon_path = 'images/piece_images/'
piece_icons = {'hippo': 'hippo.png',
               'lion': 'lion.png',
               'camel': 'camel.png',
               'giraffe': 'giraffe.png',
               'monkey': 'monkey.png',
               'axolotl': 'axolotl.png',
               'cat': 'cat.png',
               'elephant': 'elephant.png',
               'bird': 'bird.png',
               'unicorn': 'unicorn.png'}

# enter the piece information
animals = [animal for animal in piece_icons.keys()]
colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'gray', 'pink', 'saddlebrown', 'peachpuff', 'white']


