# %%
import os
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import librosa
import librosa.display
import re
from scipy.signal import butter, filtfilt, find_peaks
import cleaning_analysis_helper_functions as ahf
import pandas as pd

# %%
# Specify directory
clean_data_path = '/Users/bastugb/Desktop/tapping_experiment/clean_data/'
data_directory = '/Users/bastugb/Desktop/tapping_experiment/data/'

# Specify block and participant IDs
block_id = 'block1'
participant_id = '7'

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
# TO STORE ITEMS
all_unit_dur_values = []
all_tap_onset_points_in_time = []
all_tap_onset_points_in_signal = []
all_actual_onset_values = []
all_wav_file_names = []  # this is a bit circular but I thought it is necessary to double check each step





# %%
wav_idx = 0
filename = wav_trials[wav_idx]
print(filename)
wav_directory = data_directory + 'tapping_experiment_' + block_id + '/participantid_' + participant_id + '/' + filename
unitdur_value = ahf.find_unitdur(filename)
print('unit duration is: ', unitdur_value)






# %%
# READ OUT THE SIGNAL
sample_rate, data = wavfile.read(wav_directory)
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
# # to simplify the matter take the absolute values of the signal values
# # this is just for plotting purposes
# only_positive_signal = np.abs(tapping_data)  # The first onset is the first location in samples, and it is used to perform the chunkwise
# ax = ahf.plot_signal_with_onsets(time_axis, only_positive_signal, actual_onsets, sample_rate)
# #ax.set_ylim([0, 0.001])
# plt.show()




# %%
# THRESHOLDING & REFRACTORY PERIOD
# inspect the data, set a threshold to y axis
# Add a green horizontal line at a specific y-value
tapping_threshold = 0.15 # THRESHOLD, the y-value where you want to draw the line
refractory_period = 0.2 # in seconds
refractory_period_samples = int(refractory_period * sample_rate)  # should be integer, otherwise find peak function raises an error
# ax.axhline(y=tapping_threshold, color='green', linestyle='-')
# Show the plot (if not already shown by plot_signal_with_onsets)
# plt.show()





# %%
# LOCATE THE ONSETS
tap_onset_points_in_time, tap_onset_points_in_signal = ahf.find_peaks(tapping_data, tapping_threshold, time_axis, refractory_period_samples)
ax = ahf.plot_signal_with_onsets(time_axis, tapping_data, actual_onsets, sample_rate)
ax.axhline(y=tapping_threshold, color='green', linestyle='-')
ax.plot(tap_onset_points_in_time, [tapping_data[i] for i in tap_onset_points_in_signal], '.', color='black', markersize=10)
#ax.set_ylim([0, 0.0009])
plt.show
print(len(tap_onset_points_in_signal))




# %%
all_tap_onset_points_in_time.append(tap_onset_points_in_time)
all_tap_onset_points_in_signal.append(tap_onset_points_in_signal)
all_unit_dur_values.append(unitdur_value)
all_actual_onset_values.append(actual_onsets)

wav_name = filename.split('/')[-1]
all_wav_file_names.append(wav_name)






# %%
data_mark =  participant_id + '_' + block_id + '_'


all_peak_points_in_signal_df = from_list_to_df(all_tap_onset_points_in_signal)
all_peak_points_in_signal_df.to_csv(clean_data_path + data_mark + 'all_tap_onset_points_in_signal.tsv', sep='\t', index=False)

all_peak_points_in_time_df = from_list_to_df(all_tap_onset_points_in_time)
all_peak_points_in_time_df.to_csv(clean_data_path + data_mark + 'all_tap_onset_points_in_time.tsv', sep='\t', index=False)

all_actual_onset_values_df = from_list_to_df(all_actual_onset_values)
all_actual_onset_values_df.to_csv(clean_data_path + data_mark + 'all_actual_onset_values.tsv', sep='\t', index=False)


all_unit_dur_values_df = from_list_to_df(all_unit_dur_values)
all_unit_dur_values_df.to_csv(clean_data_path + data_mark + 'all_unit_dur_values.tsv', sep='\t', index=False)

all_wav_file_names_df = from_list_to_df(all_wav_file_names)
all_wav_file_names_df.to_csv(clean_data_path + data_mark + 'all_wav_file_names.tsv', sep='\t', index=False)
# %%
