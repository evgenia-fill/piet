import sys
from io import BytesIO
from PIL import Image, ImageOps
import numpy as np


class UserInputParser:
    def __init__(self, path):
        self.path = path

    def open_image(self):
        image = Image.open(self.path)
        img_arr = np.array(image)
        # image.show()
        return img_arr