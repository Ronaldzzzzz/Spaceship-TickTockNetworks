import curses
import random
import argparse
import time
import threading
import sys

# Initialize Variables and Strings

# Dropping Speed
SPEED = [1, 0.8 ,0.6 ,0.4, 0.2, 0.1, 0.07, 0.05, 0.03, 0.01]    

def init():
    global obstacles_list, ship_location, status_bar_str, args, difficulty, end_flag, score

    args = set_argument()

    obstacles_list = []

    # True If Game Over
    end_flag = False

    score = 0    
    ship_location = args.width // 2
    difficulty = SPEED[args.difficulty-1]
    status_bar_str = "Press 'q' to exit | Size: " + str(args.width) + "x" + str(args.height) + " | Difficulty: " + str(args.difficulty) + " | Score: "

# Command-Line Argument Parse
def set_argument():
    parser = argparse.ArgumentParser(
        description="Playing Spaceship Dodging Game in Terminal!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    parser.add_argument("--height", action='store', default=24, type=height_type, help="Set the height of the screen [height > 7]")
    parser.add_argument("--width", action='store', default=80, type=width_type, help="Set the width of the screen")
    parser.add_argument("--difficulty", action='store', default=1, type=difficulty_type, help="Set the difficulty[1-10] of the game, increase the speed of dropping obstacles")

    return parser.parse_args()

# Customize Type Function
def height_type(x):
    x = int(x)
    if x < 7:
        raise argparse.ArgumentTypeError("Height must greater than 7 [height > 7]")
    return x
def width_type(x):
    x = int(x)
    if x < 65:
        raise argparse.ArgumentTypeError("width must greater than 65 [width > 65]")
    return x
def difficulty_type(x):
    x = int(x)
    if x < 1 or x > 10:
        raise argparse.ArgumentTypeError("Difficulty must between [1-10]")
    return x

# Render Information When Game End
def render_end_game(stdscr, rows, cols):
    global score, end_flag

    # Hit Warning
    stdscr.attron(curses.color_pair(2))
    stdscr.addch(rows-2, ship_location, "*")
    stdscr.addch(rows-3, ship_location, "X")
    stdscr.attroff(curses.color_pair(2))

    # Middle Information Window
    str_1 = " GAME OVER! "
    str_2 = " Your Score: " + str(score) + " "
    str_3 = " Press 'q' to exit, 'r' to restart "
    _y = int((rows // 2) - 2)
    _x_1 = int((cols // 2) - (len(str_1) // 2) - len(str_1) % 2)
    _x_2 = int((cols // 2) - (len(str_2) // 2) - len(str_2) % 2)
    _x_3 = int((cols // 2) - (len(str_3) // 2) - len(str_3) % 2)

    for i in range(-1, 4):
        for j in range( (_x_3-2), (_x_3-2) + len(str_3) + 4):
            stdscr.addch(_y + i, j , "/")

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(_y    , _x_1  , str_1)
    stdscr.addstr(_y + 1, _x_2  , str_2)
    stdscr.addstr(_y + 2, _x_3  , str_3)
    stdscr.attroff(curses.color_pair(1))
    
    stdscr.refresh()

    # Key Event
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            curses.endwin()
            sys.exit()
        elif key == ord('r'):
            init()
            return

# Render Status Bar on the Bottom
def render_status_bar(stdscr, rows, cols):
    global status_bar_str, score

    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(rows-1, 0, status_bar_str + str(score))
    stdscr.addstr(rows-1, len(status_bar_str + str(score)), " " * (cols - len(status_bar_str + str(score)) - 1))
    stdscr.attroff(curses.color_pair(3))

def rendering(stdscr):
    global obstacles_list, ship_location, end_flag
    rows, cols = stdscr.getmaxyx()

    if end_flag:
        render_end_game(stdscr, rows, cols)
    else:
        stdscr.erase()	

        # Render Scene
        index = 0
        for i in reversed(obstacles_list):
            for j in i:
                stdscr.addch(index, j, "-")
            index += 1
        stdscr.addch(rows - 2, ship_location, "*")

        render_status_bar(stdscr, rows, cols)

        stdscr.refresh()

# Thread Target Function
def update_obstacles():
    global obstacles_list, ship_location, end_flag, score, args, difficulty
    
    while True:
        # Generate Obstacle
        obstacles = random.sample(range(0, args.width), 5)

        if len(obstacles_list) >= args.height-2:
            target = obstacles_list[0]
            obstacles_list.pop(0)

            score += args.difficulty
            if ship_location in target:
                end_flag = True

        obstacles_list.append(obstacles)

        # Dropping Speed
        time.sleep(difficulty)

def run(stdscr):
    global ship_location, args

    # Scene Initialize & Setting
    stdscr = curses.initscr()
    stdscr.resize(args.height, args.width)
    stdscr.nodelay(True)
    curses.curs_set(0)
    curses.noecho()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    th_update.start()

    while True:
        # Render Starting
        rendering(stdscr)

        # FPS
        time.sleep(0.001)

        # Key event
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT:
            if(ship_location > 0):
                ship_location -= 1
        elif key == curses.KEY_RIGHT:
            if(ship_location < args.width-1):
                ship_location += 1
        else:
            pass

    curses.endwin()
    

if __name__ == '__main__':
    init()

    # Obstacle dropping thread
    th_update = threading.Thread(target=update_obstacles, daemon=True)

    curses.wrapper(run)

