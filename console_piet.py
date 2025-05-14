from argparse import ArgumentParser
import argparse
from pixel_Interpreter import PixelInterpreter
from user_input import UserInputParser

# вдруг понадобится такой вариант запуска
parser = ArgumentParser(description="Интерпретатор языка Piet, написанный на python")
parser.add_argument("image_path", help="путь до интерпретируемого изображения")
parser.add_argument('--debug', '-d', action=argparse.BooleanOptionalAction,
                    help="Включает вывод команд и состояния стека.")
parser.add_argument('--step-by-step', '-s', action=argparse.BooleanOptionalAction,
                    help="Включает пошаговое выполнение программы. \
                          После каждого шага требуется нажатие ENTER для продолжения.")
args = parser.parse_args()
parser = UserInputParser(args.image_path)
img_arr = parser.open_image()
step_by_step = args.debug and args.step_by_step
interpreter = PixelInterpreter(img_arr, debug=args.debug, step_by_step=step_by_step)
result = interpreter.interpreter()