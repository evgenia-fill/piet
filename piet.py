from user_input import UserInputParser
from pixel_Interpreter import PixelInterpreter
from errors import *
from colored_text import red


# image_path = input("Введите путь к изображению: ")
def main(image_path):
    try:
        parser = UserInputParser(image_path)
        img_arr, breakpoints = parser.open_image()
        interpreter = PixelInterpreter(img_arr)
        result = interpreter.interpreter()
        return result
    except UnknownColorError as e:
        print(red("Использован недопустимый цвет!"))
    except FileNotFoundError as e:
        print(red("Некорректный путь до изображения!"))
    except Exception as e:
        print(red(e))


if __name__ == "__main__":
    main('/Users/evgeniavolkova/Desktop/уник/питон/piet/test_image/Piet_hello_breakpoints.png')