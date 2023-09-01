from functools import partial
from psychopy import core
import numpy as np

from .cfs import CFSMask, MaskedStimulus
from .clock import LibetClock

def discrimination_trial(win, mask_color, mask_size, stim_color,
                            stim_contrast, frame_rate = 60.):

    mask = CFSMask(win, mask_color, size = mask_size)
    stim = MaskedStimulus(win, stim_color, mask_size, contrast = stim_contrast)

    cfs_duration = 5. # seconds
    cfs_frames = np.round(cfs_duration * frame_rate).astype(int)
    count = 0
    stim_onset = np.random.uniform(.5, 4.5)
    stim_pos = stim.present(time_from_now = stim_onset, duration = .2)
    while not mask.completed:
        count += 1
        if count > cfs_frames:
            mask.terminate()
        mask.draw() # update stimuli
        stim.draw()
        win.flip()
    del mask
    return stim_pos

def clock_trial(win, kb, mask_color, mask_size, stim_color,
                    stim_contrast, stim_position = None,
                    show_mask = True, frame_rate = 60.):
    '''
    Measures action binding with a masked operant stimulus.

    For baseline condition (i.e. no operant stimulus), just set stim_contrast
    to zero. This ensures code/timing is exactly the same for both conditions,
    since psychopy technically still draws an (invisible) stimulus.

    Arguments
    -----------
    win : psychopy.visual.Window
    kb : psychopy.hardware.keyboard.Keyboard
    mask_color : str
        Should be 'red', 'green', or 'blue' (depending on the color of your
        anaglyph glasses).
    mask_size : float
        In units set when initializing `win`.
    stim_color : str
        Should be 'red', 'green', or 'blue', but not the same as `mask_color`.
    stim_contrast : float
        Ranges from 0 to 1. For baseline trials, set to zero, and set to
        something non-zero for operant trials.
    stim_position : str, default: None
        One of 'upper_right',  'upper_left', 'lower_right', or 'lower_left'.
        This is the corner of the CFS mask the masked sitmulus should be
        drawn in. Can also be None if you want the stim position to be random.
    show_mask : bool, default: True
        Whether to actually mask the stimulus. If False, this will just be
        a normal intentional binding paradigm with no flash suppression, and
        the mask_color parameter will be ignored (but still must be specified
        simply because I didn't bother to set a default).
    frame_rate : float, default: 60.
        The refresh rate of the monitor. This is set by the OS; you're merely
        providing it to the function so it knows how many frames should elapse
        before updating the CFS mask. (In other words, this does *not* change
        the refresh rate on its own.)

    Returns
    ----------
    trial_data : dict
        Dictionary containing information about trial/subject responses.
    '''
    mask = CFSMask(win, mask_color, size = mask_size)
    stim = MaskedStimulus(
        win, stim_color, mask_size,
        contrast = stim_contrast,
        position = stim_position
        )
    cue_stim = partial(stim.present, time_from_now = .15, duration = .2)
    radius = np.sqrt(2*(mask_size/2)**2)
    clock = LibetClock(
        win, kb,
        pos = (0, 0),
        radius = radius,
        on_event = cue_stim, # executes on keypress,
        feedback = True
        )

    clock.start()
    while not clock.trial_ended:
        if not clock.spinning:
            mask.terminate()
        if show_mask:
            mask.draw()
        stim.draw()
        clock.draw(frame_rate)
        win.flip()
    win.flip() # to show feedback
    core.wait(2.)
    data = clock.get_data()
    data['stimulus_position'] = stim.position
    del clock
    del mask
    win.flip() # stop showing feedback
    return data
