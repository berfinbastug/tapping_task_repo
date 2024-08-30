# %%
import os
import pandas as pd
import numpy as np
import analysis_helper_functions as hf
import matplotlib.pyplot as plt
import seaborn as sns

# DEFINE DIRECTORIES
main_directory = '/Users/bastugb/Desktop/tapping_experiment/'
cleaned_data_directory = main_directory + 'clean_data/'


# %%
fs = 44100
items = os.listdir(cleaned_data_directory)
# things to be read
# a) all actual onset values
# b) 
onset_signals = [item for item in items if 'peak_points_in_signal' in item]
onset_signals_sorted = sorted(onset_signals)

actual_onset_signals = [item for item in items if 'actual_onset_values' in item]
actual_onset_signals_sorted = sorted(actual_onset_signals)
# %%
# read the onset signals one by one
o_idx = 0
which_onset_signals = onset_signals_sorted[o_idx]
onset_signals_df = pd.read_csv((cleaned_data_directory + which_onset_signals), delimiter= '\t')


which_actual_onset_signals = actual_onset_signals_sorted[o_idx]
actual_onset_signals_df = pd.read_csv((cleaned_data_directory + which_actual_onset_signals), delimiter = '\t')

trial_idx = 0

# the tapping points are rows of a data frame
# convert them to a numpy array
trial_tap_onset_vals = onset_signals_df.iloc[trial_idx].values
trial_actual_onset_vals = actual_onset_signals_df.iloc[trial_idx].values

# Remove NaN values
cleaned_tap_onset_vals = trial_tap_onset_vals[~np.isnan(trial_tap_onset_vals)]   
n_tap = len(cleaned_tap_onset_vals)

# Find the index of the closest smaller value in actual_onset_time_points for each element in rt_array_trial_1
closest_indices = np.searchsorted(trial_actual_onset_vals, cleaned_tap_onset_vals, side='right') - 1

  
# I am doing this because there might be cases where the ntap is lower than nrep. 
# but the code above makes them equal length. I am cutting the closest indices with respect to the
# actual number of taps
cut_closest_indices = closest_indices[:n_tap]

# Identify repeated indices and store them
# i don't know what to do with them for now (16.04.2024)
unique_elements, counts = np.unique(cut_closest_indices, return_counts=True)
repeated_elements = unique_elements[counts > 1]

# Subtract tapping points from the closest smaller value in actual_onset_time_points
result_array = cleaned_tap_onset_vals - trial_actual_onset_vals[cut_closest_indices]
result_array_msecs = result_array/fs

