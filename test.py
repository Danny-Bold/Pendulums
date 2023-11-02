import pygame


class Square:
    def __init__(self, side, pos):
        self.side = side
        self.pos = pos

    def draw(self, screen, coords, zoom):
        pygame.draw.rect(screen, (255, 255, 255), ((self.pos[0] - coords[0]) * zoom, (self.pos[1] - coords[1]) * zoom,
                                                   self.side * zoom, self.side * zoom))
