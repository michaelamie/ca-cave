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
  # Left column
  if row-1 >= 0 and col-1 >= 0 and map[row-1][col-1] == True:
    count += 1
  if col-1 >= 0 and map[row][col-1] == True:
    count += 1
  if row+1 < len(ROWS) and col-1 >= 0 and map[row+1][col-1] == True:
    count += 1
  # Center column
  if row-1 >= 0 and map[row-1][col] == True:
    count += 1
  if row+1 < len(ROWS) and map[row+1][col] == True:
    count += 1
  # Right column
  if row-1 >= 0 and col+1 < len(COLS) and map[row-1][col+1] == True:
    count += 1
  if col+1 < len(COLS) and map[row][col+1] == True:
    count += 1
  if row+1 < len(ROWS) and col+1 < len(COLS) and map[row+1][col+1] == True:
    count += 1
  return count


try:
  screen = curses.initscr()
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)

################################################################################

  # Values
  ROWS = range(23)
  COLS = range(80)

  # Populate and randomize map
  map = [[random.randint(1, 100) < 36 for c in COLS] for r in ROWS]

  # Fill in edges
  for row in ROWS:
    map[row][0] = True
    map[row][1] = True
    map[row][len(COLS)-1] = True
    map[row][len(COLS)-2] = True
  for col in COLS:
    map[0][col] = True
    map[1][col] = True
    map[len(ROWS)-1][col] = True
    map[len(ROWS)-2][col] = True

  # Draw map before iterations
  drawMap(screen, map, ROWS, COLS)
  screen.addstr(len(ROWS), 0, "Initial state")
  screen.refresh()
  time.sleep(.1)

  # Iterate cellular automata algorithm
  iteration = 0
  while True:
    iteration += 1
    changed = False
    for row in ROWS:
      for col in COLS:
        count = countNeighbors(map, row, col)
        # Modify the current cell
        if map[row][col] == False and count >= 5:
          map[row][col] = True
          changed = True
        if map[row][col] == True and count <= 2:
          map[row][col] = False
          changed = True
  
    # Draw map for each iteration
    drawMap(screen, map, ROWS, COLS)
    screen.addstr(len(ROWS), 0, "CA iteration: %d" % iteration)
    screen.refresh()
    time.sleep(.1)

    # Break out of the loop if we've reached equilibrium
    if not changed:
        break

  screen.getch()

################################################################################

finally:
  curses.echo()
  curses.nocbreak()
  curses.endwin()
