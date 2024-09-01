from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from scipy.signal import butter, filtfilt, find_peaks

# step size is there to cut off high frequency oscillations
def find_peaks(signal, threshold, time, step_size):
    time = time.flatten()  
    peak_points_in_time = []
    peak_points_in_signal = []
    i = 1
    while i in range(1, len(signal)-1):
        if signal[i] >= max(threshold, signal[i-1], signal[i+1]):
            peak_points_in_signal.append(i)
            peak_points_in_time.append(time[i])
            i = i + step_size
        else:
            i = i + 1

    return peak_points_in_time, peak_points_in_signal



def plot_audio_with_peaks(signal, time, peak_points_in_time, peak_points_in_signal):
    plt.figure(figsize=(10, 4))
    plt.plot(time, signal, color='b')
    plt.plot(peak_points_in_time, signal[peak_points_in_signal], 'x', color='r', markersize=10)  # Plot peaks
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Audio Signal with Peaks')
    plt.grid(False)
    plt.show()


def find_unitdur(filename):

    # Use a regular expression to find the value after 'unitdur_'
    match = re.search(r'unitdur_(\d+(\.\d+)?)', filename)
    if match:
        unitdur_value = float(match.group(1))  # Convert to float first, then to integer
        # print(unitdur_value)
    else:
        print("Unit duration not found in the file path.")
    return unitdur_value


def get_wav_file(data_directory, block_idx, participant_idx, wav_idx):
    # what is in the data directory
    items = os.listdir(data_directory)
    block_list = [item for item in items if item != '.DS_Store']
    # choose one block
    # later I will put a for loop here
    which_block = block_list[block_idx]
    block_directory = os.path.join(data_directory, which_block)
    items_b = os.listdir(block_directory)
    participant_list = [item for item in items_b if 'participant' in item]
    # there will be a for loop here
    which_participant = participant_list[participant_idx]
    participant_directory = os.path.join(block_directory, which_participant)
    # List all files ending with .wav
    wav_files = [file for file in os.listdir(participant_directory) if file.endswith('.wav')]
    filename = os.path.join(participant_directory, wav_files[wav_idx])
    return filename, which_block, which_participant


def find_zeropad_transitions(sound_data, zp_threshold, sample_rate):
    # to find the transition point from zero energy to an actual signal
    # reshape the signal to a 1D array if needed
    signal = sound_data.flatten()
    # Find the indices where the absolute value of the signal exceeds the threshold
    non_zero_indices = np.where(np.abs(signal) > zp_threshold)[0]
    # Locate the first and last non-zero indices
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    # Convert to time (in seconds) using the sampling rate
    start_time = start_index / sample_rate
    end_time = end_index / sample_rate

    return start_index, end_index, start_time, end_time


def plot_sound_onset_offset_marker(time_axis, signal, start_time, end_time):

    plt.figure(figsize=(12, 6))
    plt.plot(time_axis, signal, label='Sound Signal')
    plt.axvline(x=start_time, color='g', linestyle='--', label='Start of Signal')
    plt.axvline(x=end_time, color='r', linestyle='--', label='End of Signal')
    plt.xlabel('Signal duration in seconds')
    plt.ylabel('Amplitude')
    plt.title('Sound Signal with Start and End Markers')
    plt.legend()
    plt.show()


def extract_onsets(signal, start_index, end_index, unitdur_value, sample_rate, onset_threshold):

    # filter the signal, remove zero pads
    signal_segment = signal[start_index:end_index + 1]
    # Compute the short-term energy
    frame_size = int(unitdur_value * sample_rate)  # frame size changes wrt the unitdur
    energy = np.array([np.sum(signal_segment[i:i+frame_size]**2) for i in range(0, len(signal_segment), frame_size)])
    # Detect onsets based on energy threshold
    threshold = onset_threshold * np.max(energy)  # Set a threshold (can be adjusted)
    onsets = np.where(energy > threshold)[0] * frame_size

    # Filter out onsets that are too close to each other (within 0.1 seconds)
    min_distance = int(0.1 * sample_rate)
    filtered_onsets = [onsets[0]]
    for onset in onsets[1:]:
        if onset - filtered_onsets[-1] > min_distance:
            filtered_onsets.append(onset)

    onsets_full_signal = filtered_onsets + start_index

    return onsets_full_signal


def plot_signal_with_onsets(time_axis, signal, onsets, sample_rate):
    
    # Create a new figure and axes
    fig, ax = plt.subplots()
    
    # Plot the signal
    ax.plot(time_axis, signal, label='Signal')
    
    # Plot the onsets
    for onset in onsets:
        ax.axvline(x=onset/sample_rate, color='red', linestyle='--', label='Onset')

    # Additional plot customization (e.g., labels, title, etc.)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Signal with Onsets')
    
    # Display legend
    # ax.legend()

    # Return the axes object
    # # Plot the signal with detected onsets
    # plt.figure(figsize=(12, 6))
    # plt.plot(time_axis, signal, label='Signal')

    # # Plot red lines for each detected onset
    # for onset in onsets:
    #     plt.axvline(x=onset/sample_rate, color='r', linestyle='--', label='Onset' if onset == onsets[0] else "")

    # # Add labels and title
    # plt.xlabel('Signal duration in seconds')
    # plt.ylabel('Amplitude')
    # plt.title('Signal with onset markers')
    # plt.legend()
    # plt.show()
    
    return ax
    



# Low-Pass Filter Design
# I don't know whether I will use it or not but let the function stay there
def low_pass_filter(data, cutoff_freq, sample_rate, order=4):
    nyquist_freq = 0.5 * sample_rate  # Nyquist frequency
    normalized_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(order, normalized_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data



def plot_audio_with_peaks(signal, time, peak_points_in_time, peak_points_in_signal, onsets, sample_rate):
    
    # plt.figure(figsize=(12, 6))
    plt.plot(time, signal, color='b')
    plt.plot(peak_points_in_time, signal[peak_points_in_signal], 'x', color='r', markersize=10)  # Plot peaks
    
    # Plot red lines for each detected onset
    for onset in onsets:
        plt.axvline(x=onset/sample_rate, color='r', linestyle='--', label='Onset' if onset == onsets[0] else "")

    # Add labels and title
    plt.xlabel('Signal duration in seconds')
    plt.ylabel('Amplitude')
    plt.title('Signal with onset markers and peak points')
    plt.legend()
    plt.grid(False)
    plt.show()


