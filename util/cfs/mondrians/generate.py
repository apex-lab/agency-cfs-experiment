from psychopy import visual
import numpy as np

win = visual.Window([370,370],  units="pix")

def draw_rand_sq(win, sq):

    gray1 = [0, 0, 0]
    c = np.random.uniform(-1, 1)
    color = (c, c, c)
    sq.fillColor = color
    sq.lineColor = color
    sq.setPos([np.random.randint(-180,180), np.random.randint(-180,180)])
    sq.setSize(np.random.uniform(30,100))
    sq.draw()


c = 0.2
x = 1

backg = map(lambda x: x/1000.0, range(0, 10000, 100))
opacitylist = map(lambda x: x/1000.0, range(0, 10000, 20))

squares = []
for i in range(350):
    squares.append(visual.Rect(win))



for i in range(100):
    for square in squares:
        draw_rand_sq(win,square)
    win.flip()
    win.getMovieFrame()
    x += 1

win.saveMovieFrames('mondrian.tif')
