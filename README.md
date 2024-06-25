data_frame_functions.py [import as dff]
(1) Generate_baseline_table: This function generates a list of trial conditions for an experiment based on provided parameters. It creates combinations of unit durations and repetition percentages, assigns a specific stimulus code for each combination, and specifies expected responses.
(2) get_df(table_name, table_dir): to read a tab-separated values (TSV) file into a Pandas DataFrame and return both the DataFrame and the number of rows (trials) it contains.
(3) check_consecutive_occurrences(array):
(4) pseudorandomize_and_save_df(df, which_block, exp_info, table_dir):
(5) save_output_df(output, experiment_mark, which_block, data_dir): The function saves the provided output data to a file in a specified directory. The file is named based on the block number and experiment mark, and the data is saved in a tab-separated format without row indices.
