import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from decompress import *
import data_processing


def find_start_end_signal(filename):
    y = read_from_file(filename)
    y = data_processing.decomplexize_data(y)

    # get real component of y
    print "complex y ", y
    real_y = [float(x) for x in y]
    print "real_y ", real_y[0], real_y[1]

    # get start & end of signal
    start_of_signal = 0 # going to be first index at first (update with later one if I have time)
    for i in range(len(real_y)):
        if (abs(real_y[i]) > 0.0025):
            start_of_signal = i - 3
            break


    end_of_signal = len(real_y)-1
    for i in list(reversed(range(len(real_y)))):
        if (abs(real_y[i]) > 0.0025):
            end_of_signal = i + 3
            break

    print "start & end of signal: ", (start_of_signal, end_of_signal)
    # plt.plot(real_y[start_of_signal:end_of_signal])
    # plt.show()
    return (start_of_signal, end_of_signal)

# find_start_end_signal()