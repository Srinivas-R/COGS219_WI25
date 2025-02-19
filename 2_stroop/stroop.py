import time
import sys
import os
import numpy as np
import pandas as pd
import random
from psychopy import visual,event,core,gui
from generate_trials import make_incogruent, generate_trials


stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
accepted_keys = ['r','o','y','g','b','q']
RTs = []
timer = core.Clock()

#function for collecting runtime variables
def get_runtime_vars(vars_to_get,order,exp_version="Stroop"):
    infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order)
    if infoDlg.OK:
        return vars_to_get
    else: 
        print('User Cancelled')

# get the runtime variables
order =  ['subj_code','seed','reps']
runtime_vars = get_runtime_vars({'subj_code':'stroop_00','seed': 42, 'reps': 25}, order)

#add the import_trials function we've used in previous assignments
def import_trials(filepath : str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

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
    cur_text = random.choice(stimuli)
    word_stim.setText(cur_text)
    if np.random.rand() < 0.5:
        cur_color = make_incogruent(cur_text, stimuli)
    else:
        cur_color = cur_text
    word_stim.setColor(cur_color)
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
    elif key_pressed_list[0] == cur_color[0]:
        # Do nothing
        pass
    else:
        word_stim.setText('INCORRECT')
        word_stim.setColor('black')
        word_stim.draw()
        win.flip()
        core.wait(1)
