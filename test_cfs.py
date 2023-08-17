from util.cfs import init_window, CFSMask
from psychopy import visual

SIZE = 500 # size of mask in pixels
RED = (1, 0, 0)
BLUE = (0, 0, 1)
MASK_COLOR = RED
STIM_COLOR = BLUE

win = init_window(size = (2*SIZE, 2*SIZE), units = 'pix')
mask = CFSMask(win, color = MASK_COLOR, size = SIZE)
stim_pos = dict(
    upper_right = (SIZE//4, SIZE//4),
    upper_left = (-SIZE//4, SIZE//4),
    lower_left = (-SIZE//4, -SIZE//4),
    lower_right = (SIZE//4, -SIZE//4)
    )


max_frames = 60 * 10
count = 0
circle = visual.Circle(
    win,
    size = SIZE//3,
    contrast = .3,
    pos = stim_pos['lower_right'],
    fillColor = STIM_COLOR
    )
circle.autoDraw = True
while not mask.completed:
    count += 1
    if count < max_frames:
        win.callOnFlip(mask.on_flip)
    else:
        win.callOnFlip(mask.on_flip, True)
    win.flip()
