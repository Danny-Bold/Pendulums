import pygame


class Scene:
    """

    A class that holds all other objects to be viewed.

    The Scene object will handle zooming and adjusting view position.

    """
    def __init__(self, *objs):
        self.zoom = 1
        self.viewPos = [0, 0]
        self.objs = objs
        self.zoomSensitivity = 1.1
        self.mousePressed = False

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for x in self.objs:
            x.draw(screen, self.viewPos, self.zoom)

    def update(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.zoom *= self.zoomSensitivity ** event.y

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mousePressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mousePressed = False

        elif event.type == pygame.MOUSEMOTION and self.mousePressed:
            self.viewPos[0] -= event.rel[0] / self.zoom
            self.viewPos[1] -= event.rel[1] / self.zoom

    def calcNewPositions(self, dt):
        for x in self.objs:
            x.update(dt)
