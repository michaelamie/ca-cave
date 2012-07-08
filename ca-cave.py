#!/usr/bin/env python

import curses, random, time

try:
  screen = curses.initscr()
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)

################################################################################

  # Values
  ROWS = range(24)
  COLS = range(60)

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
      if not (random.randint(1,2) % 2):
        map[row][col] = '#'

  # Draw map before iterations
  for row in ROWS:
    for col in COLS:
      screen.addch(row, col, map[row][col])
  screen.refresh()
  time.sleep(1)
  #screen.getch()

  # Iterate cellular automata algorithm
  for iteration in range(4):
    for row in ROWS:
      for col in COLS:
        count = 0

        if row-1 >= 0 and col-1 >= 0 and map[row-1][col-1] == '#':
          count += 1
        if col-1 >= 0 and map[row][col-1] == '#':
          count += 1
        if row+1 < len(ROWS) and col-1 >= 0 and map[row+1][col-1] == '#':
          count += 1

        if row-1 >= 0 and map[row-1][col] == '#':
          count += 1
        if map[row][col] == '#':
          count += 1
        if row+1 < len(ROWS) and map[row+1][col] == '#':
          count += 1

        if row-1 >= 0 and col+1 < len(ROWS) and map[row-1][col+1] == '#':
          count += 1
        if col+1 < len(ROWS) and map[row][col+1] == '#':
          count += 1
        if row+1 < len(ROWS) and col+1 < len(ROWS) and map[row+1][col+1] == '#':
          count += 1

        if count > 5:
          map[row][col] = '#'
        elif count <= 3:
          map[row][col] = ' '

    # Draw map for each iteration
    screen.clear()
    screen.refresh()
    for row in ROWS:
      for col in COLS:
        screen.addch(row, col, map[row][col])
    screen.refresh()
    time.sleep(1)

  screen.getch()

################################################################################

finally:
  curses.echo()
  curses.nocbreak()
  curses.endwin()
