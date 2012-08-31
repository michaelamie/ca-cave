#!/usr/bin/env python
import curses, random, time


def drawMap(screen, theMap, rows, cols):
  screen.clear()
  for row in rows:
    for col in cols:
      if theMap[row][col] == True:
        screen.addch(row, col, '#')

def countNeighbors(theMap, row, col):
  count = 0
  for y in [row-1, row, row+1]:
    for x in [col-1, col, col+1]:
      if theMap[y][x]:
        count += 1
  return count

def addBorders(theMap, rows, cols):
  for row in rows:
    for col in [0, len(cols)-1]:
      theMap[row][col] = True
  for col in cols:
    for row in [0, len(rows)-1]:
      theMap[row][col] = True


if __name__ == '__main__':
  # Set up curses
  try:
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    # Values
    rows = range(23)
    cols = range(80)
    delay = .1

    # Populate and randomize map
    caveMap = [[random.randint(1, 100) < 40 for col in cols]
           for row in rows]
    addBorders(caveMap, rows, cols)

    # Draw map before iterations
    drawMap(screen, caveMap, rows, cols)
    screen.addstr(len(rows), 0, "Initial state")
    screen.refresh()
    time.sleep(delay)

    # Iterate cellular automata algorithm
    iteration = 0
    while True:
      iteration += 1
      changed = False

      # Initialize next map
      nextMap = [[False for col in cols] for row in rows]
      addBorders(nextMap, rows, cols)

      # Count the neighbors of each cell and populate next map
      for row in rows[1:len(rows)-1]:
        for col in cols[1:len(cols)-1]:
          count = countNeighbors(caveMap, row, col)
          # Modify the current cell
          if caveMap[row][col] == True and count >= 4:
            nextMap[row][col] = True
          if caveMap[row][col] == False and count >= 5:
            nextMap[row][col] = True
            changed = True

      # Update map
      caveMap = nextMap

      # Draw map for each iteration
      drawMap(screen, caveMap, rows, cols)
      screen.addstr(len(rows), 0, "CA iteration: %d" % iteration)
      screen.refresh()
      time.sleep(delay)

      # Break out of the loop if we've reached equilibrium
      if not changed:
          break

    screen.getch()

  # Restore terminal to regular state
  finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
