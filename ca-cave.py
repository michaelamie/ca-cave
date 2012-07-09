#!/usr/bin/env python

import curses, random, time

def drawMap(map, rows, cols):
  for row in rows:
    for col in cols:
      if map[row][col] == False:
        screen.addch(row, col, ' ')
      else:
        screen.addch(row, col, '#')

try:
  screen = curses.initscr()
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)

################################################################################

  # Values
  ROWS = range(23)
  COLS = range(80)

  # Populate map
  map = []
  for row in ROWS:
    new_row = []
    for col in COLS:
      new_row.append(False)
    map.append(new_row)

  # 50/50 chance that each tile is populated by a wall
  for row in ROWS:
    for col in COLS:
      if random.randint(1, 100) < 40:
        map[row][col] = True

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
  drawMap(map, ROWS, COLS)
  screen.addstr(len(ROWS), 0, "Initial state")
  screen.refresh()
  time.sleep(.5)

  # Iterate cellular automata algorithm
  for iteration in range(3):
    for row in ROWS:
      for col in COLS:
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
        # Modify the current cell
        if map[row][col] == False and count >= 5:
          map[row][col] = True
        if map[row][col] == True and count <= 2:
          map[row][col] = False

    # Draw map for each iteration
    drawMap(map, ROWS, COLS)
    screen.addstr(len(ROWS), 0, "CA iteration: %d" % iteration)
    screen.refresh()
    time.sleep(.5)
  screen.getch()

################################################################################

finally:
  curses.echo()
  curses.nocbreak()
  curses.endwin()
