from user_input import UserInputParser
from pixel_Interpreter import PixelInterpreter


def main():
    image_path = input("Введите путь к изображению: ")
    parser = UserInputParser(image_path)
    img_arr = parser.open_image()
    interpreter = PixelInterpreter(img_arr)
    try:
        result = interpreter.interpreter()
        print(result)
    except ValueError as e:
        print("Использован недопустимый цвет!")


if __name__ == "__main__":
    main()