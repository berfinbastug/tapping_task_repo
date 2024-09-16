# %%
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import cleaning_analysis_helper_functions as ahf
import pandas as pd
import random

# %%
import os

# Specify directory
data_directory = '/Users/bastugb/Desktop/tapping_experiment/data/'

# Specify block and participant IDs
block_id = 'block6'
participant_id = '5'

# Filter for block and participant
try:
    # Find the block matching block_id
    tmp_block = next(item for item in os.listdir(data_directory) if block_id in item)

    # Directory for participants within the block
    participants_directory = os.path.join(data_directory, tmp_block)
    
    # Find the participant matching participant_id
    tmp_participant = next(item for item in os.listdir(participants_directory) if participant_id in item)

    # Get participant directory
    participant_directory = os.path.join(participants_directory, tmp_participant)

    # List all .wav files in the participant directory
    wav_trials = [file for file in os.listdir(participant_directory) if file.endswith('.wav')]

    #print("WAV Trials:", wav_trials)

except StopIteration:
    print("Block or participant not found.")
except FileNotFoundError as e:
    print(f"Error: {e}")



# %% 
# to control whether the data looks okay or not, generate random numbers and plot the data of these trials

# Generate a list of 10 random 4-digit numbers 
random_trials = [random.randint(0, 29) for _ in range(10)] 
print(random_trials)


# %%
# READ OUT THE SIGNAL
for i in random_trials:

    full_name = participant_directory + '/' + wav_lists[i]
    unitdur_value = ahf.find_unitdur(full_name)
    sample_rate, data = wavfile.read(full_name)
    sound_data_index = 0
    tapping_data_index = 1
    sound_data = data[:,sound_data_index]
    tapping_data = data[:, tapping_data_index]
    # check whether the size of tapping data equals to the size of the sound data
    sound_data.size == tapping_data.size
    # to find the transition point from zero energy to an actual signal
    # reshape the signal to a 1D array if needed
    signal = sound_data.flatten()
    # Define a small threshold to differentiate between zero-padding and actual signal
    zp_threshold = 0.001  # You can adjust this based on the noise level in your signal
    start_index, end_index, start_time, end_time = ahf.find_zeropad_transitions(sound_data, zp_threshold, sample_rate)
    print(f"Start of the actual signal: Sample {start_index} (Time {start_time:.2f} seconds)")
    print(f"End of the actual signal: Sample {end_index} (Time {end_time:.2f} seconds)")
    # Plot the signal with transition points
    # Calculate time in seconds for each sample
    time_axis = np.arange(len(signal)) / sample_rate
    ahf.plot_sound_onset_offset_marker(time_axis, signal, start_time, end_time)
    onset_threshold = 0.6
    actual_onsets = ahf.extract_onsets(signal, start_index, end_index, unitdur_value, sample_rate, onset_threshold)
    actual_onsets_seconds = actual_onsets/sample_rate
    # make sure that the time between two onset points equals to the actual unit duration values
    check_onsets = np.diff(actual_onsets_seconds) 
    print(check_onsets)
    # Plot the signal with detected onsets
    # sound signal
    ax = ahf.plot_signal_with_onsets(time_axis, signal, actual_onsets, sample_rate)
    # tapping signal
    ax = ahf.plot_signal_with_onsets(time_axis, tapping_data, actual_onsets, sample_rate)


# %%
