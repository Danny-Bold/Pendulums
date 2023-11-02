import sys
from math import sin, cos, pi

import pygame

from Scene import Scene

G = 9.81


class LinearPendulum:
    """

    The same as the Pendulum class, but follows linearised motion
    """
    def __init__(self, pos, initAngle, initVel, length, mass=1, col=(255, 255, 255)):
        self.pos = pos
        self.initAngle = initAngle
        self.angle = initAngle
        self.initVel = initVel
        self.vel = initVel
        self.length = length
        self.mass = mass
        self.col = col

    def draw(self, screen, coords, zoom):
        pygame.draw.aaline(screen, self.col,
                           ((self.pos[0] - coords[0]) * zoom, (self.pos[1] - coords[1]) * zoom),
                           ((self.pos[0] + self.length * sin(self.angle) - coords[0]) * zoom,
                            (self.pos[1] + self.length * cos(self.angle) - coords[1]) * zoom))
        pygame.draw.circle(screen, self.col,
                           ((self.pos[0] + self.length * sin(self.angle) - coords[0]) * zoom,
                            (self.pos[1] + self.length * cos(self.angle) - coords[1]) * zoom), 10)

    def update(self, dt):
        """

        The system follows theta_tt = -g/l * sin(theta)

        """
        accel = -G / self.length * self.angle
        self.vel += accel * dt
        self.angle += self.vel * dt


class Pendulum:
    def __init__(self, pos, initAngle, initVel, length, mass=1, col=(255, 255, 255)):
        self.pos = pos
        self.initAngle = initAngle
        self.angle = initAngle
        self.initVel = initVel
        self.vel = initVel
        self.length = length
        self.mass = mass
        self.col = col

    def draw(self, screen, coords, zoom):
        pygame.draw.aaline(screen, self.col,
                           ((self.pos[0] - coords[0]) * zoom, (self.pos[1] - coords[1]) * zoom),
                           ((self.pos[0] + self.length * sin(self.angle) - coords[0]) * zoom,
                            (self.pos[1] + self.length * cos(self.angle) - coords[1]) * zoom))
        pygame.draw.circle(screen, self.col,
                           ((self.pos[0] + self.length * sin(self.angle) - coords[0]) * zoom,
                            (self.pos[1] + self.length * cos(self.angle) - coords[1]) * zoom), 10)

    def update(self, dt):
        """

        The system follows theta_tt = -g/l * sin(theta)

        """
        accel = -G / self.length * sin(self.angle)
        self.vel += accel * dt
        self.angle += self.vel * dt


class DoublePendulum:
    def __init__(self, pos, pendInfo):
        """

        pendInfo takes the form:
        [initAngle, initVel, length, mass, col]

        """

        self.pos = pos
        self.pend1 = pendInfo[0]
        self.pend2 = pendInfo[1]

        self.INIT_INFO = [pendInfo[0][0:1], pendInfo[1][0:1]]  # For book-keeping only

    def draw(self, screen, coords, zoom):
        pend1Pos = [((self.pos[0] - coords[0]) * zoom, (self.pos[1] - coords[1]) * zoom),
                    ((self.pos[0] + self.pend1[2] * sin(self.pend1[0]) - coords[0]) * zoom,
                     (self.pos[1] + self.pend1[2] * cos(self.pend1[0]) - coords[1]) * zoom)]

        pend2Pos = ((self.pos[0] + self.pend1[2] * sin(self.pend1[0]) + self.pend2[2] *
                     sin(self.pend2[0]) - coords[0]) * zoom,
                    (self.pos[1] + self.pend1[2] * cos(self.pend1[0]) + self.pend2[2] * cos(self.pend2[0]) -
                     coords[1]) * zoom)

        pygame.draw.aaline(screen, self.pend1[4], pend1Pos[0], pend1Pos[1])
        pygame.draw.circle(screen, self.pend1[4], pend1Pos[1], 10)

        pygame.draw.aaline(screen, self.pend2[4], pend1Pos[1], pend2Pos)
        pygame.draw.circle(screen, self.pend2[4], pend2Pos, 10)

    def update(self, dt):
        # Same denominator for both pendulum expressions
        denom = self.pend1[2] * (2 * self.pend1[3] + self.pend2[3] - self.pend2[3] * cos(2 * self.pend1[0] -
                                                                                         2 * self.pend2[0]))

        pend1Accel = (-G * (2 * self.pend1[3] + self.pend2[3]) * sin(self.pend1[0]) - self.pend2[3] * G *
                      sin(self.pend1[0] - 2 * self.pend2[0]) - 2 * sin(self.pend1[0] - self.pend2[0]) * self.pend2[3] *
                      ((self.pend2[1] ** 2) * self.pend2[2] + (self.pend1[1] ** 2) * self.pend1[2] *
                       cos(self.pend1[0] - self.pend2[0]))) / denom

        self.pend1[1] += pend1Accel * dt
        self.pend1[0] += self.pend1[1] * dt

        pend2Accel = 2 * sin(self.pend1[0] - self.pend2[0]) * ((self.pend1[1] ** 2) * self.pend1[2] * (self.pend1[3] +
                                                                                                       self.pend2[3]) +
                                                               G * (self.pend1[3] + self.pend2[3]) * cos(self.pend1[0])
                                                               + (self.pend2[1] ** 2) * self.pend2[2] * self.pend2[3] *
                                                               cos(self.pend1[0] - self.pend2[0])) / denom

        self.pend2[1] += pend2Accel * dt
        self.pend2[0] += self.pend2[1] * dt


if __name__ == '__main__':
    p = DoublePendulum((320, 100), [[pi / 2, 0, 100, 1000, (255, 0, 0)],
                                    [pi / 2, 0, 100, 60, (0, 0, 255)]])

    s = Scene(p)

    app = pygame.display.set_mode((640, 640))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            s.update(event)

        s.draw(app)

        pygame.display.flip()
