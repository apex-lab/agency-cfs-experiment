from util.cfs import init_window, CFSMask, MaskedStimulus
from psychopy import visual

SIZE = 500 # size of mask in pixels
RED = (1, 0, 0)
BLUE = (0, 0, 1)

win = init_window(size = (2*SIZE, 2*SIZE), units = 'pix')
mask = CFSMask(win, color = RED, size = SIZE)
stim = MaskedStimulus(win, BLUE, SIZE, contrast = 1.)

max_frames = 60 * 10
count = 0

stim.present(time_from_now = 4., duration = 4.)
while not mask.completed:
    count += 1
    if count > max_frames:
        mask.terminate()
    mask.on_flip() # update stimuli
    stim.on_flip()
    win.flip()
