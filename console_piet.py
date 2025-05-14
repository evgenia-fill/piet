from argparse import ArgumentParser
import argparse
from pixel_Interpreter import PixelInterpreter
from user_input import UserInputParser


parser = ArgumentParser(description="Интерпретатор языка Piet, написанный на python")
parser.add_argument("image_path", type=str, help="путь до интерпретируемого изображения")
parser.add_argument('--debug', '-d', action=argparse.BooleanOptionalAction,
                    help="Включает вывод команд и состояния стека.")
parser.add_argument('--step-by-step', '-st', action=argparse.BooleanOptionalAction,
                    help="Включает пошаговое выполнение программы. \
                          После каждого шага требуется нажатие ENTER для продолжения.")
parser.add_argument('--size', '-s', type=int, default=1, #// , nargs='?'
                    help="Размер кодела (по умолчанию 1). Укажите положительное целое число.")
args = parser.parse_args()
step_by_step = args.debug and args.step_by_step
if args.size >= 1:
    parser = UserInputParser(args.image_path, size=args.size)
    img_arr = parser.open_image()
    interpreter = PixelInterpreter(img_arr, debug=args.debug, step_by_step=step_by_step)
    result = interpreter.interpreter()
else:
    print("Размер кодела должен быть >= 1")