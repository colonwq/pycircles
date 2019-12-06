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
NUM_RINGS = 60
RING_SPACING = 5
COLOR_ONE = 0xFF0000
COLOR_TWO = 0x00FF00
COLOR_BACKGROUND = 0x000000
SMOOTHNESS = 4
SLEEP_SECONDS = 5
MAX_WOBBLE = 5

#start the circles in the center-ish
P0x = 300
P0y = 200
P1x = 0
P1y = 0

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
    global P0Circles
    global P1Circles
    print("Draw circles called")
    #draw the first circles
    i = 1
    while i < NUM_RINGS:
        draw_circle(320, 240,i*RING_SPACING, P0Circles, 1)
        i+=1

    #draw the second draw_circles
    i = 1
    while i < NUM_RINGS:
        draw_circle(320, 240,i*RING_SPACING, P1Circles, 2)
        i+=1
    collect()

def make_palette():
    global P0Palette
    print("Make palette called")
    P0Palette = displayio.Palette(3)
    P0Palette[2] = COLOR_TWO
    P0Palette[1] = COLOR_ONE
    #P0Palette[0] = 0x888888
    P0Palette.make_transparent(0)

def make_bitmaps():
    global PxCircles
    global P0Circles
    global P1Circles
    print("Make bitmaps called")
    PxCircles = displayio.Bitmap(board.DISPLAY.width, board.DISPLAY.height, 3)
    P0Circles = displayio.Bitmap(board.DISPLAY.width*2, board.DISPLAY.height*2, 3)
    P1Circles = displayio.Bitmap(board.DISPLAY.width*2, board.DISPLAY.height*2, 3)

def place_circles():
    global P0Circles
    global P1Circles
    global P0Palette
    global P0TileGrid
    global P1TileGrid
    global P0x
    global P0y
    global P1x
    global P1y
    print("Place circles called")
    #P0TileGrid = displayio.TileGrid(P0Circles, pixel_shader=P0Palette, x=P0x, y=P0y)
    #P1TileGrid = displayio.TileGrid(P1Circles, pixel_shader=P0Palette, x=P1x, y=P1y)
    copy_area( src_bmp = P0Circles, dest_bmp=PxCircles, src_x = P0x, src_y = P0y )

    PxTileGrid = displayio.TileGrid(PxCircles, pixel_shader=P0Palette)
    basegroup.append(PxTileGrid)
    #basegroup.append(P0TileGrid)
    #basegroup.append(P1TileGrid)
    board.DISPLAY.wait_for_frame()

def fudge_tilegrids():
    global P0TileGrid
    global P1TileGrid
    global P0x
    global P0y
    global P1x
    global P1y
    print("Fudge tile grids called")
    wobbleP0x = random.randint(-MAX_WOBBLE,MAX_WOBBLE)
    wobbleP0y = random.randint(-MAX_WOBBLE,MAX_WOBBLE)
    wobbleP1x = random.randint(-MAX_WOBBLE,MAX_WOBBLE)
    wobbleP1y = random.randint(-MAX_WOBBLE,MAX_WOBBLE)

    P0x = P0TileGrid.x + wobbleP0x
    P0y = P0TileGrid.y + wobbleP0y
    P1x = P1TileGrid.x + wobbleP1x
    P1y = P1TileGrid.y + wobbleP1y
    print("Base group length: %d" % (len(basegroup)) )
    #basegroup.pop(len(basegroup)-1)
    #basegroup.pop(len(basegroup)-1)
    place_circles()

def copy_area( src_bmp: displayio.Bitmap, dest_bmp: displayio.Bitmap, src_x = 0, src_y = 0, dest_x = 0, dest_y = 0, width = 320, height = 240):
    global Pxcircles
    global P0Circles
    print("Copy area called")
    if src_bmp == None or dest_bmp == None:
        raise Exception("src_bmp and dest_bmp must be defined")
    if src_x + width > src_bmp.width:
        raise Exception("Source end width out of bounds of source image")
    if src_y + height > src_bmp.height:
        raise Exception("Source end height out of bounds of source image")
    if dest_x + width > dest_bmp.width:
        raise Exception("Destination end width out of bounds of destination image")
    if dest_y + height > dest_bmp.height:
        raise Exception("Destination end height out of bounds of destination image")

    print("Src bmp size: (%d,%d)" %( src_bmp.width, src_bmp.height))
    print("Dest bmp size: (%d,%d)" %( dest_bmp.width, dest_bmp.height))
    print("Copy area : (%d,%d)" % (width, height))
    for x in range(width):
        for y in range(height):
            #print("Copy location %d %d" %(x,y))
            #if dest_bmp[dest_x+x,dest_y+y] != 0:
            #    dest_bmp[dest_x+x,dest_y+y] = src_bmp[src_x+x,src_y+y]
            dest_bmp[dest_x+x,dest_y+y] = src_bmp[src_x+x,src_y+y]
    print("Copy area finished")



#three colors [transparent, color_one, color_two]
P0Palette = None
#bmp 320x240 3 color
PxCircles = None
#bmp 640x480 3 color
P0Circles = None
#bmp 640x480 3 color
P1Circles = None
PxTileGrid = None
P0TileGrid = None
P1TileGrid = None

#make the color palette
make_palette()
#make the 
make_bitmaps()
#add cirlces to P[01]Circles
draw_circles()
place_circles()

print("Finished drawing first circles")

while True:
    time.sleep(SLEEP_SECONDS)
    collect(verbose=1)
    #collect()
    #fudge_tilegrids()
