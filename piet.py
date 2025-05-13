from user_input import UserInputParser
from pixel_Interpreter import PixelInterpreter


def main():
    image_path = input("Введите путь к изображению: ")
    parser = UserInputParser(image_path)
    img_arr = parser.open_image()
    interpreter = PixelInterpreter(img_arr)
    result = interpreter.interpreter()


if __name__ == "__main__":
    main()
# /Users/evgeniavolkova/Desktop/уник/питон/Piet/test image/пиет.hello_world.png