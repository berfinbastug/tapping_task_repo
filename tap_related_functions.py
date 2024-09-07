import numpy as np

def find_tap_onset(sample_rate, refractory_period, threshold, tapping_data):
    """
    Detects tap onsets in the tapping signal based on a threshold and returns both the time
    and index of each onset event

    Parameters:
    -----------
    sample_rate:
    refractory period: how long should it take to detect the next onset? should be in seconds
    threshold: the lowest signal value to be considered as a tap
    tapping_data: data recorded from the microphone

    Returns:
    ----------
    onset_points_in_time: a list of time values where a tap onset is detected
    onset_points_in_signal: a list of indices in the signal where a tap onset is detected

    """

    # Flatten the time axis in case it's multi-dimensional (e.g., if it came from a 2D array).
    time_axis = np.linspace(0, len(tapping_data) / sample_rate, num=len(tapping_data))
    time = time_axis.flatten() 

    # initialize lists to store the onset points
    onset_points_in_time = []
    onset_points_in_signal = []


    step_size = int(refractory_period * sample_rate) # transform seconds to samples

    i = 1

    while i in range(1, len(tapping_data)-1):
        if tapping_data[i] >= threshold:
            
            onset_points_in_signal.append(i)
            onset_points_in_time.append(time[i])
            i = i + step_size

        else:
            i = i + 1

    return onset_points_in_time, onset_points_in_signal 



