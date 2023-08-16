from psychopy import visual, core, event
import random
import ImageGrab

win = visual.Window([800,700],  units="pix")

def draw_rand_sq(win, sq):
#    red = [1, -1, -1]
#    green = [-1, 1, -1]
#    blue = [-1, -1, 1]
#    yellow = [1, 1, -1]
#    black = [-1, -1, -1]
#    violet = [1,-0.3,0.7]
#    azure = [-0.6, 0.9, 1]
#    colors = [red, green, blue, yellow, black, violet, azure]
    gray1 = [0, 0, 0]
    color = colors[random.randint(0,len(colors)-1)]
    sq.fillColor = color
    sq.lineColor = color
    #sq.color = color
    sq.setPos([random.randint(-180,180), random.randint(-180,180)])
    sq.setSize(random.randrange(30,100,5))
    sq.draw()
    


c = 0.2

x = 1

#stim.contrast = c

backg = map(lambda x: x/1000.0, range(0, 10000, 100))
opacitylist = map(lambda x: x/1000.0, range(0, 10000, 20))

squares = []
for i in range(350):
    squares.append(visual.Circle(win))
    
#timer = core.CountdownTimer(10)
#while timer.getTime() > 0.001:
#    if round(timer.getTime(), 1) in backg:
#        print timer.getTime(), "weird"
#        for square in squares:
#            draw_rand_sq(win,square)
#        stim.draw()
#        win.flip()
#        stim.contrast *= 1.02
#        if stim.contrast > 1.0:
#            break
#    elif round(timer.getTime(), 1) in opacitylist:
#        stim.draw()
#        win.flip()
#        stim.contrast *= 1.02
#        print timer.getTime(),"xyz"
#        if stim.contrast > 1.0:
#            break


tme = core.getTime()

for i in range(100):
    for square in squares:
        draw_rand_sq(win,square)
    #stim.draw()
    print round(core.getTime(),2) - round(tme,2)
    win.flip()
    y = ImageGrab.grab([500,200,870,570])
    y.save("Mondrian%d.jpg" % x)
    x += 1
    core.wait(0.2)
    tme = core.getTime()
   
    #imageGrab
    #imaging library
    #python image library PIL