import pygame
from constants import *

class Tile:
    def __init__(self, x: int, y: int, size: int, color: tuple, value) -> None:
        self.pos = pygame.Vector2(x, y)
        self.size = size
        self.color = color
        self.font_size = 110

        self.value = value

    def draw(self, screen: pygame.Surface, value=None):
        value = str(self.value) if value is None else str(value)

        self.value = value

        if value and int(value) >= 8192:
            self.color = TILE_COLOR["8192"]
        else:
            self.color = TILE_COLOR[value]

        pos = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, pos, border_radius=4)

        if value:
            number_font = pygame.font.SysFont(None, self.font_size)
            
            while number_font.size(value)[0] >= self.size - 10:
                self.font_size -= 10
                number_font = pygame.font.SysFont(None, self.font_size)

            number = number_font.render(value, True, NUMBER_COLOR[0] if int(value) <= 4 else NUMBER_COLOR[1])


            num_x = (self.pos.x + (self.size / 2) - number.get_width() / 2)
            num_y = (self.pos.y + (self.size / 2) - number.get_height() / 2 + 5)
            
            screen.blit(number, (num_x, num_y))


class Tile_Oper:
    def move_tiles(self, row: list[list], dir: str):
        for i in range(len(row)-1):
            for j in range(len(row)-i-1):
                if dir == "left" and row[j+1][1] and row[j][1] == "":
                    row[j+1][0].pos.x, row[j][0].pos.x = row[j][0].pos.x, row[j+1][0].pos.x
                    row[j+1], row[j] = row[j], row[j+1]
                elif dir == "right" and row[j][1] and row[j+1][1] == "":
                    row[j+1][0].pos.x, row[j][0].pos.x = row[j][0].pos.x, row[j+1][0].pos.x
                    row[j+1], row[j] = row[j], row[j+1]
                elif dir == "up" and row[j+1][1] and row[j][1] == "":
                    row[j+1][0].pos.y, row[j][0].pos.y = row[j][0].pos.y, row[j+1][0].pos.y
                    row[j+1], row[j] = row[j], row[j+1]
                elif dir == "down" and row[j][1] and row[j+1][1] == "":
                    row[j+1][0].pos.y, row[j][0].pos.y = row[j][0].pos.y, row[j+1][0].pos.y
                    row[j+1], row[j] = row[j], row[j+1]

        return row

    def sum_tiles(self, row: list[list], dir: str):
        i = 0
        if dir == "left":
            while i < len(row) - 1:
                if row[i][1] and row[i+1][1] and row[i][1] == row[i+1][1]:
                    row[i][1] = str(int(row[i][1]) * 2)
                    row[i+1][1] = ""
                i += 1
        if dir == "right":
            while i < len(row) - 1:
                if row[i][1] and row[i+1][1] and row[i][1] == row[i+1][1]:
                    row[i+1][1] = str(int(row[i+1][1]) * 2)
                    row[i][1] = ""
                i += 1
        if dir == "up":
            while i < len(row) - 1:
                if row[i][1] and row[i+1][1] and row[i][1] == row[i+1][1]:
                    row[i][1] = str(int(row[i][1]) * 2)
                    row[i+1][1] = ""
                i += 1
        if dir == "down":
            while i < len(row) - 1:
                if row[i][1] and row[i+1][1] and row[i][1] == row[i+1][1]:
                    row[i+1][1] = str(int(row[i+1][1]) * 2)
                    row[i][1] = ""
                i += 1
                
        return self.move_tiles(row, dir)


        