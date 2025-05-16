from argparse import ArgumentParser
import argparse
from pixel_Interpreter import PixelInterpreter
from user_input import UserInputParser
from errors import *
from colored_text import red


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
try:
    if args.step_by_step and not args.debug:
        raise IncorrectModeError("Режим пошагового исполнения можно использовать только при отладке!")
    if args.size < 1:
        raise IncorrectSizeError("Размер кодела должен быть >= 1!")
    parser = UserInputParser(args.image_path, size=args.size)
    img_arr, breakpoints = parser.open_image()
    br_mode = 'some' if len(breakpoints) > 0 else 'all'
    interpreter = PixelInterpreter(img_arr, 
                                   debug=args.debug, 
                                   step_by_step=args.step_by_step, 
                                   breakpoints=breakpoints, 
                                   breakpoint_mode=br_mode)
    result = interpreter.interpreter()
except FileNotFoundError:
    print(red("Некорректный путь до изображения!"))
except UnknownColorError:
        print(red("Использован недопустимый цвет!"))
except Exception as e:
    print(red(e))