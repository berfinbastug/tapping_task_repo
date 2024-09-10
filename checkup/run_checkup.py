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
main_dir = '/home/bastugb/Documents/tapping_experiment/checkup'
# stimuli_dir = main_dir + '/stimuli_checkup'
data_dir = main_dir + '/data_checkup'

# we don't need a table here
# table_dir = main_dir + '/tables_training' 

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
experiment_mark = 'spontaneous_tapping_experiment_toneclouds_pid' + str(exp_info['participant_id']) + '_' + exp_info['time'] + '.wav'

#=====================
#READ THE TRAINING DATA FRAME 
#=====================


#=====================
#PRELOAD STIMULUI
#=====================
fs = 44100
channels= 1
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
stream = [audio.Stream(freq=fs, device_id = params.device_id, mode = 3, latency_class = 3, channels= [channels, 2])]

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
#stream[0].stimuli = stimuli

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

checkup_start_text = ("Welcome! Here, we are checking whether the system is working properly.\n"
                    "Please tap on the microphone attached to the table at a comfortable level until the stop sign appears on the screen\n"
                    "\n"
                    "\n"
                    "You can press any button to start recording.")

ef.display_text(checkup_start_text, win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

stream[0].get_audio_data()  # I think I am doing this to clear the buffer just before the recording
wakeup = GetSecs() # learn when a block starts.When I have multiple blocks, I should also store this as a list. For now, it is okay
kb.clearEvents()  # clear any previous keypresses

#=====================
#START RECORDING
#=====================
ef.display_text('start tapping', win)
# first only control the tapping data
# in disguise also record participants' spontaneous tapping rate
# for this I will present no sound but silence
silence_dur = 1.5 * 60  # 1.5 minutes in seconds

# fs is already defined above
# generate silence
num_samples_silence = int(silence_dur * fs)
silence = np.zeros(num_samples_silence)
#stim = stream[0].stimuli[silence]
stream[0].fill_buffer(silence)
# present stimuli and collect responses
tonset = stream[0].start(when = 0, wait_for_start = 1)
WaitSecs(silence_dur)

# just after that while playing the audio, simultaneously record the microphone outpu
# current_audio_data, absrecposition, overflow, cstarttime = stream[0].get_audio_data(min_secs = min_stim_duration + 1)
current_audio_data, absrecposition, overflow, cstarttime = stream[0].get_audio_data(min_secs = silence_dur + 1)

# purpose is to plot the tapping data
tapping_signal_only = current_audio_data[:, 1]
time_axis = np.arange(0, len(tapping_signal_only))/ fs

# slowly approaching to an end
ef.display_text('You can stop. Press any button to end the session.', win)
# Wait for any key press to continue
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

# after pressing any key, save the output tapping data
output_stim_name = data_dir + '/' + experiment_mark
wavfile.write(output_stim_name, fs, current_audio_data)

# finally close the data
win.close()

# Plot the audio signal
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


plot_title = experiment_mark.replace('wav', 'png')
plt.savefig(plot_title, dpi=300) 
plt.show()

# save the name of the wav files at the end of an each block    
stream[0].close()

