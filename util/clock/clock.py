from psychopy.visual import Line, Circle, Polygon
from psychopy.core import Clock
import numpy as np

class LibetClock:

    def __init__(self, win, kb, pos = (0, 0), radius = 3.2,
                    period = 2.56, hand_color = 'black', feedback = True):

        EDGES = 256
        self.win = win
        self.kb = kb
        self.radius = radius
        self.period = period
        self.pos = pos
        self._start_angle = np.random.uniform(0, 2*np.pi)
        self.clock = None
        self._event_t = None
        self.trial_ended = False
        self._give_feedback = feedback
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
        self.ticks = self.make_ticks(60, length = 1.05)
        for tick in self.ticks:
            tick.autoDraw = True
        ## pre-draw all positions of moving hand
        self.hands = self.make_arrows(EDGES, color = hand_color, length = 1.07)
        self.cursors = self.make_arrows( # and hand that subject can move
            EDGES,                      # when they're reporting perceived time
            color = hand_color,
            fill = False,
            length = 1.07
            )
        # lastly, some markers to show feedback after subjects respond
        self.feedback_ticks = self.make_ticks(EDGES, 'white', 1.2)

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
        self.kb.clock.reset()
        self.clock.reset()

    def time_to_deg(self, t):
        '''
        return angle (in radians) corresponding corresponding to
        a time after trial start
        '''
        clock_phase = (t % self.period) / self.period
        rad = 2*np.pi * clock_phase
        rad += self._start_angle
        rad %= (2*np.pi)
        return rad

    def deg_to_idx(self, rad):
        '''
        return index of pre-generated hand/marker at a given angle
        '''
        clock_phase = rad / (2*np.pi)
        idx = int(len(self.hands) * clock_phase)
        return idx

    @property
    def first_rotation_complete(self):
        if self.clock is None: # not started yet
            return False
        return self.clock.getTime() > self.period

    def check_for_event(self):
        if not self.first_rotation_complete: # too soon for event
            self.kb.clearEvents(eventType = ['space'])
            return
        if self._event_t is not None: # event already happened
            return
        keys = self.kb.getKeys(keyList = ['space'], waitRelease = False)
        if keys:
            key = keys[0]
            self.critical_event(key.rt)

    def critical_event(self, t):
        '''
        call this when the critical event (e.g. a button press) has occured
        '''
        self._event_t = t
        self._event_deg = self.time_to_deg(self._event_t)
        self._end_t = self._event_t + np.random.choice([1., 1.5, 2.])
        self._choice_t = self._end_t + 1.
        init_offset = np.random.uniform(np.pi/4, np.pi/3)
        init_offset *= np.random.choice([-1., 1.])
        self._resp_deg = self._event_deg + init_offset

    @property
    def critical_event_occured(self):
        t = self.clock.getTime()
        if self._event_t is None:
            return False
        return True

    @property
    def spinning(self):
        if not self.critical_event_occured:
            return True
        if self.clock.getTime() < self._end_t:
            return True
        return False

    @property
    def intermission(self):
        t = self.clock.getTime()
        if t < self._choice_t:
            return True
        return False

    def end_trial(self, resp_deg):
        resp_idx = idx = self.deg_to_idx(resp_deg)
        self.cursors[resp_idx].autoDraw = True
        event_idx = self.deg_to_idx(self._event_deg)
        if self._give_feedback:
            self.feedback_ticks[event_idx].autoDraw = True
        self.trial_ended = True


    def update_cursor(self):
        speed = .5*np.pi / len(self.cursors)
        keys = self.kb.getKeys(
            keyList = ['left', 'right', 'space'],
            waitRelease = False,
            clear = False
            )
        for key in keys: # check if currently held down
            if key.name == 'left' and key.duration is None:
                self._resp_deg -= speed
            if key.name == 'right' and key.duration is None:
                self._resp_deg += speed
            self._resp_deg %= 2*np.pi
            if key.name == 'space':
                self.end_trial(self._resp_deg)
        idx = self.deg_to_idx(self._resp_deg)
        self.cursors[idx].draw()

    def draw(self):
        '''
        updates clock display; call this on every flip
        '''
        if self.clock is None: # not started yet
            return
        if self.spinning:
            # determine which position hand should be drawn
            t = self.clock.getTime()
            theta = self.time_to_deg(t)
            idx = self.deg_to_idx(theta)
            # and draw it!
            self.hands[idx].draw()
            if not self.critical_event_occured:
                self.check_for_event()
            return
        if self.intermission: # then hand should vanish
            self.kb.clearEvents(eventType = ['space', 'left', 'right'])
            return
        if not self.trial_ended:
            self.update_cursor()
            return
        return
