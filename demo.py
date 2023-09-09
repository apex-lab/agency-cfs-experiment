from functools import partial
import numpy as np

from psychopy.hardware.keyboard import KeyPress
from psychopy import core, visual

from util.cfs import init_window, CFSMask, MaskedStimulus
from util.clock import LibetClock


SIZE = 370 # size of mask in pixels
RED = (1, 0, 0)
BLUE = (0, 0, 1)
WIN_SIZE = (1500, 750)

offset = WIN_SIZE[0] // 4
MASK_POS = (-offset, 0)
STIM_POS = (offset, 0)


class MockKeyboard:

    def __init__(self, wait = 3.):
        self.wait = wait
        self.clock = core.Clock()
        return None

    def getKeys(self, **kwargs):
        t = self.clock.getTime()
        if t < self.wait:
            return []
        name = kwargs['keyList'][0]
        key = KeyPress(0, t, name)
        key.rt = t
        key.name = name
        np.random.seed(0) # clocks pick same cursor offset
        return [key]

    def clearEvents(self, **kwargs):
        return None

kb = MockKeyboard()
win = init_window(size = WIN_SIZE, units = 'pix')

# masks on one side ...
mask = CFSMask(win, RED, size = SIZE, pos = MASK_POS)
_mask = CFSMask(win, RED, size = SIZE, pos = STIM_POS)
# ... and operant stimulus on the other
stim = MaskedStimulus(win, BLUE, SIZE, contrast = 1., mask_pos = STIM_POS)
cue_stim = partial(stim.present, time_from_now = .15, duration = .2)

np.random.seed(0)
clock1 = LibetClock(
    win, kb,
    pos = MASK_POS,
    radius = np.sqrt(2*(SIZE/2)**2)
    )
np.random.seed(0)
clock2 = LibetClock(
    win, kb,
    pos = STIM_POS,
    radius = np.sqrt(2*(SIZE/2)**2),
    on_event = cue_stim
    )

win_height = WIN_SIZE[1] // 2
divider = visual.Line(
    win,
    (0, win_height), (0, -win_height),
    lineColor = (-1, -1, -1)
    )

clock1.start()
clock2.start()
while clock1.spinning:
    stim.draw()
    clock1.draw(60.)
    clock2.draw(60.)
    mask.draw()
    divider.draw()
    win.flip()
    win.getMovieFrame()
mask.terminate()
timer = core.Clock()
timer.reset()
while timer.getTime() < 5.:
    stim.draw()
    clock1.draw(60.)
    clock2.draw(60.)
    mask.draw()
    divider.draw()
    win.flip()
    win.getMovieFrame()

del clock1
del clock2
del mask
del _mask
del divider
del stim 

fname = 'side-by-side.mp4'
win.saveMovieFrames(fname)
win.close()
