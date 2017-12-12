"""
Script to separate an image into tiles and color channels before compressing.
"""
import cv2, math
import numpy as np
from PIL import Image
from frequency_calculator import get_frequencies
from data_processing import *
from puffman import *

class Tile(object):
    """ Tile class for storing data about a tile of an image """
    def __init__(self, tile_image):
        """
            tile_image: original tile (np.array)
            y_tile: original tile's Y color channel (np.array)
            cb_tile: original tile's Cb color channel (np.array)
            cr_tile: original tile's Cr color channel (np.array)
        """
        self.tile_image = tile_image
        self.y_tile, self.cb_tile, self.cr_tile = None, None, None


class ImageProcessing(object):
    """
        Compression algorithm
    """
    def __init__(self, file_path="dog.jpg", tile_size=300):
        """
            file_path = path to image file to be compressed (string)
            tile_size: size of tile (int)
        """
        self.file_path = file_path
        self.tile_size = tile_size

        self.img = None
        # list of Tile objects of the image
        self.tiles = []


        self.rgb2ycbcr_matrix = np.array([[0.2999, 0.587, 0.114],
            [-0.16875, -0.33126, 0.5],[0.5, -0.41869, -0.08131]])
        self.ycbcr2rgb_matrix = ([[1.0, 0, 1.402], [1.0, -0.34413, -0.71414], [1.0, 1.772, 0]])  

    def init_image(self):
        """ create image"""
        self.img = cv2.imread(self.file_path)

    def create_tiles(self):
        """
            Save tiles from self.img of size self.tile_size by self.tile_size into self.tiles

        """
        (h, w, _) = self.img.shape


        # add to w and h so right and bottom edges have full tiles
        # in case w and h are not originally divisible by self.tile_size
        extra = w % self.tile_size
        w += (self.tile_size - extra)
        extra = h % self.tile_size
        h += (self.tile_size - extra)


        # loop through w and h with tile_size steps
        # to find the top left corner pixel of every tile
        for i in range(0, w, self.tile_size): # loop through the width to get cols
            for j in range(0, h, self.tile_size): # loop through the height to get rows
                tile = Tile(self.img[j:j + self.tile_size, i:i + self.tile_size])
                self.tiles.append(tile)

    def color_transform(self):
        """
            convert a tile from RGB to YCbCr color space
        """
        for tile in self.tiles:
            (h, w, _) = tile.tile_image.shape

            # cv2 uses BGR to open images
            rgb_tile = cv2.cvtColor(tile.tile_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_tile, 'RGB')

            # placeholder matricies for the 3 color spaces
            # size of each matrix is size of original tile
            tile.y_tile, tile.cb_tile, tile.cr_tile = np.zeros((h, w)), np.zeros((h, w)), np.zeros((h, w))

            # loop through each pixel, calculate the YCbCr values,
            # and save the values in the Tile object
            for i in range(0, w):
                for j in range(0, h):
                    r, g, b = img.getpixel((i, j))
                    rgb_array = np.array([r, g, b])
                    yCbCr = np.matmul(self.rgb2ycbcr_matrix, rgb_array)
                    tile.y_tile[j][i], tile.cb_tile[j][i], tile.cr_tile[j][i] = center_zero(yCbCr[0]), center_zero(yCbCr[1]), center_zero(yCbCr[2])
            # see the tile
            # Image.fromarray(tile.y_tile).show()

    def center_zero(self, value):
        return value - 127
    
    def compress(self):
        self.init_image()
        self.create_tiles()
        self.color_transform()


# class ConstructImage(object):
#     """
#         Parse numpy array to get the decoding dictionary and image tiles
#     """
#     def __init__(self, complete_vector, tile_size=300):
#         """
#             image_vector = deconstructed 1D numpy array with headers, 
#             tile_size = size of tile (int)
#         """
#         self.tile_size = tile_size
#         self.complete_vector = complete_vector
#         self.dict = self.get_dictionary()
#         self.img_matrix = None
#     def get_dimensions(self):
#         height = self.complete_vector[200:208]
#         width = self.complete_vector[208:216]
#         return self.complete_vector[200:216]
#     def get_dict(self):
#         decode_dict = self.complete_vector[216+34+200:216+34+200+80] # 200 -> header, 16 -> h & w dimensions, 34 -> image len, 80 -> dictionary length
#         return decode_dict
#     def get_encoded_img(self):
#         encoded_img = self.complete_vector[216:216+34] # 200 -> header, 16 -> h & w dimensions, 34 -> image len
#         return encoded_img
#     def get_dictionary(self):
#         """
#             Take in binary dictionary and convert it to an actual dictionary
#         """
#         binary_float_vector = list(self.complete_vector[216+34+200:216+34+200+120]) # 120 -> encoded_dict len
#         binary_int_vector = []
#         for i in range(len(binary_float_vector)):
#             try:
#                 binary_int_vector.append(int(binary_float_vector[i]))
#             except IndexError as e:
#                 print e, i
#         temp = binary_to_dictionary(binary_int_vector)
#         return flip_dictionary(temp) # I think this is needed


def save_image(img_array, filename):
    img = Image.fromarray(img_array)
    img.save(filename)
    img.show()

if __name__ == '__main__':
    img = cv2.imread('images/dog.jpg')
    save_image(img, 'images/dog2.jpg')
    
# # ImageProcessing().compress()
