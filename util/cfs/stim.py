from psychopy import visual, core
import numpy as np

class MaskedStimulus:

    def __init__(self, win, color, mask_size, contrast, position = None, mask_pos = (0, 0)):

        possible_positions = dict(
            upper_right = (mask_pos[0] + mask_size//4, mask_pos[1] + mask_size//4),
            upper_left = (mask_pos[0] - mask_size//4, mask_pos[1] + mask_size//4),
            lower_left = (mask_pos[0] - mask_size//4, mask_pos[1] - mask_size//4),
            lower_right = (mask_pos[0] + mask_size//4, mask_pos[1] - mask_size//4)
            )
        if position is None:
            self.position = np.random.choice([key for key in possible_positions])
        else:
            self.position = position
        self.circle = visual.Circle(
            win,
            size = mask_size//3,
            contrast = contrast,
            pos = possible_positions[self.position],
            fillColor = color
            )
        self._triggered = False
        self._clock = core.Clock()

    def present(self, time_from_now, duration):
        self._clock.reset(0.)
        self._onset = time_from_now
        self._offset = time_from_now + duration
        self._triggered = True
        return self.position

    def on_flip(self):
        if not self._triggered:
            return
        t = self._clock.getTime()
        if t >= self._onset and t < self._offset:
            self.circle.draw()
