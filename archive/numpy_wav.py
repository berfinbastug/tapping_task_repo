import numpy as np
from scipy.io import wavfile
#=====================
#SAVE NUMPY FILE AS WAV FILE
#====================
def save_numpy_as_wav(filepath, current_audio_data, itrial, experiment_mark, unitdur, percentage, which_block, fs):
    sound_name = '/itrial_' + str(itrial) + '_unitdur_' + str(unitdur) + '_percentage_' + str(percentage) + '_block_' + str(which_block) + '_' + experiment_mark
    stim_directory = filepath + sound_name
    wavfile.write(stim_directory, fs, current_audio_data)
    return sound_name