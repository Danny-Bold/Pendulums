from math import pi
import sys

import pygame

from Pendulums import Pendulum, LinearPendulum
from Scene import Scene


def main(screen, *args):
    """

    args - Pendulum.Pendulum objects

    """

    clock = pygame.time.Clock()

    scene = Scene(*args)

    while True:
        dt = clock.tick() / 100
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            scene.update(event)

        scene.calcNewPositions(dt)

        scene.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    app = pygame.display.set_mode((640, 640))
    p1 = Pendulum((320, 100), 3 * pi / 4, 0, 100)
    p2 = Pendulum((320, 100), pi / 4, 0, 100)
    cols = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (102, 0, 204), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 128, 0), (51, 255, 255), (100, 100, 100)]
    p = [LinearPendulum((320, 100), pi / 4, 0, 100 + 10 * k) for k in range(1, 30)]
    main(app, *p)
