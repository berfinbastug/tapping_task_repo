import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

#=====================
#DEFINE DIRECTORIES
#=====================
# when I switch to a new computer, just change the main_dir
main_dir = '/home/bastugb/Documents/tapping_experiment'
data_dir = main_dir + '/data'

# this part is temporary
which_block = 1
specific_block = f'tapping_experiment_block{which_block}'
block_dir = data_dir + '/' + specific_block

pid = 668
wav_directory = block_dir + '/participantid_' + str(pid)
files_in_wavdirectory = os.listdir(wav_directory)
wav_list  = [file for file in files_in_wavdirectory if file.endswith('.wav')]

# Read the WAV file
example_wav = wav_directory + '/' + wav_list[0]

# find out the actual data
# actual_signal = '/home/bastugb/Documents/tapping_experiment/stimuli/tapping_experiment_block1/tapping_experiment_index_6_unitdur_0.4_percentage_0.6666666666666666.wav'
fs, mic_signal = wavfile.read(example_wav)

# Generate time axis
time_axis = np.linspace(0, len(mic_signal) / fs, num=len(mic_signal))


# Plot the audio signal
plt.figure(figsize=(15, 5))
if len(mic_signal.shape) == 2:
    plt.subplot(2, 1, 1)
    plt.plot(time_axis, mic_signal[:, 0], label='Left Channel')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Left Channel')

    plt.subplot(2, 1, 2)
    plt.plot(time_axis, mic_signal[:, 1], label='Right Channel')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Right Channel')
else:
    plt.plot(time_axis, mic_signal, label='Mono Channel')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Audio Signal')
plt.tight_layout()
plt.show()


# %%

sound_data_index = 0
tapping_data_index = 1
sample_rate = 44100

sound_data = mic_signal[:,sound_data_index]
tapping_data = mic_signal[:, tapping_data_index]
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
unitdur_value = 1
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




import cleaning_analysis_helper_functions as ahf


time = time_axis.flatten()
peak_points_in_time = []
peak_points_in_signal = []
i = 1
threshold = 0.1
step_size = int(0.2 * 44100)
signal = tapping_data

while i in range(1, len(signal)-1):
    if signal[i] >= threshold:
        print(signal[i])
        peak_points_in_signal.append(i)
        peak_points_in_time.append(time[i])
        i = i + step_size

    else:
        i = i + 1


ax = ahf.plot_signal_with_onsets(time_axis, tapping_data, actual_onsets, sample_rate)
ax.axhline(y=threshold, color='green', linestyle='-')
ax.plot(peak_points_in_time, [tapping_data[i] for i in peak_points_in_signal], '.', color='black', markersize=10)
#ax.set_ylim([0, 0.0009])
plt.show
