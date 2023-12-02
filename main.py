import pygame
import sys
import copy
import random as r
from tile import Tile, Tile_Oper
from constants import *

pygame.init()

used_idx = []

##############################################################
### This function will return the indices of all used tiles ###
##############################################################
def return_used_tiles(tiles):
    emp = []
    for i, row in enumerate(tiles):
        for j, (_, value) in enumerate(row):
            if value != "":
                idx = i * TILE_PER_ROW + j
                emp.append(idx)

    return emp


##########################################################################
### This function will generate the tils and returns the list of tiles ###
##########################################################################
def generate_tiles():
    tiles = []
    for j in range(TILE_PER_ROW):
        row = []
        for i in range(TILE_PER_ROW):
            x = TILE_GAP * (i + 1) + i * TILE_SIZE
            y = TILE_GAP * (j + 1) + j * TILE_SIZE

            tile = Tile(x, y, TILE_SIZE, TILE_BG_COLOR, "")

            row.append([tile, ""])
        tiles.append(row)

    return tiles


##########################################################
### This function will add a tile to a random location ###
##########################################################
def add_tile(tiles: list[list], idx: int = None, value: str = None) -> list[list]:
    used_idx = return_used_tiles(tiles)
    if len(used_idx) == TILE_PER_ROW ** 2: return tiles

    if idx is None:
        idxs = r.sample(range(0, TILE_PER_ROW ** 2), 16)
        for i in used_idx:
            idxs.pop(idxs.index(i))

        idx = r.choice(idxs)
    
    tiles[idx//TILE_PER_ROW][idx%TILE_PER_ROW][1] = "2" if value is None else value
    
    return tiles


###################################################################
### This function will move all the tiles to a desired location ###
###################################################################
def move_tiles(tiles: list[list], key: str) -> list[list]:
    r = Tile_Oper()
    if key in {"left", "right"}:
        for i, row in enumerate(tiles):
            tiles[i] = r.move_tiles(row, key)
            tiles[i] = r.sum_tiles(row, key)
    elif key in {"up", "down"}:
        col = []
        for i in range(len(tiles[0])):
            col = []
            for row in tiles:
                col.append(row[i])
            ret = r.move_tiles(col, key)
            sum_ret = r.sum_tiles(ret, key)

            for j in range(len(tiles)):
                tiles[j][i] = sum_ret[j]


    return tiles


#####################
### Main function ###
#####################
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    tiles = generate_tiles()
    prev_tiles = copy.deepcopy(tiles)
    tiles = add_tile(tiles)
    # print(tiles)

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    prev_tiles = copy.deepcopy(tiles)
                    tiles = move_tiles(tiles, "left")
                    add_tile(tiles)
                elif event.key == pygame.K_RIGHT:
                    prev_tiles = copy.deepcopy(tiles)
                    tiles = move_tiles(tiles, "right")
                    add_tile(tiles)
                elif event.key == pygame.K_UP:
                    prev_tiles = copy.deepcopy(tiles)
                    tiles = move_tiles(tiles, "up")
                    add_tile(tiles)
                elif event.key == pygame.K_DOWN:
                    prev_tiles = copy.deepcopy(tiles)
                    tiles = move_tiles(tiles, "down")
                    add_tile(tiles)
                elif event.key == pygame.K_BACKSPACE:
                    tiles = copy.deepcopy(prev_tiles)

        screen.fill(BG_COLOR)
        for row in tiles:
            for tile_data in row:
                tile_data[0].draw(screen, tile_data[1])

        pygame.display.flip()


if __name__ == '__main__':
    main()
    sys.exit()
