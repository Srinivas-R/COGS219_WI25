import itertools
import os
import random
import pandas as pd

def make_incogruent(color, all_colors):
    return random.choice([x for x in all_colors if x != color])

def generate_trials(subj_code: str, seed: int,num_repetitions :int =25):
    '''
    Writes a file named {subj_code_}trials.csv, one line per trial. Creates a trials subdirectory if one does not exist
    subj_code: a string corresponding to a participant's unique subject code
    seed: an integer specifying the random seed
    num_repetitions: integer specifying total times that combinations of trial type (congruent vs. incongruent) and orientation (upright vs. upside_down) should repeat (total number of trials = 4 * num_repetitions)
    '''
    # define general parameters and functions here

    stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
    trial_types = ['congruent', 'incongruent']
    orientations = ['upright', 'upside_down']
    
    # create a trials folder if it doesn't already exist
    os.makedirs('trials', exist_ok=True)
    
    # write code to loop through creating and adding trials to the file here
    trials = itertools.product(trial_types, orientations)
    trials = list(trials) * num_repetitions
    words = [random.choice(stimuli) for _ in trials]
    trials = [(subj_code, 
               seed, 
               word, 
               word if trial_type == 'congruent' else make_incogruent(word, stimuli), 
               trial_type, 
               orientation) for ((trial_type, orientation), word) in zip(trials, words)]

    df = pd.DataFrame(data=trials, columns=["subj_code", "seed", "word", "color", "trial_type", "orientation"])
    df.to_csv(f"trials/{subj_code}_trials.csv")

if __name__ == "__main__":
    generate_trials('test', 0)