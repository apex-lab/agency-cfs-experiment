from psychopy import visual

def _display_text(win, txt, **txt_kwargs):
    '''
    Parameters
    ----------
    win : psychopy.visual.Window
    txt : str
        Text to display.
    '''
    msg = visual.TextStim(
        win,
        text = txt,
        pos = (0,0),
        font = 'Arial',
        depth = -4.0,
        **txt_kwargs
        )
    msg.draw()
    win.flip()

def _wait_for_spacebar(kb):
    '''
    Parameters
    ----------
    kb : psychopy.hardware.Keyboard
    '''
    kb.waitKeys(keyList = ['space'], clear = True)

def show_instructions(win, kb, msg, max_width = None):
    if max_width is None:
        max_width = win.size[0]
    msg += '\n(Press the space bar to continue.)'
    _display_text(win, msg, wrapWidth = max_width)
    _wait_for_spacebar(kb)

def discrimination_instructions(win, kb):
    msg = '''
    Welcome to the experiment.
    '''
    show_instructions(win, kb, msg)
    msg = '''
    In this first task, one circle will be briefly flashed among
    many flashing squares.

    Your job is to tell us which side the circle is on (left or right).
    You will respond with your keyboard.
    '''
    show_instructions(win, kb, msg)
    msg = '''
    The circle will appear briefly on every trial, but it may be
    so faint that it is very difficult to see.

    If you are unsure which side the circle was on, please make your best guess.
    This task is difficult, and it is normal to have to guess on many trials.
    '''
    show_instructions(win, kb, msg)
    msg = '''
    Please keep your gaze fixated at the cross (+)
    in the middle of the screen during the task.

    Please DO NOT attempt to cheat by closing one eye
    or by crossing your eyes.

    Again, the task is quite difficult and it is expected you
    will have to guess often.
    '''
    show_instructions(win, kb, msg)
    msg = '''
    If you have any questions, please ask the experimenter now.

    Otherwise, you can begin the experiment by pressing space.
    '''
    show_instructions(win, kb, msg)

def post_block_instructions(win, kb):
    msg = 'You have completed an experiment block.'
    show_instructions(win, kb, msg)

def _clock_instructions(win, kb):
    msg = '''
    In this block, you will see a 'clock' with a rotating 'hand.'

    At a time of your choice following the first rotation
    of the clock, you should press the space bar.

    When you do, please note the position of the clock hand.

    After the clock stops spinning, you will be asked to guide the
    clock hand back to the position it was in when you pressed space.
    '''
    show_instructions(win, kb, msg)
    msg = '''
    If you press the space bar before the clock completes its first
    rotation, that button press will not register.

    Again, please wait until the first rotation completes to make your press.
    Do not press the button repeatedly to try to speed through the task,
    or you will not receive compensation.

    After each trial, you will see the true position that the clock
    hand was in when you pressed the space bar displayed in white.

    Please try to be as accurate as possible.
    '''
    show_instructions(win, kb, msg)

def clock_instructions_masked(win, kb):
    _clock_instructions(win, kb)
    msg = '''
    Additionally, you will see the same squares from the first block
    flashing in the middle of the clock.

    Instead of appearing on every trial as in the first block,
    a circle will only appear on a small proportion of trials.

    We will ask you after each trial whether you saw a circle appear.
    Please answer to the best of your knowledge.
    '''
    show_instructions(win, kb, msg)
    msg = '''
    You will start with some practice trials.

    Please ask the experimenter if you have any questions.

    Otherwise, you may press space to begin the practice trials.
    '''
    show_instructions(win, kb, msg)

def clock_instructions_unmasked(win, kb):
    msg = '''
    In the next block, you will complete the same clock task
    as in the previous two blocks.

    However, this time there will be no flashing quares.
    There is no need to report if you see a circle.
    '''
    show_instructions(win, kb, msg)
    msg = '''
    You will again begin with some practice trials.

    Please let the experimenter know if you have any questions.

    Otherwise, you may press space to begin the practice trials.
    '''
    show_instructions(win, kb, msg)

def same_as_previous_instructions(win, kb):
    msg = '''
    The instructions for the next block are the same
    as those for the previous block.

    Please let the experimenter know if you have any questions.

    Otherwise, you may press space to begin the practice trials.
    '''
    show_instructions(win, kb, msg)

def post_practice_trial_instructions(win, kb):
    msg = 'You have completed the practice trials.'
    show_instructions(win, kb, msg)
    msg = '''
    Please let the experimenter know if you have any questions.

    Otherwise, you may press space to start the main block.
    '''
    show_instructions(win, kb, msg)

def post_experiment_instructions(win, kb):
    msg = 'You have completed the experiment!'
    show_instructions(win, kb, msg)
    msg = '''
    Thank you for participating.

    Please press space to close the experiment,
    and notify the experimenter that you're done.
    '''
    show_instructions(win, kb, msg)
