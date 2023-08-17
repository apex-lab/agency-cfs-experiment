from psychopy import visual
import numpy as np
import os

def get_files_from_subdir(dirname, ext):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    subdir = os.path.join(this_dir, dirname)
    fnames = os.listdir(subdir)
    fnames = [f for f in fnames if ext in f]
    fpaths = [os.path.join(subdir, f) for f in fnames]
    return fpaths

class CFSMask:

    def __init__(self, win, color = (0,0,1), pos = (0, 0), size = .5,
                presentation_rate = 10., frame_rate = 60.):
        '''
        Arguments
        ---------
        color : tuple[int]
            Specifies RGB color to use for masks, e.g. (0, 0, 1) is blue
        pos : tuple
            Position of image.
        size : float:
            Size of square to draw image.
        presentation_rate : float
            Rate (in Hz) at which each subsequent mask stimulus
            should be presented.
        frame_rate : float
            The refresh rate of the monitor (or the rate at which psychopy's
            win.flip() is going to be called).
        '''
        self.win = win
        self.color = color
        self.pos = pos
        self.size = size
        self.presentation_rate = presentation_rate
        self.frame_rate = frame_rate
        self._counter = 0 # counts screen flips that have occured
        self._update_on = np.round(frame_rate / presentation_rate).astype(int)
        self.completed = False
        self._terminate = 0

        self._mondrians = self.init_mondrians()
        self._mask = self.init_mask()
        self._border = self.init_border()
        self._fixation = self.init_fixation()
        self._current_mask = None
        self._border.autoDraw = True

    def on_flip(self, terminate = False):
        '''
        Must be called on every screen flip outside this class at the flip rate
        specified in __init__ to ensure that mask stimuli update, such as:
        ```
        cfs = CFSMask(win)
        while True:
            win.callOnFlip(cfs.on_flip)
            win.flip()
        ```

        Arguments
        -----------
        terminate : bool
            If True, will switch from presenting Mondrian masks to presenting
            a single noise mask for 1/self.presentation_rate seconds at the next
            update, after which no more stimuli will be presented.
        '''
        if self.completed:
            return # stop updating
        self._counter += 1
        if terminate and (self._terminate == 0):
            self._terminate = 1
        if self._counter % self._update_on == 1: # every _update_on frames...
            self.update_mask()

    def init_mondrians(self):
        '''
        intialize the mondrian masks to be used for CFS
        '''
        fpaths = get_files_from_subdir('mondrians', '.tif')
        mondrians = [
            visual.ImageStim(
                self.win,
                image = f,
                mask = None,
                size = self.size,
                pos = self.pos,
                color = self.color,
                colorSpace = 'rgb',
                opacity = 1.,
                interpolate = True
                )
            for f in fpaths]
        return mondrians

    def init_mask(self):
        '''
        initialize the final backward mask (to reduce any visual after-effects)
        '''
        fpaths = get_files_from_subdir('masks', '.png')
        f = np.random.choice(fpaths)
        mask = visual.ImageStim(
            self.win,
            image = f,
            mask = None,
            size = self.size,
            pos = self.pos,
            interpolate = True
            )
        return mask

    def init_fixation(self):
        fixation = visual.TextStim(
            win = self.win,
            text = '+',
            ori = 0,
            color = (-1, -1, -1), # black
            font = 'Arial',
            height = self.size / 10,
            wrapWidth = None,
            opacity = 1,
            depth = -4.0
            )
        return fixation

    def init_border(self):
        border = visual.Rect(
            win = self.win,
            width = self.size,
            height = self.size,
            pos = self.pos,
            lineColor = (-1, -1, -1), # black
            fillColor = None, # empty
            colorSpace = 'rgb',
            interpolate = True
            )

        return border

    def update_mask(self):
        if self._current_mask is not None:
            self._mondrians[self._current_mask].autoDraw = False
        if self._terminate == 0:
            self._current_mask = np.random.randint(0, len(self._mondrians))
            self._mondrians[self._current_mask].autoDraw = True
        elif self._terminate == 1:
            self._mask.autoDraw = True
            self._terminate += 1
        elif self._terminate > 1:
            self.stop()
            return
        # make sure these are always on top
        self._fixation.autoDraw = True

    def stop(self):
        # make sure nothing is still autodrawing
        self._mondrians[self._current_mask].autoDraw = False
        self._mask.autoDraw = False
        self._border.autoDraw = False
        self._fixation.autoDraw = False
        self.completed = True

    def __del__(self):
        self.stop()
