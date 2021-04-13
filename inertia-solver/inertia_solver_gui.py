#!/usr/bin/python3.7

import subprocess
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

GAME='10x8:wwmsswbgwmmbbwbbwsbmbmwwmmsgbwbbmsgwwwmgwwssSggwgbggmsgbbbggmssmbgswsmggsmgssmsm'
MOVE_SPEED=1
WAIT_BEFORE_EXIT_DURATION=5

def main():
    moves = subprocess.run(['./inertia_solver', GAME.split(':')[0], GAME.split(':')[1]], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')
    moves = list(filter(lambda x: x.strip() != '', moves))
    keys = []
    for move in moves:
        move = move.strip().upper()
        if move == 'NORTH':
            keys.append(Keys.ARROW_UP)
        elif move == 'SOUTH':
            keys.append(Keys.ARROW_DOWN)
        elif move == 'EAST':
            keys.append(Keys.ARROW_RIGHT)
        elif move == 'WEST':
            keys.append(Keys.ARROW_LEFT)
        elif move == 'NORTH_EAST':
            keys.append(Keys.PAGE_UP)
        elif move == 'NORTH_WEST':
            keys.append(Keys.HOME)
        elif move == 'SOUTH_EAST':
            keys.append(Keys.PAGE_DOWN)
        elif move == 'SOUTH_WEST':
            keys.append(Keys.END)

    driver = webdriver.Chrome()
    driver.get('https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html#' + GAME)
    
    puzzle = driver.find_element_by_id('puzzlecanvas')
    for key in keys:
        puzzle.send_keys(key)
        time.sleep(MOVE_SPEED)

    time.sleep(WAIT_BEFORE_EXIT_DURATION)
    driver.close()

if __name__ == "__main__":
    main()
