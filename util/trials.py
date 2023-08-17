from .cfs import CFSMask, MaskedStimulus
from psychopy import visual
import numpy as np

def discrimination_trial(win, mask_color, mask_size, stim_color, stim_constrast, frame_rate = 60.):

    mask = CFSMask(win, mask_color, size = mask_size)
    stim = MaskedStimulus(win, stim_color, mask_size, contrast = stim_constrast)

    cfs_duration = 5. # seconds
    cfs_frames = np.round(cfs_duration * frame_rate).astype(int)
    count = 0
    stim_onset = np.random.uniform(.5, 4.5)
    stim_pos = stim.present(time_from_now = stim_onset, duration = .2)
    while not mask.completed:
        count += 1
        if count > cfs_frames:
            mask.terminate()
        mask.on_flip() # update stimuli
        stim.on_flip()
        win.flip()
    return stim_pos
