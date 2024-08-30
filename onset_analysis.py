# in the future, make this code more pretty.
# 17.04.2024
import os
import pandas as pd
import numpy as np
import analysis_related_functions as arf
import matplotlib.pyplot as plt
import seaborn as sns

# DEFINE DIRECTORIES
main_directory = '/Users/bastugb/Desktop/tapping_experiment_v4/'
plot_directory = main_directory + 'plots/'
data_directory = main_directory + 'data/combined_data/'
tapping_vectors_name =  data_directory + 'combined_tapping_vectors_across_blocks_across_participants.tsv'
stim_info_name = data_directory + 'combined_stimulus_info_across_blocks_across_participants.tsv'
tapping_points_name = data_directory + 'combined_tapping_points_wrt_actual_onset_across_blocks_across_participants.tsv'

# READ THE DATA FRAMES
tapping_vectors = pd.read_csv(tapping_vectors_name, delimiter = '\t', index_col = 0)
tapping_points = pd.read_csv(tapping_points_name, delimiter = '\t', index_col = 0)
stim_info = pd.read_csv(stim_info_name, delimiter = '\t', index_col = 0)

# i guess i won't use tapping vectors here, because i can't
# not NaN function of numpy doesn't work with complex numbers
zeropad_duration = 0.4
nrep = 30

vector_mean_list = []
vector_std_list = []

for trial_idx in range(len(tapping_points)):

    trial_info = stim_info.iloc[trial_idx]
    stream_duration = trial_info['stream_durations']
    unit_duration = (stream_duration - zeropad_duration)/nrep
    
    time_info = tapping_points.iloc[trial_idx]
    time_info_np = time_info.values
    cleaned_time_info_np = time_info_np[~np.isnan(time_info_np)] 
    vectors = arf.get_tapping_vectors(cleaned_time_info_np, unit_duration)

    if len(vectors) > 0:
    #     # my_circ_mean = pycircstat.descriptive.mean(tapping_vectors)
        vector_mean = abs(vectors.mean())
        vector_std = abs(vectors.std())
    else:
        vector_mean = 0
        vector_std = 0

    vector_mean_list.append(vector_mean)
    vector_std_list.append(vector_std)


# Adding the list as a new column
stim_info['vector_mean'] = vector_mean_list
stim_info['vector_std'] = vector_std_list

# %%
##### FIRST GROUP BY PARTICIPANT & UNIT DURATION #####
grouped = stim_info.groupby(['pid', 'unit_durations'])

# access specific group data
which_pid = 8
which_unitdur = 1
specific_data = grouped.get_group((which_pid, which_unitdur))

mean_values_vector = specific_data.groupby('percentages')['vector_mean'].mean()
mean_values_ntaps = specific_data.groupby('percentages')['n_taps'].mean()

# %%
# PLOTTING #
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns

# Plotting vector mean on the first subplot
ax1.plot(mean_values_vector.index, mean_values_vector.values, marker='o', linestyle='-')
ax1.set_xticks(mean_values_vector.index)  # Setting custom x-axis ticks
ax1.set_title('Mean Vector Mean by Percentages')
ax1.set_xlabel('Percentages')
ax1.set_ylabel('Vector Mean')
ax1.grid(True)

# Plotting number of taps on the second subplot
ax2.plot(mean_values_ntaps.index, mean_values_ntaps.values, marker='o', linestyle='-', color = 'red')
ax2.set_title('Mean Number of Taps by Percentages')
ax2.set_xticks(mean_values_ntaps.index)
ax2.set_xlabel('Percentages')
ax2.set_ylabel('Number of Taps')
ax2.grid(True)

sup_title_name = 'participant id: ' + str(which_pid) + ', unit duration: ' + str(which_unitdur)
fig.suptitle(sup_title_name, fontsize=16)

plt.tight_layout()
plt.show()


# %%
##### NOW GROUP BY UNIT DURATION ONLY #####
grouped = stim_info.groupby(['unit_durations'])
specific_data = grouped.get_group(which_unitdur)


which_unitdur = 1
specific_data = grouped.get_group((which_pid, which_unitdur))

mean_values_vector = specific_data.groupby('percentages')['vector_mean'].mean()
mean_values_ntaps = specific_data.groupby('percentages')['n_taps'].mean()

# PLOTTING #
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns

# Plotting vector mean on the first subplot
ax1.plot(mean_values_vector.index, mean_values_vector.values, marker='o', linestyle='-')
ax1.set_xticks(mean_values_vector.index)  # Setting custom x-axis ticks
ax1.set_title('Mean Vector Mean by Percentages')
ax1.set_xlabel('Percentages')
ax1.set_ylabel('Vector Mean')
ax1.grid(True)

# Plotting number of taps on the second subplot
ax2.plot(mean_values_ntaps.index, mean_values_ntaps.values, marker='o', linestyle='-', color = 'red')
ax2.set_title('Mean Number of Taps by Percentages')
ax2.set_xticks(mean_values_ntaps.index)
ax2.set_xlabel('Percentages')
ax2.set_ylabel('Number of Taps')
ax2.grid(True)

sup_title_name = 'unit duration: ' + str(which_unitdur)
fig.suptitle(sup_title_name, fontsize=16)

plt.tight_layout()
plt.show()



# NOW PLOT A HEATMAP
# for this I need a matrix
# Initialize an empty list to hold the series

list_mean_vector = []
list_mean_ntaps = []
unit_duration_list = []

# Loop to obtain the mean vector and mean number of taps
for i in stim_info['unit_durations'].unique():  # Adjust range if more series are needed

    which_unitdur = i

    unit_duration_list.append(i)
    grouped = stim_info.groupby(['unit_durations'])
    specific_data = grouped.get_group(which_unitdur)

    mean_values_vector = specific_data.groupby('percentages')['vector_mean'].mean()
    mean_values_ntaps = specific_data.groupby('percentages')['n_taps'].mean()

    list_mean_vector.append(mean_values_vector)
    list_mean_ntaps.append(mean_values_ntaps)


matrix_vector_mean = pd.DataFrame(list_mean_vector, index = unit_duration_list)
matrix_vector_mean.sort_index(inplace=True)

matrix_ntap = pd.DataFrame(list_mean_ntaps, index = unit_duration_list)
matrix_ntap.sort_index(inplace=True)
# vector_means_np = matrix_vector_mean.values
# percentages = list(matrix_vector_mean.columns)

ax = sns.heatmap(matrix_ntap, cmap='viridis', annot=False, fmt=".2f",
        xticklabels=matrix_ntap.columns,
        yticklabels=matrix_ntap.index)

plt.xlabel('Percentage of the repeating tones')
plt.ylabel('Unit Duration')
plt.title('Heatmap of the mean number of taps')
# Adjust layout to show labels clearlyß
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability if needed
plt.yticks(rotation=0)  # Ensure y-axis labels are horizontal
ax.invert_yaxis()
plt.show()


