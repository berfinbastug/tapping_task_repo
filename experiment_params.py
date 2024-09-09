#=====================
#STIMULUS RELATED PARAMETERS
#=====================
# DURATION, IV 1
# independent variable 1
min_unit_dur = 0.4  
max_unit_dur = 1 
n_unit_dur_cond = 3

# REPEATING PERCENTAGE OF THE TONES, IV 2
min_rep_percentage = 0  # Define the start point
max_rep_percentage = 1  # define the end point
n_rep_percentage_cond = 10  # define the number of elements

nblocks = 7
iti = 1  # inter trial interval

#=====================
#OUTPUT
#=====================
output_data_columns = ['participant_id', 'time', 'block_idx', 
                       'trial_idx', 'tapping_file_name', 'stim_code', 
                       'unitdur', 'percentage']

#=====================
#SET UP AUDIO PARAMETERS
#=====================
device_name = 'US-4x4HR'
# device_name = 'MacBook Pro Speakers'
#device_name = 'US-2x2HR'
device_id = 1
stimulus_rms = 1