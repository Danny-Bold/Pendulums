from math import pi
import sys

import pygame

from Pendulums import DoublePendulum
from Scene import Scene


def main(screen, *args):
    """

    args - Pendulum.Pendulum objects

    """

    paused = True

    clock = pygame.time.Clock()

    scene = Scene(*args)

    while True:
        dt = clock.tick()
        try:
            #print(1000 / dt)
            pass

        except:
            pass
        
        dt /= 100
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

            scene.update(event)

        if not paused:
            scene.calcNewPositions(dt)

        scene.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    app = pygame.display.set_mode((640, 640), pygame.RESIZABLE)

    pl = []

    for i in range(500):
        pl.append(DoublePendulum((320, 100), [[-pi + 0.01 * i, 0, 100, 1, (255, 255, 255)], [3.12902628, 0, 100, 1, (255 - i / 500 * 255, 255, 255)]]))

    main(app, *pl)
