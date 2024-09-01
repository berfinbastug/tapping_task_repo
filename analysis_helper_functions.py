import numpy as np
from math import pi


def tap_onset_deviation_ms(trial_tap_onset_values, trial_actual_onset_values, fs):

    # Remove NaN values
    cleaned_tap_onsets = trial_tap_onset_values[~np.isnan(trial_tap_onset_values)]   
    n_tap = len(cleaned_tap_onsets)
    # Find the index of the closest smaller value in actual_onset_time_points for each element in rt_array_trial_1
    closest_indices = np.searchsorted(trial_actual_onset_values, cleaned_tap_onsets, side='right') - 1
    # I am doing this because there might be cases where the ntap is lower than nrep. 
    # but the code above makes them equal length. I am cutting the closest indices with respect to the
    # actual number of taps
    cut_closest_indices = closest_indices[:n_tap]
    # Identify repeated indices and store them
    # i don't know what to do with them for now (16.04.2024)
    unique_elements, counts = np.unique(cut_closest_indices, return_counts=True)
    repeated_elements = unique_elements[counts > 1]
    # Subtract tapping points from the closest smaller value in actual_onset_time_points
    result_array = cleaned_tap_onsets - trial_actual_onset_values[cut_closest_indices]
    result_array_msecs = result_array/fs

    return result_array_msecs, n_tap



def obtain_tapping_vectors(result_array_msecs, trial_unit_dur_value):
    # transform them to vectors
    # Subtract elements and handle remaining last elements

    tapping_phases = (result_array_msecs/trial_unit_dur_value) * 2*pi
    tapping_vectors = np.exp( 1j * tapping_phases )

    return tapping_vectors
