from argparse import ArgumentParser
import argparse
from pixel_Interpreter import PixelInterpreter
from user_input import UserInputParser

# вдруг понадобится такой вариант запуска
parser = ArgumentParser(description="Интерпретатор языка Piet, написанный на python")
parser.add_argument("image_path", help="путь до интерпретируемого изображения")
parser.add_argument('--debug', action=argparse.BooleanOptionalAction)
args = parser.parse_args()
parser = UserInputParser(args.image_path)
img_arr = parser.open_image()
interpreter = PixelInterpreter(img_arr, debug=args.debug)
result = interpreter.interpreter()