import time
import sys
import os
import random
from psychopy import visual,event,core,gui

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
accepted_keys = ['r','o','y','g','b','q']

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
    
    key_pressed = event.waitKeys(keyList=accepted_keys)[0]
    # core.wait(1.0)
    # placeholder.draw()
    # win.flip()
    # core.wait(.15)

    if key_pressed == 'q':
        win.close()
        core.quit()
