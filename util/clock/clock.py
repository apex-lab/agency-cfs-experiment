from psychopy.visual import Line, Circle
from psychopy.core import Clock
import numpy as np

class LibetClock:

    def __init__(self, win, pos = (0, 0), radius = 3.2,
                    period = 2.56, framerate = 60, hand_color = 'green'):

        EDGES = 256
        self.win = win
        self.radius = radius
        self.period = period
        self.pos = pos
        self.framerate = framerate
        self.ring = Circle(
            win,
            radius = radius,
            edges = EDGES,
            pos = pos,
            fillColor = 'grey',
            lineColor = 'black',
            lineWidth = 5
            )
        self.ring.autoDraw = True
        self.ticks = self.make_ticks(12)
        for tick in self.ticks:
            tick.autoDraw = True
        self.hands = self.make_ticks(EDGES, color = hand_color, length = 1.2)
        self.clock = None

    def abspos(self, relpos):
        '''
        Given a position relative to clock center, returns
        an absolute position.
        '''
        return self.pos[0] + relpos[0], self.pos[1] + relpos[1]

    def make_ticks(self, n_ticks = 12, color = 'black', length = 1.1):
        tick_angles = -1*np.linspace(0, 2*np.pi, n_ticks + 1)[:-1]
        ticks = []
        for i in range(tick_angles.size):
            theta = tick_angles[i]
            x = np.cos(theta)
            x_start = self.radius * x
            x_end = length*self.radius * x
            y = np.sin(theta)
            y_start = self.radius * y
            y_end = length*self.radius * y
            line = Line(
                self.win,
                self.abspos((x_start, y_start)),
                self.abspos((x_end, y_end)),
                lineColor = color,
                lineWidth = self.ring.lineWidth
                )
            ticks.append(line)
        return ticks

    def start(self):
        self.clock = Clock()
        self.clock.reset()

    def on_flip(self):
        if self.clock is None: # not started yet
            return
        # determine which hand position should be drawn
        t = self.clock.getTime()
        clock_phase = (t % self.period) / self.period
        idx = np.floor(len(self.hands) * clock_phase).astype(int)
        # and draw it!
        self.hands[idx].draw()

    @property
    def first_rotation_complete(self):
        if self.clock is None: # not started yet
            return False
        return self.clock.getTime() > self.period
