from psychtoolbox import WaitSecs, GetSecs
from psychopy import visual, core
import os.path as op
import os
import numpy as np
import soundfile as sf
from datetime import datetime
from scipy.io import wavfile


#=====================
#GET DATE TIME AS STRING
#=====================
def get_datetime_string():
    now = datetime.now()
    return now.strftime("%Y%m%d_%H%M%S"), now.strftime("%Y%m%d")



#=====================
#SET UP AUDIO
#====================
# The setup_audio_files function preloads and processes a list of audio files, 
# ensuring they have a consistent sampling rate and number of channels. 
# The audio data is scaled by a specified RMS value and stored in a dictionary for later use, along with the sampling rate and channel information.
def setup_audio_files(sound_filenames, stim_for_block, params):

    # Preload stimuli from wav-file
    stimuli = {}
    # filenames = stimulus_filenames+feedback_filenames
    fs = channels = None
    stim_rms = params.stimulus_rms

    for filename in sound_filenames:
        
        # Construct the full filepath for the current sound file
        filepath = op.join(stim_for_block, filename)

        if len(filename) == 0:
            continue

        # Read the sound file using the soundfile library (sf)
        y, fs_file = sf.read(filepath)
        
        # Determine the number of channels in the sound file
        channels_file = 1 * (y.ndim < 2) or y.shape[1]
				
        # Update the global sampling rate (fs) and channels based on the current sound file
        if fs is None:
            fs = fs_file
            channels = channels_file
				
        # Check that the global sampling rate and channels match the current sound file
        assert (fs == fs_file)
        assert (channels == channels_file)
				
        # Add the sound data multiplied by the stimulus RMS to the stimuli dictionary
        stimuli[filename] = y*stim_rms

    return stimuli, channels, fs


#=====================
#DISPLAY INSTRUCTION
#====================
# The function displays a string of text both on a PsychoPy window (if provided) and in the console. 
# It then returns the time at which the text was displayed. 
# The function uses PsychoPy's visual.TextStim to handle the graphical display of the text.
def display_instruction(string, win):
    if win is not None:
        text = visual.TextStim(
            win, text=string
        )
        text.draw()
        win.flip()
    print(string)
    t_instruction = GetSecs()
    return t_instruction



#=====================
#SHORTER VERSION OF PARSE RESPONSE
#====================
def get_key_values_when_response(keys):

    reaction_time = keys[0].rt
    name = keys[0].name
    tDown = keys[0].tDown
    button_press_duration = keys[0].duration
    return reaction_time, name, tDown, button_press_duration


def get_key_values_when_noresponse(max_wait_time):

    reaction_time = max_wait_time
    name = 'no_response'
    tDown = 0
    button_press_duration = 0
    return reaction_time, name, tDown, button_press_duration



#=====================
#SAVE OUPUT, NAME LIST OF THE WAV FILES THAT STORE THE TAPPING INFORMATION
#====================
def save_output(file_path, output, participant_id, which_block):
    filename = 'tapping_experiment_wav_names_list_pid_' + str(participant_id) + '_block_' + str(which_block) + '.tsv'
    output_data_directory = file_path + '/' + filename
    output.to_csv(output_data_directory, sep='\t', index=False)



#=====================
#CREATE A NEW FOLDER FOR EACH PARTICIPANT INSIDE THE BLOCK SPECIFIC DATA FOLDER
#====================
def create_a_new_folder_for_participants(data_dir, which_block, participant_id):
    file_path = data_dir + '/tapping_experiment_block' + str(which_block) + '/participantid_' + str(participant_id)
    os.makedirs(file_path, exist_ok=True)
    return file_path


#=====================
#SAVE NUMPY FILE AS WAV FILE
#====================
def save_numpy_as_wav(filepath, current_audio_data, itrial, experiment_mark, unitdur, percentage, which_block, fs):
    sound_name = '/itrial_' + str(itrial) + '_unitdur_' + str(unitdur) + '_percentage_' + str(percentage) + '_block_' + str(which_block) + '_' + experiment_mark
    stim_directory = filepath + sound_name
    wavfile.write(stim_directory, fs, current_audio_data)
    return sound_name