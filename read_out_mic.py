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

pid = 10
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


# plot actual signal
fs, actual_audio = wavfile.read(actual_signal)
time_axis_a = np.linspace(0, len(actual_audio) / fs, num=len(actual_audio))
plt.plot(time_axis_a, actual_audio, label='Mono Channel')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Audio Signal')