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
NUM_RINGS = 30
RING_SPACING = 5
COLOR_ONE = 0xFF0000
COLOR_TWO = 0x00FF00
SMOOTHNESS = 5
SLEEP_SECONDS = .1

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
        pixel_shader=displayio.ColorConverter(),
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

set_background_color(0x000000)

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
    P0x = random.randint(60,260)
    P0y = random.randint(60,180)
    P1x = random.randint(60,260)
    P1y = random.randint(60,180)

    P0Circiles = displayio.Bitmap(board.DISPLAY.width, board.DISPLAY.height, 3)
    P0Pallete = displayio.Palette(3)
    P0Pallete[2] = COLOR_TWO
    P0Pallete[1] = COLOR_ONE
    #P0Pallete[0] = 0x000000
    P0Pallete.make_transparent(0)
    P0TileGrid = displayio.TileGrid(P0Circiles, pixel_shader=P0Pallete)

    collect()
    #draw the red circles
    i = 1
    while i < NUM_RINGS:
        #print("Drawing a Red Circle")
        draw_circle(P0x, P0y,i*RING_SPACING, P0Circiles, 1)
        i+=1
        collect()

    #draw the green draw_circles
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
    collect(verbose=1)
    draw_circles()
