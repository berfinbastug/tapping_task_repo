# %%
import os
import pandas as pd
import numpy as np
import analysis_helper_functions as hf
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
import tapping_data_plotting_functions as plot_f


# DEFINE DIRECTORIES
main_directory = '/Users/bastugb/Desktop/tapping_experiment/'
cleaned_data_directory = main_directory + 'clean_data/'


# %%
# here, we have all kinds of tsv files 
items = os.listdir(cleaned_data_directory)

# i need these tsv files in an organized way
# things to be read
# a) all actual onset values
# b) all tap onset points in signal
# c) all unit dur values
# d) wav file names

# subset these tsv files according to their categories
actual_onset_values = [item for item in items if 'all_actual_onset_values' in item]
tap_onset_signals = [item for item in items if 'tap_onset_points_in_signal' in item]
unit_dur_values = [item for item in items if 'unit_dur_values' in item]
wav_file_names = [item for item in items if 'wav_file_names' in item]

# sort these file names because they dont match
actual_onset_values_sorted = sorted(actual_onset_values)
tap_onset_signals_sorted = sorted(tap_onset_signals)
unit_dur_values_sorted = sorted(unit_dur_values)
wav_file_names_sorted = sorted(wav_file_names)


fs = 44100  # sampling rate of the data


# %%
# later add a for loop here
# read the onset signals one by one
block_idx = 0
tmp_actual_onset_values = actual_onset_values_sorted[block_idx]
tmp_tap_onset_signals = tap_onset_signals_sorted[block_idx]
tmp_unit_dur_values = unit_dur_values_sorted[block_idx]
tmp_wav_file_names = wav_file_names_sorted[block_idx]

actual_onset_values_df = pd.read_csv((cleaned_data_directory + tmp_actual_onset_values), delimiter= '\t')
tap_onset_signals_df = pd.read_csv((cleaned_data_directory + tmp_tap_onset_signals), delimiter= '\t')
unit_dur_values_df = pd.read_csv((cleaned_data_directory + tmp_unit_dur_values), delimiter= '\t')
wav_file_names_df = pd.read_csv((cleaned_data_directory + tmp_wav_file_names), delimiter= '\t')


# %%
all_tap_onset_deviations = []
all_tapping_vectors = []

for i in range(len(actual_onset_values_df)):

    # then another for loop here
    trial_idx = i
    trial_unit_dur_value = unit_dur_values_df.iloc[trial_idx].values[0]

    # the tapping points are rows of a data frame
    # convert them to a numpy array
    trial_actual_onset_values = actual_onset_values_df.iloc[trial_idx].values
    trial_tap_onset_values  = tap_onset_signals_df.iloc[trial_idx].values

    result_array_msecs, n_tap = hf.tap_onset_deviation_ms(trial_tap_onset_values, trial_actual_onset_values, fs)
    tapping_vectors = hf.obtain_tapping_vectors(result_array_msecs, trial_unit_dur_value)
    
    all_tap_onset_deviations.append(result_array_msecs)
    all_tapping_vectors.append(tapping_vectors)



# %%
for trial_idx in range(len(all_tapping_vectors)):

    trial_wav_file_name = wav_file_names_df.iloc[trial_idx].values[0]
    result_array_msecs = all_tap_onset_deviations[trial_idx]
    trial_unit_dur_value = unit_dur_values_df.iloc[trial_idx].values[0]
    plot_f.plot_vertical_lines_tapping(result_array_msecs, trial_wav_file_name)

# %%
plot_f.circular_plot_tapping_vectors(tapping_vectors, trial_wav_file_name)
plot_f.plot_vertical_lines_tapping(result_array_msecs, trial_wav_file_name)

# %%

# %%
