**Description**

So, I tried to make a live moire display of circles.

The code is very basic

- Sets the background to a black bitmap
- Creates to display groups to contain circles
- Move X,Y for each ring center a random amount up to MAX_WOBBLE
- Creates twp sets of 30 rings (NUM_RINGS)
- Displays the two ring groups
- Sleeps for SLEEP_SECONDS seconds before deleting the ring groups and starting over.

**Update**
- Custom circle function is used instead of the adafruit_display_shapes
- All circles are pre-drawn into two BMPs which are 1.5 the size of the screen
- The top left corner is random on startup
- The circles BMPs are copied into the screen bmp and displayed
- Configuration parameters are added to the top of the code.py
  - NUM_RINGS: The number of rings to be drawn per group
  - RING_SPACING: How many pixels to increase the next ring from the previous
  - COLOR_ONE, COLOR_TWO: The RGB color of the rings
  - COLOR_BACKGROUND: The color of the background
  - SMOOTHNESS: A fudge factor for how many steps to go around the diameter of the circle
  - SLEEP_SECONDS: How many seconds to sleep between ring generations
  - MAX_WOBBLE: what is the +- max the cetners can move per iteration

**The Good**

- The overlapping pattern is very nice
- The BMPs use a lot of space. 1.5 is about the limit as the code uses 4
  BMP. (color_one, color_two, display, new display)
- Faster image display.
  - The image will complete a redraw in ~1 sec
- Timings
  - Startup: 12 seconds includes drawing circles in color_one and color_two bmp
  - Update: 7 to 9 seconds. This is the copying of displayed areas of color_one and
    color_two into the new display bmp

**The Bad**
- Not quite fast enough for a live display

**Options**
- Could make the color_one and color_two bmp a depth of 2 instead of 3 but this would 
  complicate the copy process. 
