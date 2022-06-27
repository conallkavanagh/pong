#!/usr/bin/env python3

import curses
import keyboard
import threading
from time import sleep


class Player(object):
    def __init__(self, x):
        self.length = 3
        self.x = x
        self.y = curses.LINES // 2

    def update_pos(self, y):
        # updates pos and makes sure player is within screen
        if 0 <= self.y + y <= curses.LINES - self.length:
            self.y += y

    def draw(self, stdscr):
        for i in range(self.length): 
            stdscr.addch(self.y+i, self.x, '#')

class Ball(object):
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.vel_x = 1
        self.vel_y = 1

    def update_ball(self):
        # check within screen and if at edge change velocity
        if not 0 <= self.y + self.vel_y <= curses.LINES - 1:
            self.vel_y = -self.vel_y
        if not 0 <= self.x + self.vel_x <= curses.COLS - 1:
            self.vel_x = -self.vel_x

        self.x += self.vel_x
        self.y += self.vel_y

    def check_collisions(self, player):
        if (self.x - 1 == player.x or self.x + 1 == player.x) and player.y <= self.y < player.y + player.length:
            self.vel_x = -self.vel_x

    def draw(self, stdscr):
        stdscr.addch(self.y, self.x, '0')


def p1_movement(stdscr, player):
    #k = 0
    while True:
        # check arrow keys pressed and update coords
        if keyboard.is_pressed('s'):
            player.update_pos(1)
        elif keyboard.is_pressed('w'):
            player.update_pos(-1)
        sleep(0.05)
        #if k == 115: # s
        #    player.update_pos(1)
        #elif k == 119: # w
        #    player.update_pos(-1)
        #k = stdscr.getch()
        

def p2_movement(stdscr, player):
    #k = 0
    while True:
        # check arrow keys pressed and update coords
        if keyboard.is_pressed(keyboard.KEY_DOWN):
            player.update_pos(1)
        elif keyboard.is_pressed(keyboard.KEY_UP):
            player.update_pos(-1)
        sleep(0.05)
        #if k == curses.KEY_DOWN: # s
        #    player.update_pos(1)
        #elif k == curses.KEY_UP: # w
        #    player.update_pos(-1)
        #k = stdscr.getch()


def main(stdscr):
    curses.curs_set(0) # make cursor invisible
    # Clear screen
    stdscr.clear()

    player1 = Player(3)
    player2 = Player(curses.COLS - 4)
    game_ball = Ball(curses.LINES // 2, curses.COLS // 2)

    # check arrow keys pressed and update coords
    p1 = threading.Thread(target=p1_movement, args=(stdscr,player1), daemon=True)
    p2 = threading.Thread(target=p2_movement, args=(stdscr,player2), daemon=True)
    p1.start()
    p2.start()

    while True:
        # init
        stdscr.erase()
        player1.draw(stdscr)
        player2.draw(stdscr)
        game_ball.update_ball()
        game_ball.check_collisions(player1)
        game_ball.check_collisions(player2)
        game_ball.draw(stdscr)
        sleep(0.05)

        stdscr.refresh()

curses.wrapper(main)
