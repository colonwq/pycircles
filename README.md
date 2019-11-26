**Description**

So, I tried to make a live moire display of circles.

The code is very basic

- Sets the background to a black bitmap
- Creates to display groups to contain circles
- Generate a random X,Y for each ring center
- Creates twp sets of 30 rings (NUM_RINGS)
- Displays the two ring groups
- Sleeps for 5 seconds before deleting the ring groups and starting over.

**The Good**

The overlapping pattern is very nice

**The Bad**
- This consumes a lot of memory. I do not know how many more circles can be added
- Drawing a single frame of the display is about 20 seconds. 20 seconds is too long for a reasonable live display.

**Options**
- The memory pressure could be reduced if each circle group could be one bitmap.
- I don't know of any options for speeding the display updates. 
