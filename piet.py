from user_input import UserInputParser
from pixel_Interpreter import PixelInterpreter


def main():
    a = input("Введите путь к изображению: ")
    img_parser = UserInputParser(a)
    img_arr = img_parser.open_image()
    interpreter = PixelInterpreter(img_arr)
    result_stack = interpreter.interpreter()
    print("Результат стека:", result_stack)


if __name__ == "__main__":
    main()