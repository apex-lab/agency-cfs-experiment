from util.cfs import init_window, CFSMask
from psychopy import visual

win = init_window(size = (1000, 1000))
mask = CFSMask(win, color = (1, 0, 0), size = 1.)

maximum = 60 * 10
count = 0
circle = visual.Circle(
    win,
    size = 1.,
    contrast = 1.,
    pos = (0, 0),
    fillColor = (0, 0, 1)
    )
circle.autoDraw = True
while not mask.completed:
    count += 1
    if count < maximum:
        win.callOnFlip(mask.on_flip)
    else:
        win.callOnFlip(mask.on_flip, True)
    win.flip()
