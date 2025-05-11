from user_input import UserInputParser

class PixelInterpreter:
    def __init__(self, img_arr):
        self.img_arr = img_arr
        self.stack = []
        self.dir = (0, 0)
        self.start_dir = (0, 1)

    def interpreter(self):
        height, width, _ = self.img_arr.shape
        for y in range(height):
            for x in range(width):
                rgb = tuple(self.img_arr[y, x][:3])
                colour_number = '{:02X}{:02X}{:02X}'.format(rgb[0], rgb[1], rgb[2])
                colour_with_shade = self.get_colour_by_number(colour_number)
                colour = self.normalize_colour(colour_with_shade)
                command = self.get_command_by_colour(colour)
                if command:
                    self.execute_command(command)
        return self.stack

    def normalize_colour(self, colour):
        if 'red' in colour:
            colour = 'red'
        elif 'yellow' in colour:
            colour = 'yellow'
        elif 'green' in colour:
            colour = 'green'
        elif 'cyan' in colour:
            colour = 'cyan'
        elif 'blue' in colour:
            colour = 'blue'
        elif 'magenta' in colour:
            colour = 'magenta'

        return colour

    def get_colour_by_number(self, colour):
        colour_dict = {
            'FFFFFF': 'white',
            '000000': 'black',
            'FFC0C0': 'light red',
            'FF0000': 'red',
            'C00000': 'dark red',
            'FFFFC0': 'light yellow',
            'FFFF00': 'yellow',
            'C0C000': 'dark yellow',
            'C0FFC0': 'light green',
            '00FF00': 'green',
            '00C000': 'dark green',
            'C0FFFF': 'light cyan',
            '00FFFF': 'cyan',
            '00C0C0': 'dark cyan',
            'C0C0FF': 'light blue',
            '0000FF': 'blue',
            '0000C0': 'dark blue',
            'FFC0FF': 'light magenta',
            'FF00FF': 'magenta',
            'C000C0': 'dark magenta'
        }
        return colour_dict.get(colour)

    def get_command_by_colour(self, colour):
        colour_dict = {
            'white': '',  # игнор
            'black': 'stop',
            'red': 'add',  # сложение
            'yellow': 'subtract',  # вычитание
            'green': 'dup',  # дублирование верхнего знач стека
            'cyan': 'swap',  # поменять местами два верхних знач стека
            'blue': 'push',
            'magenta': 'pop'
        }
        return colour_dict.get(colour, '')

    def execute_command(self, command):
        if command == 'push':
            self.stack.append(1)
        elif command == 'pop':
            if self.stack: self.stack.pop()
        elif command == 'add':
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a + b)
        elif command == 'subtract':
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b - a)
        elif command == 'stop':
            return
        elif command == 'dup':
            if self.stack:
                last_value = self.stack[-1]
                self.stack.append(last_value)
        elif command == 'swap':
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(b)
                self.stack.append(a)

        return self.stack