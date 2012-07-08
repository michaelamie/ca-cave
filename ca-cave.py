#!/usr/bin/env python

import curses, random, time

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
      new_row.append(' ')
    map.append(new_row)

  # 50/50 chance that each tile is populated by a '#' symbol
  for row in ROWS:
    for col in COLS:
      if random.randint(1, 100) < 40:
        map[row][col] = '#'

  # Fill in edges
  for row in ROWS:
    map[row][0] = '#'
    map[row][1] = '#'
    map[row][len(COLS)-1] = '#'
    map[row][len(COLS)-2] = '#'
  for col in COLS:
    map[0][col] = '#'
    map[1][col] = '#'

  # Draw map before iterations
  for row in ROWS:
    for col in COLS:
      screen.addch(row, col, map[row][col])
  screen.addstr(len(ROWS), 0, "Initial state")
  screen.refresh()
  time.sleep(.5)

  # Iterate cellular automata algorithm
  for iteration in range(3):
    for row in ROWS:
      for col in COLS:
        count = 0
        # Left column
        if row-1 >= 0 and col-1 >= 0 and map[row-1][col-1] == '#':
          count += 1
        if col-1 >= 0 and map[row][col-1] == '#':
          count += 1
        if row+1 < len(ROWS) and col-1 >= 0 and map[row+1][col-1] == '#':
          count += 1
        # Center column
        if row-1 >= 0 and map[row-1][col] == '#':
          count += 1
        if row+1 < len(ROWS) and map[row+1][col] == '#':
          count += 1
        # Right column
        if row-1 >= 0 and col+1 < len(COLS) and map[row-1][col+1] == '#':
          count += 1
        if col+1 < len(COLS) and map[row][col+1] == '#':
          count += 1
        if row+1 < len(ROWS) and col+1 < len(COLS) and map[row+1][col+1] == '#':
          count += 1
        # Modify the current cell
        if map[row][col] == '#' and count >= 4:
          map[row][col] = '#'
        elif map[row][col] == ' ' and count >= 5:
          map[row][col] = '#'
        elif count <= 2:
          map[row][col] = ' '

    # Draw map for each iteration
    for row in ROWS:
      for col in COLS:
        screen.addch(row, col, map[row][col])
    screen.addstr(len(ROWS), 0, "CA iteration: %d" % iteration)
    screen.refresh()
    time.sleep(.5)
  screen.getch()

################################################################################

finally:
  curses.echo()
  curses.nocbreak()
  curses.endwin()
