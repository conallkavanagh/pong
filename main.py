#!/usr/bin/env python3

import curses
import keyboard
from random import choice
from time import sleep


class Player(object):
    def __init__(self, x):
        self.length = 5
        self.x = x
        self.y = curses.LINES // 2
        self.score = 0

    def update_pos(self, y):
        # updates pos and makes sure player is within screen
        if 0 <= self.y + y <= curses.LINES - self.length:
            self.y += y

    def draw(self, stdscr):
        for i in range(self.length): 
            stdscr.addch(self.y+i, self.x, '#')

    def movement(self, up, down):
        # check arrow keys pressed and update coords
        if keyboard.is_pressed(down):
            self.update_pos(1)
        elif keyboard.is_pressed(up):
            self.update_pos(-1)


class Ball(object):
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.vel_x = 1
        self.vel_y = 0

    def update_ball(self):
        # check within screen and if at edge change velocity
        if not 0 <= self.y + self.vel_y <= curses.LINES - 1:
            self.vel_y = -self.vel_y
        if not 0 <= self.x + self.vel_x <= curses.COLS - 1:
            self.vel_x = -self.vel_x

        self.x += self.vel_x
        self.y += self.vel_y

    def check_collisions(self, player):
        third_player = player.length // 3
        #if (self.x - 1 == player.x or self.x + 1 == player.x) and player.y <= self.y < player.y + player.length:
        #    self.vel_x = -self.vel_x

        # check if we are colliding
        if self.x - 1 == player.x or self.x + 1 == player.x and player.y <= self.y < player.y + player.length:
            self.vel_x = -self.vel_x
            if self.y <= player.y + third_player:
                # first third go up
                self.vel_y = -1
            elif player.y + third_player < self.y <= player.y + third_player * 2:
                # second third go straight
                self.vel_y = 0
            else:
                # third third go down
                self.vel_y = 1

    def draw(self, stdscr):
        stdscr.addch(self.y, self.x, '0')

    def respawn(self):
        self.y = curses.LINES // 2
        self.x = curses.COLS // 2
        self.vel_x = choice([1,-1])
        self.vel_y = choice([1,-1])


def main(stdscr):
    curses.curs_set(0) # make cursor invisible
    # Clear screen
    stdscr.clear()

    player1 = Player(3)
    player2 = Player(curses.COLS - 4)
    game_ball = Ball(curses.LINES // 2, curses.COLS // 2)

    # check arrow keys pressed and update coords
    #p1 = threading.Thread(target=p1_movement, args=(stdscr,player1), daemon=True)
    #p2 = threading.Thread(target=p2_movement, args=(stdscr,player2), daemon=True)
    #p1.start()
    #p2.start()

    while not keyboard.is_pressed('esc'):
        # init
        stdscr.erase()
        stdscr.addstr(0, curses.COLS // 2 - 3, 'SCORE')
        stdscr.addstr(1, curses.COLS // 2 - 6, f'P1: {player1.score} P2: {player2.score}')

        player1.movement('w','s')
        player2.movement(keyboard.KEY_UP, keyboard.KEY_DOWN)
        player1.draw(stdscr)
        player2.draw(stdscr)

        game_ball.update_ball()
        game_ball.check_collisions(player1)
        game_ball.check_collisions(player2)
        game_ball.draw(stdscr)

        if game_ball.x > player2.x:
            player1.score += 1
            game_ball.respawn()
        elif game_ball.x < player1.x:
            player2.score += 1
            game_ball.respawn()

        sleep(0.05)

        stdscr.refresh()

    stdscr.clear()
    if player1.score > player2.score:
        stdscr.addstr(curses.LINES // 2, (curses.COLS // 2) - 6, 'Player 1 wins!')
    elif player1.score < player2.score:
        stdscr.addstr(curses.LINES // 2, (curses.COLS // 2) - 6, 'Player 2 wins!')
    else:
        stdscr.addstr(curses.LINES // 2, (curses.COLS // 2) - 2, 'Draw')
    stdscr.refresh()
    
    sleep(2)

curses.wrapper(main)
