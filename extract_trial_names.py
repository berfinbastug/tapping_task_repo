# %%
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import librosa
import librosa.display
import re
from scipy.signal import butter, filtfilt, find_peaks
import analysis_helper_functions as ahf
import pandas as pd

# %%
def from_list_to_df(list):

    df = pd.DataFrame()

    # Step 2: Iterate through each list and add it as a row
    for lst in list:
        # Convert list to a DataFrame with one row
        row_df = pd.DataFrame([lst])
        
        # Append the row to the DataFrame, aligning columns as needed
        df = pd.concat([df, row_df], ignore_index=True)
    
    return df

# %%
clean_data_path = '/Users/bastugb/Desktop/tapping_experiment/clean_data/'



# %%
# SPECIFY DIRECTORY
data_directory = '/Users/bastugb/Desktop/tapping_experiment/data/'
block_idx = 6
participant_idx = 3

# %%
items = os.listdir(data_directory)
block_list = [item for item in items if item != '.DS_Store']
# choose one block
# later I will put a for loop here
which_block = block_list[block_idx]
block_directory = os.path.join(data_directory, which_block)
items_b = os.listdir(block_directory)
participant_list = [item for item in items_b if 'participant' in item]
# there will be a for loop here
which_participant = participant_list[participant_idx]
participant_directory = os.path.join(block_directory, which_participant)
# List all files ending with .wav
wav_files = [file for file in os.listdir(participant_directory) if file.endswith('.wav')]

# %%
data_mark = which_participant + '_' + which_block + '_'

# %%
all_wav_file_names = from_list_to_df(wav_files)
all_wav_file_names.to_csv(clean_data_path + data_mark + 'all_wav_file_names.tsv', sep='\t', index=False)


# %%
