#!/usr/bin/env python
import curses, random, time


def drawMap(screen, map, rows, cols):
  screen.clear()
  for row in rows:
    for col in cols:
      if map[row][col] == True:
        screen.addch(row, col, '#')

def countNeighbors(map, rows, cols, row, col):
  count = 0
  # Left column
  if row-1 >= 0 and col-1 >= 0 and map[row-1][col-1] == True:
    count += 1
  if col-1 >= 0 and map[row][col-1] == True:
    count += 1
  if row+1 < len(rows) and col-1 >= 0 and map[row+1][col-1] == True:
    count += 1
  # Center column
  if row-1 >= 0 and map[row-1][col] == True:
    count += 1
  if row+1 < len(rows) and map[row+1][col] == True:
    count += 1
  # Right column
  if row-1 >= 0 and col+1 < len(cols) and map[row-1][col+1] == True:
    count += 1
  if col+1 < len(cols) and map[row][col+1] == True:
    count += 1
  if row+1 < len(rows) and col+1 < len(cols) and map[row+1][col+1] == True:
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
  map = [[random.randint(1, 100) < 36 for col in cols] for row in rows]

  # Fill in edges
  for row in rows:
    map[row][0] = True
    map[row][1] = True
    map[row][len(cols)-1] = True
    map[row][len(cols)-2] = True
  for col in cols:
    map[0][col] = True
    map[1][col] = True
    map[len(rows)-1][col] = True
    map[len(rows)-2][col] = True

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
    for row in rows:
      for col in cols:
        count = countNeighbors(map, rows, cols, row, col)
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
