from psychopy.visual import Line, Circle, Polygon
from psychopy.core import Clock
import numpy as np

class LibetClock:

    def __init__(self, win, pos = (0, 0), radius = 3.2,
                    period = 2.56, framerate = 60, hand_color = 'black'):

        EDGES = 256
        self.win = win
        self.radius = radius
        self.period = period
        self.pos = pos
        self.framerate = framerate
        self.clock = None
        self._event_t = None
        ## draw basic clock shape (circle and ticks)
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
        self.ticks = self.make_ticks(12, length = 1.05)
        for tick in self.ticks:
            tick.autoDraw = True
        ## pre-draw all positions of moving hand
        self.hands = self.make_arrows(EDGES, color = hand_color, length = 1.07)
        self.movable_hands = self.make_arrows( # and hand that subject can move
            EDGES,                      # when they're reporting perceived time
            color = hand_color,
            fill = False,
            length = 1.1
            )
        # lastly, some markers to show feedback after subjects respond
        self.feedback_ticks = self.make_ticks(EDGES, 'white', 1.1)

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

    def make_arrows(self, n = 12, color = 'black', fill = True, length = 1.1):
        tick_angles = -1*np.linspace(0, 2*np.pi, n + 1)[:-1]
        ticks = []
        for i in range(tick_angles.size):
            theta = tick_angles[i]
            x = np.cos(theta) * self.radius*length
            y = np.sin(theta) * self.radius*length
            r = self.radius*length - self.radius
            triangle = Polygon(
                self.win,
                pos = self.abspos((x, y)),
                edges = 3,
                radius = r,
                ori = -np.degrees(theta) - 90.,
                lineColor = color,
                fillColor = color if fill else None,
                lineWidth = self.ring.lineWidth
            )
            ticks.append(triangle)
        return ticks

    def start(self):
        self.clock = Clock()
        self.clock.reset()

    def critical_event(self):
        '''
        call this when the critical event (e.g. a button press) has occured
        '''
        self._event_t = self.clock.time() # time in trial

    def draw(self):
        '''
        updates clock; call this on every flip
        '''
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
