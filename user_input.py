from PIL import Image
import numpy as np


class UserInputParser:
    def __init__(self, path):
        self.path = path

    def open_image(self):
        image = Image.open(self.path).convert('RGB')
        img_arr = np.array(image)
        return img_arr