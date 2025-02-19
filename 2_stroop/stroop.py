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

#add the import_trials function we've used in previous assignments
def import_trials(filepath : str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

# get the runtime variables
order =  ['subj_code','seed','reps']
runtime_vars = get_runtime_vars({'subj_code':'stroop_00','seed': 42, 'reps': 25}, order)
# generate a trial list
generate_trials(runtime_vars['subj_code'],runtime_vars['seed'],runtime_vars['reps'])

# Output file
os.makedirs('data', exist_ok=True)
output_path = os.path.join(os.getcwd(),'data',runtime_vars['subj_code']+'_data.csv')
output_exists = False

#read in trials
trial_path = os.path.join(os.getcwd(),'trials',runtime_vars['subj_code']+'_trials.csv')
trial_df = import_trials(trial_path)
print(trial_df)

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
fixation_cross = visual.TextStim(win,text="+", height=15, color="black",pos=[0,0])
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200],autoDraw=True)


for idx, trial in trial_df.iterrows():
    placeholder.draw()
    fixation_cross.draw()
    win.flip()
    core.wait(0.5)
    placeholder.draw()
    win.flip()
    core.wait(0.5)

    cur_text = trial['word']
    word_stim.setText(cur_text)
    cur_color = trial['color']
    word_stim.setColor(cur_color)
    word_stim.setOri(0 if trial['orientation'] == 'upright' else 180)

    placeholder.draw()
    word_stim.draw()
    win.flip()
    timer.reset()
    key_pressed_list = event.waitKeys(keyList=accepted_keys, maxWait=2)
    RTs.append(np.round(timer.getTime()*1000))

    is_correct = 0
    if key_pressed_list is None:
        word_stim.setText('TOO SLOW')
        word_stim.setOri(0)
        word_stim.setColor('black')
        word_stim.draw()
        win.flip()
        core.wait(1)
    elif key_pressed_list[0] == 'q':
        win.close()
        core.quit()
    elif key_pressed_list[0] == cur_color[0]:
        is_correct = 1
        pass
    else:
        word_stim.setOri(0)
        word_stim.setText('INCORRECT')
        word_stim.setColor('black')
        word_stim.draw()
        win.flip()
        core.wait(1)
    
    trial_output = {
        'trial_num' : idx,
        'response' : key_pressed_list[0] if key_pressed_list is not None else 'NA',
        'is_correct' : is_correct,
        'rt' : RTs[-1],
    }
    trial_output.update(trial)
    temp = pd.DataFrame([trial_output])
    temp.to_csv(output_path, mode='a', header=not output_exists, index=False)
    output_exists = True  # After the first row, don't write headers again