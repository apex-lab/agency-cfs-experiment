from util.cfs import init_window, CFSMask

win = init_window(size = (1000, 1000))
mask = CFSMask(win, color = (1, 0, 0), size = 1.)

maximum = 60 * 5
count = 0
while mask.completed is False:
    count += 1
    if count < maximum:
        win.callOnFlip(mask.on_flip)
    else:
        win.callOnFlip(mask.on_flip, True)
    win.flip()
