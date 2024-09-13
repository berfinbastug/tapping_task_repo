#=====================
# ESTABLISH THE WORKING ENVIRONMENT
#=====================
import sys
default_path = '/home/bastugb/Documents/tapping_experiment'
sys.path.append(default_path)

import pandas as pd
import numpy as np
import os
from psychtoolbox import WaitSecs, GetSecs
from psychopy import core, gui, visual
from psychopy.hardware import keyboard
from psychtoolbox import audio, PsychPortAudio
from scipy.io import wavfile
import matplotlib.pyplot as plt

import run_experiment_functions as ef
import data_frame_functions as dff
import experiment_params as params



#=====================
#DEFINE DIRECTORIES
#=====================
# when I switch to a new computer, just change the main_dir
# main_dir = '/Users/bastugb/Desktop/tapping_experiment/training'
main_dir = '/home/bastugb/Documents/tapping_experiment/training'
stimuli_dir = main_dir + '/stimuli_training'
data_dir = main_dir + '/data_training'
table_dir = main_dir + '/tables_training'



#=====================
#COLLECT PARTICIPANT INFO
#=====================
#-create a dialogue box for participant information
exp_info = {'participant_id':0, 'age':0, 'handedness':('right','left','ambi')}
my_dlg = gui.DlgFromDict(dictionary=exp_info)

# # check for valid participant data, make sure subject data is entered correctly
if exp_info['participant_id'] ==0: # nothing entered
    err_dlg = gui.Dlg(title='error message') #give the dlg a title
    err_dlg.addText('Enter a valid subject number!') #create an error message
    err_dlg.show() #show the dlg
    core.quit() #quit the experiment
    
# get date and time
time_stamp = ef.get_datetime_string()[0]
exp_info['time'] = time_stamp

# create a unique filename for the data
# don't forget to turn integers into strings for the filename, don't forget to add the filetype at the end: csv, txt...
experiment_mark = 'tapping_training_toneclouds_pid' + str(exp_info['participant_id']) + '_' + exp_info['time'] + '.wav'



#=====================
#READ THE TRAINING DATA FRAME 
#=====================
table_name = f'tapping_training_block_0_table.tsv'
df, nTrials = dff.get_df(table_name, table_dir)



#=====================
#PRELOAD STIMULUI
#=====================
# list the sound filenames, in a randomized way
sound_filenames = df['stim_name'].to_list()
# this directory is necessary while reading from wav-files

# define stimuli, which is stream in my case
# setup audio stream 
stimuli, channels, fs = ef.setup_audio_files(sound_filenames, stimuli_dir, params)

device_ids = [i_device for i_device, device in enumerate(audio.get_devices()) if params.device_name in device['DeviceName']]
for i_device, device in enumerate(audio.get_devices()):
    if params.device_name in device['DeviceName']:
        print(device['DeviceName'])

assert (len(device_ids) == 1)
params.device_id = device_ids[0]
# print(audio.get_devices())



#=====================
#DEFINE STIMULI (STREAM)
#=====================
# Initialize an audio stream with the global sampling rate and channels
# channels = [channels, 2], here 2 corresponds to the channel of the output (microphone and the looped audio signal)
# the first channels value, which is 1, correspond to the input of the channel, which is the sent audio signal
stream = [audio.Stream(freq=fs, device_id = params.device_id, mode = 3, latency_class = 3, channels=[channels, 2])]

#=============
# THIS PART IS CRUCIAL
# now something like this is necessary I think 
# to record the audio from the microphone people tap
stream[0].get_audio_data(secs_allocate = 1000)
#=============

# play empty sound at first
# Create an empty stimulus buffer with 0.1 seconds duration
stimulus = np.zeros((int(fs*.1), channels))

# Fill the buffer for each slave in the audio stream and start playback
for slave in stream:
    PsychPortAudio('FillBuffer', slave.handle, stimulus)
    PsychPortAudio('Start', slave.handle)

# stream is ready now
stream[0].stimuli = stimuli



#=====================
#SET UP THE SYSTEM 
#=====================
# prepare keyboard
kb = keyboard.Keyboard()  # to handle input from keyboard (supersedes event.getKeys())
# create response time clock, to be honest, I am not sure whether I am using this one currently?
timer = core.Clock()

# define the window (size, color, units, fullscreen mode) 
# screen = 1, shows the display window in the booth
# screen = 0, shows the display window in the control room
win = visual.Window([1920, 1080], fullscr=True, monitor="testMonitor", units="cm", screen = 1)



#=====================
#INSTRUCTIONS
#=====================
experiment_start_text = ("Welcome to our experiment. This is a training session.\n"
                         "Please carefully read the following instructions.\n"
                         "\n"
                         "\n"
                         "You can now put on your headphones and proceed with the detailed instructions regarding the experimental procedure. ")

ef.display_text(experiment_start_text, win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

training_instructions = ("During the experiment, you will hear long sequences of noise-like sounds."
                        "Your task is to tap your finger on the attached microphone as soon as you hear the sound and keep tapping until the end of the sound sequence. " 
                        "Some of these sound sequences contain repeating patterns that form a distinct beat. Try to detect these repeating patterns and tap in synchrony with each cycle of repetition. " 
                        "This means aligning each tap with each cycle of the repeating pattern and tapping at the same speed as the repeating pattern. \n" 
                        "The repeating patterns will be present in some trials, sometimes obvious and sometimes not. In any case, try your best to detect the repetitions and tap in sync with them. " 
                        "If you do not detect any repeating pattern, just continuously tap your finger with any rhythm or speed you wish, as long as it is at a regular interval.\n"
                        "\n"
                        "Press any button to continue.")

ef.display_text(training_instructions, win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)



#=====================
#FASTEST SPEED
#=====================
training_introduce_fastest_sound = ("You will encounter three different speeds in the blocks.\n"
                                    "\n"
                                    "Press any button to hear a sequence with the fastest speed")

ef.display_text(training_introduce_fastest_sound, win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

ef.display_text('A sequence with the fastest speed', win)
row = df.loc[0]
stim_dur = row['stim_duration']
stim_code = ['stim_code']
stim = stream[0].stimuli[row['stim_name']]
stream[0].fill_buffer(stim)
stream[0].start(when = 0, wait_for_start = 1)
WaitSecs(stim_dur)

repeat = True 
while repeat:

    txt = ("Can you detect the repeating pattern?\n"
            "LEFT: YES               RIGHT: NO")

    ef.display_text(txt, win)
    keys = kb.waitKeys(keyList=['2', '3'], waitRelease=True)

    if '2' in keys:  # YES, proceed to the next sequence
        repeat = False
    elif '3' in keys:  # NO, repeat the sequence
        ef.display_text('Repeating the sequence one more time....', win)
        stream[0].fill_buffer(stim)
        stream[0].start(when = 0, wait_for_start = 1)
        WaitSecs(stim_dur)



#=====================
#MEDIUM SPEED
#=====================
ef.display_text("Press any button to hear a sequence with a medium speed ", win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

ef.display_text('A sequence with a medium speed', win)
row = df.loc[1]
stim_dur = row['stim_duration']
stim_code = ['stim_code']
stim = stream[0].stimuli[row['stim_name']]
stream[0].fill_buffer(stim)
stream[0].start(when = 0, wait_for_start = 1)
WaitSecs(stim_dur)

repeat = True 
while repeat:

    txt = ("Can you detect the repeating pattern?\n"
            "LEFT: YES               RIGHT: NO")

    ef.display_text(txt, win)
    keys = kb.waitKeys(keyList=['2', '3'], waitRelease=True)

    if '2' in keys:  # YES, proceed to the next sequence
        repeat = False
    elif '3' in keys:  # NO, repeat the sequence
        ef.display_text('Repeating the sequence one more time....', win)
        stream[0].fill_buffer(stim)
        stream[0].start(when = 0, wait_for_start = 1)
        WaitSecs(stim_dur)



#=====================
#THE SLOWEST SPEED
#=====================
ef.display_text("Press any button to hear a sequence with the slowest speed ", win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

ef.display_text('A sequence with the slowest speed', win)
row = df.loc[2]
stim_dur = row['stim_duration']
stim_code = ['stim_code']
stim = stream[0].stimuli[row['stim_name']]
stream[0].fill_buffer(stim)
stream[0].start(when = 0, wait_for_start = 1)
WaitSecs(stim_dur)

repeat = True 
while repeat:

    txt = ("Can you detect the repeating pattern?\n"
            "LEFT: YES               RIGHT: NO")

    ef.display_text(txt, win)
    keys = kb.waitKeys(keyList=['2', '3'], waitRelease=True)

    if '2' in keys:  # YES, proceed to the next sequence
        repeat = False
    elif '3' in keys:  # NO, repeat the sequence
        ef.display_text('Repeating the sequence one more time....', win)
        stream[0].fill_buffer(stim)
        stream[0].start(when = 0, wait_for_start = 1)
        WaitSecs(stim_dur)

# # just after that while playing the audio, simultaneously record the microphone outpu
# # current_audio_data, absrecposition, overflow, cstarttime = stream[0].get_audio_data(min_secs = min_stim_duration + 1)
# current_audio_data, absrecposition, overflow, cstarttime = stream[0].get_audio_data(min_secs = stim_dur + 1)


#=====================
#TIMING PARAMETERS
#=====================
tonsets = np.zeros(nTrials)
toffsets =  np.zeros(nTrials)
max_stim_duration = df['stim_duration'].max()
min_stim_duration = df['stim_duration'].min()
tISI = df['isi'].to_list()



start_tapping_instruction = ("Now, try to tap in synchrony with the repeating patterns.\n"
                             "You can press any button to start tapping.")

ef.display_text(start_tapping_instruction, win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

#=====================
#CLEAR THE EXISTING EVENTS
#=====================
wakeup = GetSecs() # learn when a block starts.When I have multiple blocks, I should also store this as a list. For now, it is okay
kb.clearEvents()  # clear any previous keypresses
stream[0].get_audio_data()  # I think I am doing this to clear the buffer just before the recording

#=====================
#LOOP
#=====================
for itrial in range(len(df)):
    #===========
    #START TRIAL
    #===========
    print(itrial)
    t_trial = ef.display_text(f'Trial {itrial + 1} of {nTrials}\n', win)

    # set up trial specific parameters
    row =  df.loc[itrial]
    stim_dur = row['stim_duration']
    stim_code = row['stim_code']
    stim = stream[0].stimuli[row['stim_name']]
    stream[0].fill_buffer(stim)

    # arrange timing
    # for the first trial, presentation time is half a second after the start of the trial
    if itrial == 0:
        onset_time = wakeup + 0.5
    # after the first trial, the onset_time will be saved to the tonsets
    else:
    # following trials, the stimulus onset is calculated based on the previous
    # trial's onset time and a specified inter-stimulus interval
        onset_time = tonsets[itrial-1] + tISI[itrial-1]


    # present stimuli and collect responses
    tonset = stream[0].start(when = onset_time, wait_for_start = 1)
    WaitSecs(stim_dur)

    # just after that while playing the audio, simultaneously record the microphone outpu
    # current_audio_data, absrecposition, overflow, cstarttime = stream[0].get_audio_data(min_secs = min_stim_duration + 1)
    current_audio_data, absrecposition, overflow, cstarttime = stream[0].get_audio_data(min_secs = stim_dur + 1)
    
    tonsets[itrial] = tonset  # update onset times
    toffsets[itrial] = GetSecs()

    sound_name = 'block_' + str(0) + '_itrial_' + str(itrial) + '_stimcode_' + str(stim_code) + '_unitdur_' + str(row['unitdur']) + '_percentage_' + str(row['percentage']) +  '_' + experiment_mark
    output_stim_directory = data_dir + '/' + sound_name
    wavfile.write(output_stim_directory, fs, current_audio_data)


    time_axis = np.arange(0, len(current_audio_data[:, 1]))/ fs

    # Plot the saved output 
    plt.figure(figsize=(15, 5))
    if len(current_audio_data.shape) == 2:
        plt.subplot(2, 1, 1)
        plt.plot(time_axis, current_audio_data[:, 0], label='audio channel')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('audio signal over time')
        plt.grid(True) 
        plt.legend() 
    
        plt.subplot(2, 1, 2)
        plt.plot(time_axis, current_audio_data[:, 1], label='mic channel')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('tapping data over time')
        plt.grid(True) 
        plt.legend() 
    else:
        plt.plot(time_axis, current_audio_data, label='Mono Channel')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('tapping data over time')
        plt.grid(True) 
    
    plt.tight_layout()
    plot_title = sound_name.replace('wav', 'png')
    plt.savefig(plot_title, dpi=300) 
    plt.show()


# save the name of the wav files at the end of an each block    
stream[0].close()

experiment_end_text = 'end of the training session, press any bar to end the session.'
ef.display_text(experiment_end_text, win)
# Wait for any key press to continue
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

win.close()
