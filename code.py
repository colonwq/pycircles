import os
import time
import gc
import board
import busio
from digitalio import DigitalInOut
import neopixel
import displayio
import random
import math
from adafruit_display_shapes.circle import Circle

# more math == more time
# more rings == more math
# more smoothness == more math
NUM_RINGS = 20
RING_SPACING = 5
COLOR_ONE = 0xFF0000
COLOR_TWO = 0x00FF00
COLOR_BACKGROUND = 0x000000
SMOOTHNESS = 4
SLEEP_SECONDS = 0
MAX_WOBBLE = 5

#start the circles in the center-ish
P0x = 200
P0y = 120
P1x = 160
P1y = 120


def collect(verbose=0):
    if verbose==1:
        print("Amount of free memory: ", gc.mem_free() )
    gc.collect()
    if verbose==1:
        print("Amount of free ememory (after collect)", gc.mem_free())

def set_background_color(color):
    color_bitmap = displayio.Bitmap(320, 240, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = color

    tile_grid = displayio.TileGrid(
        color_bitmap,
        pixel_shader=color_palette,
        default_tile=0,
        x=0,  # Position relative to its parent group
        y=0,
        )

    basegroup.append(tile_grid)
    board.DISPLAY.show(basegroup)

#load settings
try:
    from secrets import secrets
except ImportError:
    print("Error loading settings file")

print("Loaded settings")

basegroup = displayio.Group(max_size=3)
#background, P0 and P1 circles

set_background_color(COLOR_BACKGROUND)

def draw_circle(h, k, r, target_bitmap, color):
    '''This function will draw a circle based on math found
    here: https://www.mathopenref.com/coordcirclealgorithm.html
    '''
    step = 2*math.pi/(r*SMOOTHNESS)
    #print("Step size: %f" % (step))
    theta = 0
    while theta < 2*math.pi:
        #using int() seems to make the points more jagged
        #x = int(h + r*math.cos(theta))
        #y = int(k - r*math.sin(theta))
        x = round(h + r*math.cos(theta))
        y = round(k - r*math.sin(theta))
        #print("X: %d\tY:%d" % (int(x), int(y)))
        #x must be between 0 and <320
        #y must be between 0 and <240

        #this version results in a line on the edge of the screen
        #as min(x), min(y) = 0, max(x) = 319
        #and max(y) 239
        #x = min(max(0,x),319)
        #y = min(max(0,y),239)
        #target_bitmap[x,y] = color
        #bitmap[x,y] == 0 is the default unused value.
        if x > 0 and x < 320 and y > 0 and y < 240 and target_bitmap[x,y] == 0:
            target_bitmap[x,y] = color
        theta+=step

def draw_circles():
    #print("Draw Circles called")
    wobbleP0x = random.randint(-MAX_WOBBLE,MAX_WOBBLE)
    wobbleP0y = random.randint(-MAX_WOBBLE,MAX_WOBBLE)
    wobbleP1x = random.randint(-MAX_WOBBLE,MAX_WOBBLE)
    wobbleP1y = random.randint(-MAX_WOBBLE,MAX_WOBBLE)

    global P0x
    global P0y
    global P1x
    global P1y

    #dont walk off the edges of the screen
    if P0x + wobbleP0x >= 320 or P0x + wobbleP0x < 0:
        P0x-=wobbleP0x
    else:
        P0x+=wobbleP0x
    if P0y + wobbleP0y >= 240 or P0y + wobbleP0y < 0:
        P0y-=wobbleP0y
    else:
        P0y+=wobbleP0y

    if P1x + wobbleP1x >= 320 or P1x + wobbleP1x < 0:
        P1x-=wobbleP1x
    else:
        P1x+=wobbleP1x
    if P1y + wobbleP1y >= 240 or P1y + wobbleP1y < 0:
        P1y-=wobbleP1y
    else:
        P1y+=wobbleP1y

    P0Circiles = displayio.Bitmap(board.DISPLAY.width, board.DISPLAY.height, 3)
    P0Pallete = displayio.Palette(3)
    P0Pallete[2] = COLOR_TWO
    P0Pallete[1] = COLOR_ONE
    P0Pallete.make_transparent(0)
    P0TileGrid = displayio.TileGrid(P0Circiles, pixel_shader=P0Pallete)

    collect()
    #draw the first circles
    i = 1
    while i < NUM_RINGS:
        draw_circle(P0x, P0y,i*RING_SPACING, P0Circiles, 1)
        i+=1
        collect()

    #draw the second draw_circles
    i = 1
    while i < NUM_RINGS:
        #print("Drawing a Green Circle")
        draw_circle(P1x, P1y,i*RING_SPACING, P0Circiles, 2)
        i+=1
        collect()

    if len(basegroup) > 1:
        basegroup.pop(len(basegroup)-1)
    basegroup.append(P0TileGrid)
    board.DISPLAY.wait_for_frame()

draw_circles()
print("Finished drawing first circles")

while True:
    time.sleep(SLEEP_SECONDS)
    #collect(verbose=1)
    collect()
    draw_circles()
