# %%
import os
import pandas as pd
import numpy as np
import analysis_helper_functions as hf
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
import tapping_data_plotting_functions as plot_f
import scipy
import re

# DEFINE DIRECTORIES
main_directory = '/Users/bastugb/Desktop/tapping_experiment/'
cleaned_data_directory = main_directory + 'clean_data/'


# %%
# here, we have all kinds of tsv files 
items = os.listdir(cleaned_data_directory)

# at first participant level filtering
tmp_pid = [item for item in items if 'participantid_1' in item]
# i need these tsv files in an organized way
# things to be read
# a) all actual onset values
# b) all tap onset points in signal
# c) all unit dur values
# d) wav file names

# subset these tsv files according to their categories
actual_onset_values = [item for item in tmp_pid if 'all_actual_onset_values' in item]
tap_onset_signals = [item for item in tmp_pid if 'tap_onset_points_in_signal' in item]
unit_dur_values = [item for item in tmp_pid if 'unit_dur_values' in item]
wav_file_names = [item for item in tmp_pid if 'wav_file_names' in item]

# sort these file names because they dont match
actual_onset_values_sorted = sorted(actual_onset_values)
tap_onset_signals_sorted = sorted(tap_onset_signals)
unit_dur_values_sorted = sorted(unit_dur_values)
wav_file_names_sorted = sorted(wav_file_names)


fs = 44100  # sampling rate of the data


# %%
# obtain TAP STIMULUS ALIGNMENTS
n_total_block = 7

all_tap_stimulus_alignments = []  # across all blocks and participants and trials
all_n_taps = []
all_tapping_vectors = []
all_tapping_phases = []

all_wav_names = pd.DataFrame() 

for block_idx in range(n_total_block):

    tmp_actual_onset_values = actual_onset_values_sorted[block_idx]
    actual_onset_values_df = pd.read_csv((cleaned_data_directory + tmp_actual_onset_values), delimiter= '\t')

    tmp_tap_onset_signals = tap_onset_signals_sorted[block_idx]
    tap_onset_signals_df = pd.read_csv((cleaned_data_directory + tmp_tap_onset_signals), delimiter= '\t')
    
    tmp_wav_file_names = wav_file_names_sorted[block_idx]
    wav_file_names_df = pd.read_csv((cleaned_data_directory + tmp_wav_file_names), delimiter= '\t')

    all_wav_names = pd.concat([all_wav_names, wav_file_names_df], axis=0)

    tmp_unit_dur_values = unit_dur_values_sorted[block_idx]
    unit_dur_values_df = pd.read_csv((cleaned_data_directory + tmp_unit_dur_values), delimiter= '\t')
    
    for trial_idx in range(len(actual_onset_values_df)):

        # the tapping points are rows of a data frame
        # convert them to a numpy array
        trial_actual_onset_values = actual_onset_values_df.iloc[trial_idx].values
        trial_tap_onset_values  = tap_onset_signals_df.iloc[trial_idx].values

        result_array_msecs, n_tap = hf.tap_onset_deviation_ms(trial_tap_onset_values, trial_actual_onset_values, fs)
        
        all_tap_stimulus_alignments.append(result_array_msecs)
        all_n_taps.append(n_tap)

        trial_unit_dur_value = unit_dur_values_df.iloc[trial_idx].values[0]
        tapping_phases = (result_array_msecs/trial_unit_dur_value) * 2*pi 
        all_tapping_phases.append(tapping_phases)
        tapping_vectors = np.exp( 1j * tapping_phases ) 
        all_tapping_vectors.append(tapping_vectors)
        #print(wav_file_names_df.iloc[trial_idx].values[0])








#%%
all_csd = []
# for i in len(all_tapping_vectors):
unitdur_list = []
percentage_list = []
for i in range(len(all_tapping_vectors)):
    tapping_vectors = all_tapping_vectors[i]
    tapping_phases = all_tapping_phases[i]
    trial_wav_file_name = all_wav_names.iloc[i].values[0]
    #plot_f.circular_plot_tapping_vectors(tapping_vectors, trial_wav_file_name)
    #r = np.sum(tapping_vectors, axis=0)
    #print(np.angle(r))
    #print(scipy.stats.circmean(tapping_phases))
    #print(scipy.stats.circstd(tapping_phases))
    x = scipy.stats.circstd(tapping_phases)
    all_csd.append(x)
    # Lists to store the extracted values


    # Extract the value after 'unitdur'
    unitdur_match = re.search(r'unitdur_(\d+\.\d+)', trial_wav_file_name)
    if unitdur_match:
        unitdur_value = float(unitdur_match.group(1))
        #print(unitdur_value)
        unitdur_list.append(unitdur_value)

    # Extract the value after 'percentage'
    percentage_match = re.search(r'percentage_(\d+\.\d+)', trial_wav_file_name)
    if percentage_match:
        percentage_value = float(percentage_match.group(1))
        #print()
        percentage_list.append(percentage_value)
        
#%%
data = pd.DataFrame({
'Duration': unitdur_list,
'Percentage': percentage_list,
'Std_Dev': all_csd
})

# Pivot the data to get a 3x10 matrix
matrix = data.pivot_table(values='Std_Dev', index='Duration', columns='Percentage', aggfunc='mean')

# # Output the lists
# print("unitdur_list:", unitdur_list)
# print("percentage_list:", percentage_list)
# %%

import seaborn as sns
# Plot the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(matrix, annot=False, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Mean Std Dev'})
plt.title('Heatmap of Mean Standard Deviation by Duration and Percentage')
plt.xlabel('Percentage')
plt.ylabel('Duration')
plt.show()
# %%

# %%
from scipy.stats import circvar, circstd
from scipy.stats import circmean

for i in range(len(all_tapping_phases)):

    angles = all_tapping_phases[i]
    CM = circmean(angles)

    CSD = circstd(angles)

    plt.plot(np.cos(np.linspace(0, 2*np.pi, 500)),np.sin(np.linspace(0, 2*np.pi, 500)),c='k')  # this draws a circle
    plt.scatter(np.cos(angles), np.sin(angles), c='k')
    plt.scatter(np.cos(CM), np.sin(CM), c='b',label='circmean')
    #plt.scatter(np.cos(mean), np.sin(mean), c='r', label='mean')
    plt.title(f"circular standard deviation: {np.round(CSD, 2)!r}")
    plt.legend()
    plt.axis('equal')
    plt.show()

# %%
