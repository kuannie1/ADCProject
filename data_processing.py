"""
Data processing used for USRP wireless communication.
"""
import numpy as np
import cv2, math
import huffman


def flip_dictionary(code_dict):
	reversed_code_dict = {y:x for x,y in code_dict.iteritems()}
	return reversed_code_dict


def dictionary_to_binary(input_dict):
	""" Converts the dictionary to binary.
	Assumes keys and values are numbers. """

	res = []
	res += make_binary_list(ord('{'))
	for k, v in input_dict.iteritems():
		res += make_binary_list(k)
		res += make_binary_list(ord(':'))
		res += make_binary_list(v)
	res += make_binary_list(ord('}'))

	return np.array(res)

def expand(input_array):
	""" Given a binary input array, change 0 values to -1 
	and expand such that each value in the array is
	repeated 50 times. """
	
	expanded = []
	for val in input_array:
		if val == 0:
			val = -1
		elif val == 1:
			val = int(val)
		else:
			print("non-binary input to expand")
		print val
		for i in range(0,50):
			expanded.append(val)

	expanded_array = np.array(expanded)
	return expanded_array

def make_binary_list(num, eight_bit=True):
	""" Takes in decimal number, converts to binary and returns list of bits"""
	if eight_bit:
		num = format(num,'08b')
	else:
		num = bin(num)[2:]

	return [int(d) for d in num]



def complexize_data(nparray_data):
    """ Takes in results from data_to_write and makes every other index complex """
    print nparray_data
    list_data = list(nparray_data)
    for i in range(1, len(list_data), 2):
        list_data[i] = 1j*list_data[i]
    result = np.array(list_data)
    print result

def remove_channel_effects(y):
    """ Removes the effects of the channel by calculating h
        and the frequency offset between the receiver and transmitter
        and dividing them out of the signal as appropriate.

        y: received signal
        returns: x_estimate
    """
    y_square = np.square(y)
    fft_y_square = abs(np.fft.fftshift(np.fft.fft(y_square)))
    h_square, two_f_delta = max(fft_y_square), np.argmax(fft_y_square)
    f_delta = two_f_delta / 2
    h = math.sqrt(h_square)
    for n in range(0, y.size):
        y[n] = y[n] / (h * exp(1j*f_delta*n));
    return y

def remove_noise(y):
    """ Removes the noise on the two ends of the received signal by looking
        for large changes in signal power, indicating the start and end of
        the signal, and truncating the signal as appropriate
        y: received signal
        returns: signal without noise
    """
    pass

def estimate_transmitted_signal(y):
    """ Takes in a noisy, received signal (y) and estimates the original transmitted
        signal by squaring y and finding the the peak in the FFT of the y^2 to
        calculate the channel h and the frequency offset f_delta.

        y: received signal
        returns: estimated signal
    """
    return remove_channel_effects(remove_noise(y))

if __name__ == '__main__':
    from decompress import read_from_file
    y = read_from_file()
