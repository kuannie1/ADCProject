"""
Script to separate an image into tiles and color channels before compressing.
"""
import cv2, math
import numpy as np
from PIL import Image
from frequency_calculator import get_frequencies

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
                    tile.y_tile[j][i], tile.cb_tile[j][i], tile.cr_tile[j][i] = yCbCr[0], yCbCr[1], yCbCr[2]
            # see the tile
            # Image.fromarray(tile.y_tile).show()

    def center_zero(self):
        pass

    def compress(self):
        self.init_image()
        self.create_tiles()
        self.color_transform()



if __name__ == '__main__':
	ImageProcessing().compress()
