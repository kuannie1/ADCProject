"""
Data processing used for USRP wireless communication.
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2, math
import huffman
import math
from scipy import stats


def flip_dictionary(code_dict):
	""" Flip a dictioary's keys with its values. """
	reversed_code_dict = {y:x for x,y in code_dict.iteritems()}
	return reversed_code_dict


def dictionary_to_binary(input_dict):
	""" Converts the dictionary to np array of bits
	where each dictionary entry is represented by 24 bits:
	8 bits for how many padding zeros in the key
	8 bits for the key
	8 bits for the value
	Assumes keys are strings and values are integers. """

	res = []
	for k, v in input_dict.iteritems():	
		# right pad dictionary keys (huffman encodings) with zeros so they are each 8 bits.
		# also send how many padding zeros there are, so these can be removed later
		num_padding_zeros = 8-len(k)
		res += make_binary_list(num_padding_zeros)
		for d in k:
			res.append(int(d))
		for i in range(8-len(k)):
			res.append(0)
		res += make_binary_list(v)
	
	# len(res) == 24*len(input_dict)
	return np.array(res)

def binary_to_dictionary(binary_dict_array):
	""" Converts np array of bits to dictionary it represents. 
	Takes in np array of bit shere each dictionary entry is represented by 24 bits:
	8 bits for how many padding zeros in the key
	8 bits for the key
	8 bits for the value
	Returns a dictionary with binary strings as keys and integers as values"""
	res = {}
	for i in range(0, len(binary_dict_array), 24):
		num_padding_zeros = ''
		key = ''
		val = ''
		for j in range(8):
			num_padding_zeros += str(binary_dict_array[i + j])
			key += str(binary_dict_array[i + j + 8])
			val += str(binary_dict_array[i + j + 16])
		num_padding_zeros = int(num_padding_zeros, 2)
		# remove zero padding used to transmit
		key = key[:len(key)-num_padding_zeros]
		res[key] = int(val,2)
	return res

def expand(arr, expand_scale = 150):
	""" Given a binary input array, change 0 values to -1 
	and expand such that each value in the array is
	repeated 50 times. """
	
	expanded = []
	for val in arr:
		if val == 0:
			val = -1
		elif val == 1:
			val = int(val)
		else:
			print("non-binary input to expand")
		for i in range(0,expand_scale):
			expanded.append(val)

	expanded_array = np.array(expanded)
	return expanded_array


def unexpand_and_correct(arr, expand_scale = 150):
	""" Given a received 1-D np array (expanded before transimission), 
	retrieve original 0s and 1s array from before expansion
	correcting for errors in process """

	res = []
        
	# convert to 0s and 1s.
	for i in range(len(arr)):
		if arr[i] > 0:
			arr[i] = 1
		else:
			arr[i] = 0
	res_length = int(math.ceil(len(arr)/float(expand_scale)))
	for i in range(res_length):
	        print "i", i
		if (i+1)*expand_scale - (expand_scale / 5.0)  < len(arr):
			# arr[0: 50], arr[50:100], arr[100: 150]
                        indx1 = i*expand_scale + (expand_scale/5.0)
                        print "indx1", indx1
                        indx2 = (i+1)*expand_scale - (expand_scale/5.0)
                        print "indx2", indx2
			val = stats.mode(arr[int(indx1): int(indx2)])[0]
		else:
		        indx3 = i*expand_scale + (expand_scale/5.0) 
                        print "indx3", indx3
			val = stats.mode(arr[int(indx3) :])[0]
		print "val", val
		res.append(val[0])
	return np.array(res)

def make_binary_list(num, eight_bit=True):
	""" Takes in decimal number, converts to binary and returns list of bits"""
	if eight_bit:
		num = format(num,'08b')
	else:
		num = bin(num)[2:]

	return [int(d) for d in num]



def complexize_data(nparray_data):
    """ Makes every other index the real and imaginary part of signal """
    list_data = []
    for i in range(len(nparray_data)):
        list_data.append(np.real(nparray_data[i]))
        list_data.append(np.imag(nparray_data[i]))
    return np.array(list_data)
    

def decomplexize_data(nparray_data):
    """ Adds real and imaginary components of signal back together """
    y = np.zeros(len(nparray_data)/2)
    y = nparray_data[0::2] + 1j*nparray_data[1::2]
    return y
    #list_data = []
    #for i in range(0, len(nparray_data), 2):
    #    list_data.append(nparray_data[i] + 1j*nparray_data[i+1])
    #return np.array(list_data)

def remove_channel_effects(y):
    """ Removes the effects of the channel by calculating h
        and the frequency offset between the receiver and transmitter
        and dividing them out of the signal as appropriate.

        y: received signal
        returns: x_estimate
    """
    y_square = np.square(y)
    fft_y_square = abs(np.fft.fftshift(np.fft.fft(y_square)))
    xaxis = np.linspace(-np.pi, (len(y_square) - 1.0) / len(y_square) * np.pi, len(y_square))
    h_square, idx = max(fft_y_square), np.argmax(fft_y_square)
    theta = np.angle(xaxis[idx]) / 2.0
    f_delta = xaxis[idx] / 2.0
    h = np.sqrt(h_square)

    x_estimate = np.zeros(y.shape, dtype=complex)
    for n in range(0, y.size):
        channel_effects = (h * np.e**(1.0j*(f_delta*n + theta)))

        # can change this following line to:
        # y[n] = y[n] / channel_effects
        # to get rid of the j in the final output
        # but there is a warning that casting a
        # complet number to real gets rid of the
        # imaginary part, but I don't think we need
        # to worry about that part since the imaginary
        # part is just 0j
        y[n] = y[n] / channel_effects
    return np.real(y)

def remove_noise(y):
    """ Removes the noise on the two ends of the received signal by looking
        for large changes in signal power, indicating the start and end of
        the signal, and truncating the signal as appropriate

        y: received signal
        returns: signal without noise
    """
    return y

def estimate_transmitted_signal(y):
    """ Takes in a noisy, received signal (y) and estimates the original transmitted
        signal by squaring y and finding the the peak in the FFT of the y^2 to
        calculate the channel h and the frequency offset f_delta.

        y: received signal
        returns: estimated signal
    """
    x_est = remove_channel_effects(remove_noise(y))
    return x_est

if __name__ == '__main__':
    from decompress import read_from_file
    y = read_from_file('transmissiontest.dat')
    y = decomplexize_data(y)
    estimate_transmitted_signal(y)
    #print unexpand_and_correct(np.array([1, -1, 1, -1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1]), 5)
