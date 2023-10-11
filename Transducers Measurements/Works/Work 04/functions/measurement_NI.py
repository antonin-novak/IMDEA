# -*- coding: utf-8 -*-
# Version: 2.0.0
import nidaqmx
from nidaqmx.constants import AcquisitionType, TaskMode, TerminalConfiguration


def measurement_NI(x, fs, Dev, iepe=[False, False, False, False]):
    '''
    Measures data using National Instruments (NI) USB-4431.

    This function establishes communication with an NI device specified by `Dev`.
    It configures the analog input channels based on the provided `iepe` parameter.
    Note: Sensitivities are not included; they must be considered separately.

    Args:
    - x (list or ndarray): Input signal.
    - fs (float): Sample rate in Hz.
    - Dev (str): Name of the NI device (e.g., 'Dev1').
    - iepe (list of bool, optional): List indicating whether each channel uses IEPE. 
                                     Defaults to [False, False, False, False].

    Returns:
    - ndarray: A 2D array containing 4 channels of len(x) samples.

    Example:
        y = measurement_NI(x, fs, 'Dev1', iepe=[True, False, True, False])

    Author:
        Antonin Novak - 29.10.2021, last update - 10.10.2023
    '''

    # Initialize master and slave tasks
    with nidaqmx.Task() as master_task, nidaqmx.Task() as slave_task:

        # Configure the master task's analog output channel
        master_task.ao_channels.add_ao_voltage_chan(
            Dev + "/ao0", min_val=-3.5, max_val=3.5)

        # Iterate through each channel and configure based on the `iepe` parameter
        for index, is_iepe in enumerate(iepe):

            # Formulate the channel name based on the device and index
            channel_name = f"{Dev}/ai{index}"

            # Configure channel for IEPE (if `is_iepe` is True) or as regular voltage input
            if is_iepe:
                slave_task.ai_channels.add_ai_accel_chan(
                    channel_name,
                    current_excit_val=0.002,
                    terminal_config=TerminalConfiguration.PSEUDODIFFERENTIAL
                )
            else:
                slave_task.ai_channels.add_ai_voltage_chan(channel_name)

        # analog input port is configured for continuous 8000 s/s )
        master_task.timing.cfg_samp_clk_timing(
            fs, sample_mode=AcquisitionType.CONTINUOUS)
        # analog output port is configured for continous 8000 s/S
        slave_task.timing.cfg_samp_clk_timing(
            fs, sample_mode=AcquisitionType.CONTINUOUS)

        """ Start generating AO and reading AI"""

        master_task.write(x)  # analog output buffer is filled with sine wave
        # analog output port is committed
        master_task.control(TaskMode.TASK_COMMIT)

        # analog input port is committed
        slave_task.control(TaskMode.TASK_COMMIT)

        print('Acqusition is started')
        slave_task.start()
        master_task.start()

        """ Done """

        result = slave_task.read(
            number_of_samples_per_channel=len(x), timeout=-1)  # analog input

        print('Acqusition is finished')
        return result


if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import numpy as np

    """ Creating Sine wave for Analog output generation"""

    fs = 48000  # sampling frequency
    f0 = 50  # frequency of signal
    T = 1  # time duration
    t = np.arange(0, T, 1/fs)  # time domain array
    x = np.sin(2 * np.pi * f0 * t)  # sine wave

    """ Done """

    y = measurement_NI(x, fs, 'Dev3')
    u = y[0]
    i = y[1]

    fig, ax = plt.subplots(2)
    ax[0].plot(t, u)
    ax[1].plot(t, i)
