from collections import OrderedDict
from psychopy import core, visual
from functools import partial
import numpy as np

from .cfs import CFSMask, MaskedStimulus
from .clock import LibetClock

def _collect_2AFC_resp(win, kb, question, choices):
    '''
    Arguments
    -----------
    win : psychopy.visual.Window
    kb : psychopy.hardware.keyboard.Keyboard
    question : str
        Text to display while subjects are choosing.
    choices : dict[str]
        Dictionary where keys are the valid keyboard button names
        subjects can press, and entry is the response that button
        corresponds to. Using an OrderedDict is recommended to ensure
        that presentation of choices is consistent across trials.
    '''
    assert(len(choices) == 2)
    vbs = [key for key in choices] # valid buttons
    _fill_in = (vbs[0], choices[vbs[0]], vbs[1], choices[vbs[1]])
    msg = question + "\n\nPress '%s' for '%s' or '%s' for '%s.'"%_fill_in
    txt = visual.TextStim(win, text = msg, font = 'Arial')
    txt.draw()
    win.flip()
    key = kb.waitKeys(keyList = vbs, clear = True)[0]
    win.flip() # clear screen
    return choices[key.name]

def discrimination_trial(win, kb, mask_color, mask_size, stim_color,
                            stim_contrast, frame_rate = 60.):
    '''
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
    frame_rate : float, default: 60.
        The refresh rate of the monitor. This is set by the OS; you're merely
        providing it to the function so it knows how many frames should elapse
        before updating the CFS mask. (In other words, this does *not* change
        the refresh rate on its own.)
    '''
    ## present masked stimulus
    mask = CFSMask(win, mask_color, size = mask_size)
    stim = MaskedStimulus(win, stim_color, mask_size, contrast = stim_contrast)
    cfs_duration = 2. # seconds
    cfs_frames = np.round(cfs_duration * frame_rate).astype(int)
    count = 0
    stim_onset = np.random.uniform(.25, cfs_duration - .25)
    stim_pos = stim.present(time_from_now = stim_onset, duration = .2)
    while not mask.completed:
        count += 1
        if count > cfs_frames:
            mask.terminate()
        mask.draw() # update stimuli
        stim.draw()
        win.flip()
    del mask

    ## ask subject what side of mask stimulus appeared on
    question = 'Which side was the circle on?'
    choices = OrderedDict()
    choices['f'] = 'left'
    choices['j'] = 'right'
    resp = _collect_2AFC_resp(win, kb, question, choices)
    trial_data = dict(
        stimulus_position = stim_pos,
        contrast = stim_contrast,
        response = resp,
        correct = resp in stim_pos,
    )
    return trial_data

def clock_trial(win, kb, mask_color, mask_size, stim_color,
                    stim_contrast, stim_position = None, feedback = True,
                    show_mask = True, catch = False, frame_rate = 60.):
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
    feedback : bool, default: True
        Whether to show true time of button press on clock after trial ends.
    show_mask : bool, default: True
        Whether to actually mask the stimulus. If False, this will just be
        a normal intentional binding paradigm with no flash suppression, and
        the mask_color parameter will be ignored (but still must be specified
        simply because I didn't bother to set a default).
    catch : bool, default: False
        Whether this is a catch trial. On catch trials, an additional masked
        stimulus will be presented, at maximum contrast, during the first
        rotation of the Libet clock.
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
    ## setup stimuli
    mask = CFSMask(win, mask_color, size = mask_size)
    stim = MaskedStimulus(
        win, stim_color, mask_size,
        contrast = stim_contrast,
        position = stim_position
        )
    catch_stim = MaskedStimulus(
        win, stim_color, mask_size,
        contrast = 1.,
        position = None # i.e. choose randomly
        )
    cue_stim = partial(stim.present, time_from_now = .15, duration = .2)
    radius = np.sqrt(2*(mask_size/2)**2)
    clock = LibetClock(
        win, kb,
        pos = (0, 0),
        radius = radius,
        on_event = cue_stim, # executes on keypress,
        feedback = feedback
        )
    if catch: # pick a random time to present during first rotation
        assert(.5 < clock.period - .5)
        catch_t = np.random.uniform(.5, clock.period - .5)
        catch_stim.present(time_from_now = catch_t, duration = .2)

    ## main trial loop
    clock.start()
    while not clock.trial_ended:
        if not clock.spinning:
            mask.terminate()
        if show_mask:
            mask.draw()
        stim.draw()
        catch_stim.draw()
        clock.draw(frame_rate)
        win.flip()
    win.flip() # to show feedback
    if feedback:
        core.wait(2.)
    trial_data = clock.get_data()
    trial_data['stimulus_position'] = stim.position
    trial_data['catch'] = catch
    trial_data['contrast'] = stim_contrast
    trial_data['masked'] = show_mask
    del clock
    del mask

    if show_mask: # ask subject whether they saw a circle stimulus
        question = 'Did you see a circle?'
        choices = OrderedDict()
        choices['f'] = 'yes'
        choices['j'] = 'no'
        resp = _collect_2AFC_resp(win, kb, question, choices)
        trial_data['aware'] = True if resp == 'yes' else False
    return trial_data
