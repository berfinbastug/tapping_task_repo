import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

#=====================
#DEFINE DIRECTORIES
#=====================
# when I switch to a new computer, just change the main_dir
main_dir = '/Users/bastugb/Desktop/tapping_experiment'
data_dir = main_dir + '/data'

# this part is temporary
which_block = 1
specific_block = f'tapping_experiment_block{which_block}'
block_dir = data_dir + '/' + specific_block

pid = 0
wav_directory = block_dir + '/participantid_' + str(pid)
files_in_wavdirectory = os.listdir(wav_directory)
wav_list  = [file for file in files_in_wavdirectory if file.endswith('.wav')]

# Read the WAV file
example_wav = wav_directory + '/' + wav_list[0]
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