from util.trials import discrimination_trial, clock_trial
from util.input import get_keyboard
from util.cfs import init_window
from util.logging import TSVLogger
from util.bopt import QuestObject
from psychopy import core
import numpy as np

MASK_SIZE = 500 # size of mask in pixels
RED = (1, 0, 0)
BLUE = (0, 0, 1)
FRAME_RATE = 60.
SCREEN_SIZE = (1000, 1000) # in pixels
LOG_DIRECTORY = 'logs'

CALIBRATION_BLOCK_TRIALS = 5
CLOCK_BLOCK_TRIALS = 5 # per block; there are four blocks
PRACTICE_TRIALS = 2
CATCH_TRIALS = 1

## experimenter inputs subject identifier from Terminal
sub_num = input("Enter subject number: ")
sub_num = int(sub_num)
sub_id = '%02d'%sub_num
# init clock to keep track of time in experiment
timer = core.Clock()
timer.reset(0.)

win = init_window(size = SCREEN_SIZE, units = 'pix')
kb = get_keyboard()
trial_params = dict(
    win = win,
    kb = kb,
    mask_color = RED,
    mask_size = MASK_SIZE,
    stim_color = BLUE,
    frame_rate = FRAME_RATE
)

## CALIBRATION BLOCK ##########################################################
# initialize logger
fields = [
    'trial', 'onset',
    'contrast', 'stimulus_position',
    'response', 'correct',
    'post_5th_perc', 'post_mean', 'post_95th_perc'
    ]
log = TSVLogger(sub_id, 'discrimination', fields, LOG_DIRECTORY)
# initialize QUEST with log-scale priors
tGuess = np.log10(.5) # prior mean on log10 scale
tGuessSd = 3.0 # sd of Gaussian prior; be generous
pThreshold = 0.525 # threshold criterion (i.e. minimum accuracy of interest)
beta = 3.5 # slope to use during optimization (3.5 if on log10 scale)
delta = 0.01 # lapse rate, usually 0.01
gamma = 0.5 # chance performance
quest = QuestObject(tGuess, tGuessSd, pThreshold, beta, delta, gamma)

for trial in range(1, CALIBRATION_BLOCK_TRIALS + 1):
    # record trial onset time
    t0 = timer.getTime()
    # next stimulus contrast is mean of current threshold posterior
    post_mean = 10**quest.mean() # convert back from log10 scale
    post_5th_perc = 10**quest.quantile(.05)
    post_95th_perc = 10**quest.quantile(.95)
    contrast = np.clip(post_mean, a_min = 0., a_max = 1.) # enforce range
    # now see if subject can tell us what side masked stim is on
    trial_data = discrimination_trial(stim_contrast = contrast, **trial_params)
    accuracy = trial_data['correct']
    # and update posterior accordingly
    quest.update(np.log10(contrast), int(accuracy))
    # then add everything to experiment log
    log.write(
        trial = trial,
        onset = t0,
        post_mean = post_mean,
        post_5th_perc = post_5th_perc,
        post_95th_perc = post_95th_perc,
        **trial_data
        )
log.close()

## based on behavioral results above, #########################################
## pick stimulation intensity for the rest of the experiment... ###############
quest.beta_analysis() # Re-fit with slope as free parameter,
contrast = 10**quest.quantile(.05) # and use lower edge of .9 credible interval
print('\n\nBelow-threshold contrast is %.03f.\n\n'%contrast)
try: # check that we got a reasonable value
    assert(contrast > 0.)
except: # If we didn't, it's a big problem! So stop the experiment now.
    raise Exception(
        '''
        Optimization procedure yielded a negative contrast!
        Something is wrong. Probably best to send this subject home...
        '''
    )
trial_params['stim_contrast'] = contrast

## Now let's start the main experiment. #######################################
# initalize new logger
fields = [
    'trial', 'practice', 'catch', 'onset',
    'contrast', 'stimulus_position',
    'event_t', 'event_angle', 'resp_angle', 'overest_t', 'overest_angle',
    'saw_circle'
]
log = TSVLogger(sub_id, 'clock', fields, LOG_DIRECTORY)
# pick a position for operant stimulus
stim_pos = np.random.choice([
    'upper_left', 'upper_right',
    'lower_left', 'lower_right'
    ])
trial_params['stim_position'] = stim_pos
# start with practice trials
catch = np.array([True] + (PRACTICE_TRIALS - 1)*[False]) # include 1 catch trial
np.random.shuffle(catch)
practice = True
for trial in range(1, PRACTICE_TRIALS + 1):
    t0 = timer.getTime()
    trial_data = clock_trial(
        show_mask = True,
        catch = catch[trial - 1],
        **trial_params
        )
    log.write(trial = trial, onset = t0, practice = True, **trial_data)
log.close()