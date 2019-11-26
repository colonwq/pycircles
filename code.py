import os
import time
import gc
import board
import busio
from digitalio import DigitalInOut
import neopixel
import displayio
import random
from adafruit_display_shapes.circle import Circle

NUM_RINGS = 30

def collect():
    #print("Amount of free memory: ", gc.mem_free() )
    gc.collect()
    #print("Amount of free ememory (after collect)", gc.mem_free())

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

def draw_circles():
    P0x = random.randint(60,260)
    P0y = random.randint(60,180)
    P1x = random.randint(60,260)
    P1y = random.randint(60,180)
    P0Circiles = displayio.Group(max_size=NUM_RINGS)
    P1Circiles = displayio.Group(max_size=NUM_RINGS)
    collect()
    i = 0
    while i < NUM_RINGS:
        P0Circiles.append(Circle(P0x, P0y,i*3, outline=0xFF0000))
        i+=1
        collect()

    i = 0
    while i < NUM_RINGS:
        P1Circiles.append(Circle(P1x, P1y,i*3, outline=0x00FF00))
        i+=1
        collect()

    basegroup.append(P0Circiles)
    basegroup.append(P1Circiles)
    board.DISPLAY.wait_for_frame()


draw_circles()
print("Length of the basegroup: %d" %(len(basegroup)))
print("Finished!")

while True:
    time.sleep(5)
    basegroup.pop(len(basegroup)-1)
    print("length of the basegroup: %d" %(len(basegroup)))
    basegroup.pop(len(basegroup)-1)
    print("length of the basegroup: %d" %(len(basegroup)))
    collect()
    draw_circles()
