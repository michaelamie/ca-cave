#!/usr/bin/env python
import curses, random, time


def drawMap(screen, map, rows, cols):
  screen.clear()
  for row in rows:
    for col in cols:
      if map[row][col] == True:
        screen.addch(row, col, '#')

def countNeighbors(map, row, col):
  count = 0
  for y in [row-1, row, row+1]:
    for x in [col-1, col, col+1]:
      if map[y][x]:
        count += 1
  return count

################################################################################

# Set up curses
try:
  screen = curses.initscr()
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)

  # Values
  rows = range(23)
  cols = range(80)

  # Populate and randomize map
  map = [[random.randint(1, 100) < 36 for col in cols]
         for row in rows]

  # Populate borders with walls
  for row in rows:
    for col in [0, len(cols)-1]:
      map[row][col] = True
  for col in cols:
    for row in [0, len(rows)-1]:
      map[row][col] = True

  # Draw map before iterations
  drawMap(screen, map, rows, cols)
  screen.addstr(len(rows), 0, "Initial state")
  screen.refresh()
  time.sleep(.1)

  # Iterate cellular automata algorithm
  iteration = 0
  while True:
    iteration += 1
    changed = False
    for row in rows[1:len(rows)-1]:
      for col in cols[1:len(cols)-1]:
        count = countNeighbors(map, row, col)
        # Modify the current cell
        if map[row][col] == False and count >= 5:
          map[row][col] = True
          changed = True
        if map[row][col] == True and count <= 2:
          map[row][col] = False
          changed = True

    # Draw map for each iteration
    drawMap(screen, map, rows, cols)
    screen.addstr(len(rows), 0, "CA iteration: %d" % iteration)
    screen.refresh()
    time.sleep(.1)

    # Break out of the loop if we've reached equilibrium
    if not changed:
        break

  screen.getch()

# Restore terminal to regular state
finally:
  curses.echo()
  curses.nocbreak()
  curses.endwin()
