from psychtoolbox import WaitSecs, GetSecs
from psychopy import visual
import os.path as op
import soundfile as sf
from datetime import datetime


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
def display_text(string, win):
    if win is not None:
        text = visual.TextStim(
            win, 
            text=string,
            height = 1.2,
            alignText = 'center',
            wrapWidth = 40.0
        )
        text.draw()
        win.flip()
    print(string)
    t_text = GetSecs()
    return t_text

