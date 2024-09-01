import matplotlib.pyplot as plt
import numpy as np

def plot_dots(result_array_msecs, trial_unit_dur_value, trial_wav_file_name):

    # trial specific plots
    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(result_array_msecs, np.zeros_like(result_array_msecs), 'o', label='Tapping Points')  # Dot plot
    plt.axhline(y=0, color='k')  # Horizontal line crossing y=0
    plt.axvline(x=trial_unit_dur_value, color='r', linestyle='--', label='unit duration')  # Vertical line at x=0.4

    # Set limits and labels
    plt.xlim(0, np.max(result_array_msecs))
    plt.ylim(-0.1, 0.1)
    plt.xlabel('tapping points')
    plt.title(trial_wav_file_name)
    plt.yticks([])  # Hide y-axis ticks

    # Add legend
    plt.legend()

    # Show plot
    plt.show()



def circular_plot_tapping_vectors(tapping_vectors, trial_wav_file_name):
    # circular plot
    # Extract real and imaginary parts
    real_parts = tapping_vectors.real
    imaginary_parts = tapping_vectors.imag

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot the unit circle
    circle = plt.Circle((0, 0), 1, color='b', fill=False, linestyle='--')
    ax.add_artist(circle)

    # Plot the complex numbers
    ax.scatter(real_parts, imaginary_parts, color='r', label='Complex Numbers')

    # Draw lines from the origin to each point
    for real, imag in zip(real_parts, imaginary_parts):
        ax.plot([0, real], [0, imag], color='gray', linestyle='--')

    # # Annotate each point
    # for i, (real, imag) in enumerate(zip(real_parts, imaginary_parts)):
    #     ax.text(real, imag, f'{i+1}', fontsize=12, ha='right')

    # Set equal scaling
    ax.set_aspect('equal')

    # Set the limits and labels
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_title(trial_wav_file_name)
    # ax.set_xlabel('Real Part')
    # ax.set_ylabel('Imaginary Part')
    ax.legend()

    # Show the plot
    plt.show()



def plot_vertical_lines_tapping(result_array_msecs, trial_wav_file_name):

    # Create a figure and axis
    plt.figure(figsize=(8, 6))
    # plotting vertical lines
    # Plot vertical lines crossing the x-axis at each x-value
    for x in result_array_msecs:
        plt.axvline(x=x, color='r', linestyle='--', label='_nolegend_')  # Use '_nolegend_' to avoid duplicate labels

    # Plot horizontal line crossing y=0
    plt.axhline(y=0, color='k')

    # Set limits and labels
    plt.xlim(np.min(result_array_msecs) - 0.1, np.max(result_array_msecs) + 0.1)  # Set limits slightly beyond the min and max x-values
    plt.ylim(-0.1, 0.1)
    plt.xlabel('time (ms)')
    plt.title(trial_wav_file_name)
    plt.yticks([])  # Hide y-axis ticks

    # Add a legend for the vertical lines
    plt.legend(['tap onsets'], loc='upper left')

    # Show plot
    plt.show()