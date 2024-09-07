#=====================
# ESTABLISH THE WORKING ENVIRONMENT
#=====================
import pandas as pd
import numpy as np
import os

from psychtoolbox import WaitSecs, GetSecs
from psychopy import core, gui, visual
from psychopy.hardware import keyboard
from psychtoolbox import audio, PsychPortAudio
from scipy.io import wavfile
import run_experiment_functions as ef
import data_frame_functions as dff
import tap_related_functions as trf
import experiment_params as params

#=====================
#DEFINE DIRECTORIES
#=====================
# when I switch to a new computer, just change the main_dir
main_dir = '/home/bastugb/Documents/tapping_experiment'
stimuli_dir = main_dir + '/stimuli'
data_dir = main_dir + '/data'
table_dir = main_dir + '/tables'

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
experiment_mark = 'tapping_experiment_toneclouds_pid' + str(exp_info['participant_id']) + '_' + exp_info['time'] + '.wav'

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


experiment_start_text = ("Welcome to our experiment.\n"
                         "Please carefully read the following instructions.\n"
                         "\n"
                         "\n"
                         "You can press any button to continue to the next page.")

ef.display_text(experiment_start_text, win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

experiment_details_text = ("This session consists of 7 blocks. Each block lasts about 11 minutes." 
                           "There will be short breaks between each block. Use this time to rest and prepare for the next block.\n"
                           "You can leave the booth in between blocks to stretch your legs."
                           "\n" 
                           "Continue for detailed instructions about the experimental procedure.")

ef.display_text(experiment_details_text, win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

experimental_instructions = ("During the experiment, you will hear long sequences of noise-like sounds."
                             "Your task is to tap your finger next to the attached microphone as soon as you hear the sound and keep tapping until the sequence ends. " 
                             "Some of these sound sequences contain repeating patterns that create a certain beat. Try to detect these repeating patterns and tap in synchrony with them." 
                             "This means aligning each tap with each repeating pattern and tapping at the same speed as the repeating pattern.\n" 
                             "The repeating patterns will be present in some trials, sometimes obvious and sometimes not. In any case, try your best to detect the repetitions and tap in sync with them." 
                             "If you do not detect any repeating pattern, just continuously tap your finger with any rhythm or speed you wish.\n"
                             "\n"
                             "Press any button to continue.")

ef.display_text(experimental_instructions, win)
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)



# learn nblocks
# counterbalance the order of block presentation
# i think in my case there is no need for counterbalancing because all blocks are similar
files_in_tabledir = os.listdir(table_dir)
block_list = [file for file in files_in_tabledir if file.endswith('.tsv')]
nBlocks = params.nblocks

#=====================
# LOOP OVER BLOCKS
#=====================
for iblock in range(1):
    which_block = iblock + 1
    
    #=====================
    #READ THE BLOCK SPECIFIC DATA FRAME 
    #=====================
    table_name = f'tapping_experiment_block_{which_block}_table.tsv'
    df, nTrials = dff.get_df(table_name, table_dir)

    #=====================
    #SHUFFLE THE DATA FRAME
    #=====================
    # pseudo randomize the data frame for each individual
    # condition: any value should not occur more than three times consecutively
    # shuffle dataframe rows until the condition is met
    # save this shuffled table immediately before you forget
    df_shuffled = dff.pseudorandomize_and_save_df(df, which_block, exp_info, table_dir)


    # Here, the tapping data will be stored
    subject_block_specific_path  = data_dir + '/tapping_experiment_block' + str(which_block) + '/participantid_' + str(exp_info['participant_id'])
    os.makedirs(subject_block_specific_path, exist_ok=True)
    
    # give the instructions and block related information here
    block_start_text = f'Block {which_block} of {nBlocks}\n' + 'Press any button to start'
    ef.display_text(block_start_text, win)
    # Wait for any key press to continue
    kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

    #=====================
    #PRELOAD STIMULUI
    #=====================
    # list the sound filenames, in a randomized way
    sound_filenames = df_shuffled['stim_name'].to_list()
    # this directory is necessary while reading from wav-files
    # search the sound in a specific block folder
    stim_for_block = os.path.join(stimuli_dir,f'tapping_experiment_block{which_block}')  
    # define stimuli, which is stream in my case
    # setup audio stream 
    stimuli, channels, fs = ef.setup_audio_files(sound_filenames, stim_for_block, params)
    
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
    #TIMING PARAMETERS
    #=====================
    # I need to do something to organize the onset time of each stimulus
    # I am planning to do the following thing. for the first stimulus, I will learn the current time and just add 0.5.
    # When I start the stream, I get a time stamp of when the stream is actually presented. To learn when I should 
    # present the nth sound, I should add (n-1)th soa to the (n-1)th onset time. To accsess to the (n-1)th onset time,
    # I will create first list of zeros, the size of this will be ntrial.
    tonsets = np.zeros(nTrials)
    toffsets = np.zeros(nTrials)  # this is just for fun
    max_stim_duration = df_shuffled['stim_duration'].max()
    min_stim_duration = df_shuffled['stim_duration'].min()
    
    # I also need the list of stimulus onset asynchrony (soa or isi)
    # In this context, it only matters when participants exceeds the response window.
    # It is the maximum amount of waiting time, if they respond earlier, ISI will be defined based on their reaction time
    tISI = df_shuffled['isi'].to_list()

    #=====================
    #PREPARE DATA FRAME TO STORE OUTPUT
    #=====================
    output_data = pd.DataFrame(columns=params.output_data_columns)

    #=====================
    #LEARN WHEN THE BLOCK STARTS AND CLEAR THE EXISTING EVENTS IF ANY
    #=====================
    wakeup = GetSecs() # learn when a block starts.When I have multiple blocks, I should also store this as a list. For now, it is okay
    kb.clearEvents()  # clear any previous keypresses

    #=====================
    # LOOP OVER TRIALS
    #=====================
    stream[0].get_audio_data()  # I think I am doing this to clear the buffer just before the recording
    for itrial in range(2):
        #=====================
        #START TRIAL
        #===================== 
        print(itrial)
        t_trial = ef.display_text(f'Trial {itrial + 1} of {nTrials}\n', win)
        
        # setup trial specific parameters
        row = df_shuffled.loc[itrial]
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
            onset_time = tonsets[itrial-1]+ tISI[itrial-1]

        # present stimuli and collect responses
        tonset = stream[0].start(when = onset_time, wait_for_start = 1)
        WaitSecs(stim_dur)
        # just after that while playing the audio, simultaneously record the microphone outpu
        # current_audio_data, absrecposition, overflow, cstarttime = stream[0].get_audio_data(min_secs = min_stim_duration + 1)
        current_audio_data, absrecposition, overflow, cstarttime = stream[0].get_audio_data(min_secs = stim_dur + 1)
        
        tonsets[itrial] = tonset  # update onset times
        toffsets[itrial] = GetSecs()

        sound_name = 'block_' + str(which_block) + '_itrial_' + str(itrial) + '_stimcode_' + str(stim_code) + '_unitdur_' + str(row['unitdur']) + '_percentage_' + str(row['percentage']) +  '_' + experiment_mark
        output_stim_directory = subject_block_specific_path + '/' + sound_name
        wavfile.write(output_stim_directory, fs, current_audio_data)
        tmp_df = pd.DataFrame({'participant_id': exp_info['participant_id'],
                               'time': exp_info['time'],
                               'block_idx': [which_block],
                               'trial_idx': [itrial], 
                               'tapping_file_name': [sound_name],
                               'stim_code': [row['stim_code']],
                               'unitdur': [row['unitdur']],
                               'percentage': [row['percentage']]})
        output_data = pd.concat([output_data, tmp_df], ignore_index=True)

        refractory_period = 0.15
        threshold = 0.1
        onset_points_in_time, onset_points_in_signal = trf.find_tap_onset(fs, refractory_period, threshold, current_audio_data[:, 1])

        crude_ntap = len(onset_points_in_signal)

        # check if no taps are detected
        if crude_ntap == 0:
            # if no taps detected, display a warning message about low signal quality
            ef.display_text("The signal quality is too low; please wait for the experimenter's instructions.", win)
            kb.waitKeys(keyList=['space'], waitRelease=True)
        else:
            print(crude_ntap)

    # save the name of the wav files at the end of an each block    
    dff.save_tapping_output(subject_block_specific_path, output_data, exp_info['participant_id'], which_block)
    stream[0].close()

experiment_end_text = ("End of the experiment!\nPress any button to end the experiment.")
ef.display_text(experiment_end_text, win)
# Wait for any key press to continue
kb.waitKeys(keyList=['1', '2', '3', '4'], waitRelease=True)

win.close()
