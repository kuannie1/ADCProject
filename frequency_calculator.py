import cv2

def get_frequencies(img):
    """
        Finds the frequencies at which every value in img appears

        img: a 2D matrix
        returns: a dictionary with keys of every possible value in img
                 and values with the corresponding frequency (max 1.0)
                 of how often that value appears in img
    """
    freqs = {}

    # assume img is a w by h 2D matrix
    
    (h, w) = img.shape
    size = float(h*w)

    # loop through each pixel and 
    # save number of times each value appears
    for i in range(0, w):
        for j in range(0, h):
            n = img[j][i]
            if n in freqs:
                freqs[n] += 1
            else:
                freqs[n] = 1

    # turn each value into a percentage/frequency
    # rather than absolute number of occurrences
    for key in freqs:
        freqs[key] = freqs[key] / size
    return freqs

if __name__ == '__main__':
    # example of how to use get_freqs
    # also acts as a test to make sure it works
    img = cv2.imread('dog.jpg')
    (h, w, _) = img.shape
    print img[1] # one of the 3 color channels
    freqs = get_frequencies(img[1])
    print(freqs)
    num = 0
    for key in freqs:
        num += freqs[key]
    print num # should be 1.0

