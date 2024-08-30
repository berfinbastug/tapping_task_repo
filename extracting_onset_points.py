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
# TO STORE ITEMS
all_unit_dur_values = []
all_peak_points_in_time = []
all_peak_points_in_signal = []
all_actual_onset_values = []



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
block_idx = 0
participant_idx = 3



# %%
wav_idx = 0
filename, which_block, which_participant = ahf.get_wav_file(data_directory, block_idx, participant_idx, wav_idx)
print(filename)
print('participant_id: ', which_participant)
print('block_id: ', which_block)
unitdur_value = ahf.find_unitdur(filename)
print('unit duration is: ', unitdur_value)




# %%
# READ OUT THE SIGNAL
sample_rate, data = wavfile.read(filename)
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
# to simplify the matter remove the negative values and deal with positives only
only_positive_signal = np.abs(tapping_data)  # The first onset is the first location in samples, and it is used to perform the chunkwise
ax = ahf.plot_signal_with_onsets(time_axis, only_positive_signal, actual_onsets, sample_rate)
#ax.set_ylim([0, 0.001])
plt.show()




# %%
# THRESHOLDING & REFRACTORY PERIOD
# inspect the data, set a threshold to y axis
# Add a green horizontal line at a specific y-value
tapping_threshold = 0.0001 # THRESHOLD, the y-value where you want to draw the line
refractory_period = 0.2  # in seconds
refractory_period_samples = int(refractory_period * sample_rate)  # should be integer, otherwise find peak function raises an error
# ax.axhline(y=tapping_threshold, color='green', linestyle='-')
# Show the plot (if not already shown by plot_signal_with_onsets)
# plt.show()





# %%
# LOCATE THE ONSETS
peak_points_in_time, peak_points_in_signal = ahf.find_peaks(tapping_data, tapping_threshold, time_axis, refractory_period_samples)
ax = ahf.plot_signal_with_onsets(time_axis, only_positive_signal, actual_onsets, sample_rate)
ax.axhline(y=tapping_threshold, color='green', linestyle='-')
ax.plot(peak_points_in_time, [only_positive_signal[i] for i in peak_points_in_signal], '.', color='black', markersize=10)
#ax.set_ylim([0, 0.0009])
plt.show
print(len(peak_points_in_signal))




# %%
all_peak_points_in_time.append(peak_points_in_time)
all_peak_points_in_signal.append(peak_points_in_signal)
all_unit_dur_values.append(unitdur_value)
all_actual_onset_values.append(actual_onsets)







# %%
data_mark = which_participant + '_' + which_block + '_'


all_peak_points_in_signal_df = from_list_to_df(all_peak_points_in_signal)
all_peak_points_in_signal_df.to_csv(clean_data_path + data_mark + 'all_peak_points_in_signal.tsv', sep='\t', index=False)

all_peak_points_in_time_df = from_list_to_df(all_peak_points_in_time)
all_peak_points_in_time_df.to_csv(clean_data_path + data_mark + 'all_peak_points_in_time.tsv', sep='\t', index=False)

all_actual_onset_values_df = from_list_to_df(all_actual_onset_values)
all_actual_onset_values_df.to_csv(clean_data_path + data_mark + 'all_actual_onset_values.tsv', sep='\t', index=False)


all_unit_dur_values_df = from_list_to_df(all_unit_dur_values)
all_unit_dur_values_df.to_csv(clean_data_path + data_mark + 'all_unit_dur_values.tsv', sep='\t', index=False)

