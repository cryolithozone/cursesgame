import curses
import curses.ascii
import random
import string

# all the keys used 
class Keys:
    LEFT = curses.KEY_LEFT
    RIGHT = curses.KEY_RIGHT
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN
    ESC = curses.ascii.ESC
    W = ord("w")
    A = ord("a")
    S = ord("s")
    D = ord("d")
    Q = ord("q")
    H = ord("h")
    C = ord("c")
    B = ord("b")

# available movement keys
MOV_KEYS = {Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT, 
            Keys.W, Keys.A, Keys.S, Keys.D}

# define the little guy on the screen
HEROES = ["%", "#", "@", "&", "0", "D"]
hero = 0

# current bg character
bgchar = " "

# all possible bg characters
BG_CHARS = " "*100 + ":\"\'-*,.`~X"

# all ascii symbols
ASCII = string.ascii_letters + string.digits

# the actual background
BG = []

def draw_bg(screen, new = False):
    h, w = screen.getmaxyx()
    global BG
    if new:
        BG = ["".join(random.choice(BG_CHARS) for i in range(w - 1)) for j in range(h - 1)]
    
    
    for j, row in enumerate(BG):
        for i, char in enumerate(row):
            if char == "X":
                draw_char(screen, i, j, char, curses.color_pair(2))
            else:
                draw_char(screen, i, j, char, curses.color_pair(1))


def draw_char(screen, x, y, char, attr):
    h, w = screen.getmaxyx()

    # checking if we're in the bottom right corner
    # (either a really weird documented curses bug or some weird feature LOL)
    # then drawing the character accordingly
    if (x, y) == (w - 1, h - 1):
        screen.insch(y, x, char, attr)
    else:
        screen.addch(y, x, char, attr)

def move(screen, x, y, key):
    h, w = screen.getmaxyx()
    global bgchar
    # replace our guy with whatever character might have been under them
    # checking what kind of char it is so we can redraw appropriately
    if bgchar == "X":
        draw_char(screen, x, y, bgchar, curses.color_pair(2))
    elif bgchar in ASCII:
        draw_char(screen, x, y, bgchar, curses.color_pair(4))
    else:
        draw_char(screen, x, y, bgchar, curses.color_pair(1))
    
    # calculate new coordinates based on the pressed key
    match key:
        case Keys.DOWN | Keys.S:
            if y < h - 1:
                y = y + 1
        case Keys.UP | Keys.W:
            if y > 0:
                y = y - 1
        case Keys.LEFT | Keys.A:
            if x > 0:
                x = x - 1
        case Keys.RIGHT | Keys.D:
            if x < w - 1:
                x = x + 1
    
    # get new bg character
    bgchar = chr(screen.inch(y, x) & 0b11111111)
    # draw the little guy in the new coordinates
    draw_char(screen, x, y, HEROES[hero], curses.color_pair(3))

    return x, y

def change_hero(screen, x, y):
    global hero
    hero = (hero + 1) % len(HEROES)

    # drawing the new appearance of the little guy
    draw_char(screen, x, y, HEROES[hero], curses.color_pair(3))

def welcome_screen(screen):
    h, w = screen.getmaxyx()
    screen.addstr(h // 2, w // 2, "hi", curses.color_pair(4))
    screen.addstr(h // 2 + 1, w // 4, "world's smallest game ...... avoid X's they will kill you", curses.color_pair(4))
    screen.addstr(h // 2 + 2, w // 4, "WASD or arrow keys to move", curses.color_pair(4))
    screen.addstr(h // 2 + 3, w // 4, "Q to cycle through appearances (available: % # @ & 0 D)", curses.color_pair(4))
    screen.addstr(h // 2 + 4, w // 4, "H to show this screen again", curses.color_pair(4))
    screen.addstr(h // 2 + 5, w // 4, "B to draw a new background", curses.color_pair(4))
    screen.addstr(h // 2 + 6, w // 4, "ESC to exit the game", curses.color_pair(4))
    screen.addstr(h // 2 + 7, w // 4, "C to erase this text", curses.color_pair(4))



def end_screen(screen):
    # blocking program running until it gets input
    screen.timeout(-1)

    screen.clear()
    h, w = screen.getmaxyx()
    screen.addstr(h // 2, w // 4, "End the game?", curses.color_pair(4))
    screen.addstr(h // 2 + 1, w // 4, "press ESC again to confirm", curses.color_pair(4))
    screen.addstr(h // 2 + 2, w // 4, "press anything else to cancel", curses.color_pair(4))
    
    key = screen.getch()
    if key == Keys.ESC:
        return True
    else:
        return False

def lose_screen(screen):
    # blocking program running until it gets input
    screen.timeout(-1)

    screen.clear()
    h, w = screen.getmaxyx()
    screen.addstr(h // 2, w // 4, "GAME OVER!", curses.color_pair(4))
    screen.addstr(h // 2 + 1, w // 4, "press any key to close the game", curses.color_pair(4))

    screen.getch()


def main(win):
    
    # make it so that the program still runs even with no input
    win.timeout(0)

    # use colors!!!!!!!!!!
    curses.start_color()
    curses.use_default_colors()

    # initialize color pairs
    # 1 - bg characters
    # 2 - X's (danger)
    # 3 - our guy
    # 4 - text
    curses.init_pair(1, -1, -1)
    curses.init_pair(2, 160, 16)
    curses.init_pair(3, 51, -1)
    curses.init_pair(4, -1, 16)

    draw_bg(win, new = True)
    welcome_screen(win)

    x = 0
    y = 0

    draw_char(win, x, y, HEROES[hero], curses.color_pair(3))

    while True:
        
        # makes the cursor invisible
        curses.curs_set(0)

        key = win.getch()

        if key != -1:
            
            #win.addstr(20, 20, f"{key, x, y}")

            if key in MOV_KEYS:
                x, y = move(win, x, y, key)

            elif key == Keys.Q:
                change_hero(win, x, y)
            
            elif key == Keys.H:
                welcome_screen(win)
            
            elif key == Keys.C:
                win.clear()
                draw_bg(win)
                draw_char(win, x, y, HEROES[hero], curses.color_pair(3))
            
            elif key == Keys.B:
                win.clear()
                draw_bg(win, new = True)
                draw_char(win, x, y, HEROES[hero], curses.color_pair(3))

            elif key == Keys.ESC:
                exit = end_screen(win)
                if exit:
                    return 0
                else:
                    # getting the program back to normal
                    win.timeout(0)
                    win.clear()
                    draw_bg(win)
        
        # checking for the losing condition (stepping on an X)
        if bgchar == "X":
            lose_screen(win)
            return 1

if __name__ == "__main__":
    curses.wrapper(main)