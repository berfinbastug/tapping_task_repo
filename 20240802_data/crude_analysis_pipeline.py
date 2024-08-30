import os
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np

dir_example = '/Users/bastugb/Desktop/tapping_experiment/20240802_data/data/tapping_experiment_block1/participantid_3'

# List all files ending with .wav
wav_files = [file for file in os.listdir(dir_example) if file.endswith('.wav')]

# Function to plot two channels of a wav file
def plot_wav_channels(filename):

    
    # Read the wav file
    sample_rate, data = wavfile.read(filename)
    
    # Check if the data is stereo (2 channels)
    if len(data.shape) < 2 or data.shape[1] != 2:
        print(f"{filename} is not a stereo file.")
        return
    
    # Extract left and right channels
    channel_1 = data[:, 0]
    channel_2 = data[:, 1]
    
    # Time axis for plotting
    time_axis = np.linspace(0, len(channel_1) / sample_rate, num=len(channel_1))
    
    # Plot the two channels in separate subplots
    plt.figure(figsize=(12, 6))
    
    # Plot channel 1
    plt.subplot(2, 1, 1)
    plt.plot(time_axis, channel_1, color='blue')
    plt.title('Channel 1')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    
    # Plot channel 2
    plt.subplot(2, 1, 2)
    plt.plot(time_axis, channel_2, color='red')
    plt.title('Channel 2')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    
    plt.tight_layout()
    plt.show()


# Plot the first 30 .wav files, or less if there aren't 30 files
for wav_file in wav_files[:30]:
    filepath = os.path.join(dir_example, wav_file)
    print(f"Plotting {wav_file}")
    plot_wav_channels(filepath)   