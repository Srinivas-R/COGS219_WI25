import time
import sys
import os
import numpy as np
import random
from psychopy import visual,event,core,gui

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
accepted_keys = ['r','o','y','g','b','q']
RTs = []
timer = core.Clock()

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
fixation_cross = visual.TextStim(win,text="+", height=15, color="black",pos=[0,0])
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200],autoDraw=True)
while True:
    placeholder.draw()
    fixation_cross.draw()
    win.flip()
    core.wait(0.5)
    placeholder.draw()
    win.flip()
    core.wait(0.5)
    cur_stim = random.choice(stimuli)
    word_stim.setText(cur_stim)
    word_stim.setColor(cur_stim)
    placeholder.draw()
    word_stim.draw()
    win.flip()
    timer.reset()
    key_pressed_list = event.waitKeys(keyList=accepted_keys, maxWait=2)
    RTs.append(np.round(timer.getTime()*1000))

    if key_pressed_list is None:
        word_stim.setText('TOO SLOW')
        word_stim.setColor('black')
        word_stim.draw()
        win.flip()
        core.wait(1)
    elif key_pressed_list[0] == 'q':
        win.close()
        core.quit()
    elif key_pressed_list[0] == cur_stim[0]:
        # Do nothing
        pass
    else:
        word_stim.setText('INCORRECT')
        word_stim.setColor('black')
        word_stim.draw()
        win.flip()
        core.wait(1)
