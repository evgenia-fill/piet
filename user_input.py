from PIL import Image
import numpy as np


class UserInputParser:
    def __init__(self, filename: str, size: int = 1):
        self.path = filename
        self.size = size

    def open_image(self) -> tuple[np.array, list[int]]:
        image = Image.open(self.path).convert('RGBA')
        '''img_arr = np.array(image)
        return img_arr'''
        width, height = image.size
        new_width, new_height = width // self.size, height // self.size
        img_arr = np.zeros((new_height, new_width, 3), dtype=np.uint8)
        for y in range(0, height, self.size):
            for x in range(0, width, self.size):
                r, g, b, a = image.getpixel((x, y))
                img_arr[y // self.size, x // self.size] = r, g, b
        breakpoins = []
        for y in range(height):
            for x in range(width):
                r, g, b, a = image.getpixel((x, y))
                if 0 < a < 255:
                    breakpoins.append((y // self.size, x // self.size))
        return img_arr, breakpoins

