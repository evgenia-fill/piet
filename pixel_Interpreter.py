import numpy as np
from collections import deque


def get_next_position_in_block(block: set) -> tuple[int, int]:
    return min(block)


def get_colour_by_number(colour: str) -> tuple[int, int] | str:
    colour_dict = {
        'FFC0C0': (0, 0), 'FF0000': (0, 1), 'C00000': (0, 2),  # red
        'FFFFC0': (1, 0), 'FFFF00': (1, 1), 'C0C000': (1, 2),  # yellow
        'C0FFC0': (2, 0), '00FF00': (2, 1), '00C000': (2, 2),  # green
        'C0FFFF': (3, 0), '00FFFF': (3, 1), '00C0C0': (3, 2),  # cyan
        'C0C0FF': (4, 0), '0000FF': (4, 1), '0000C0': (4, 2),  # blue
        'FFC0FF': (5, 0), 'FF00FF': (5, 1), 'C000C0': (5, 2),  # magenta
        'FFFFFF': 'white',
        '000000': 'black'
    }
    return colour_dict.get(colour)


def get_command(curr_color, next_color) -> str | None:
    if curr_color in ('white', 'black', None) or next_color in ('white', 'black', None): return None
    hue = (next_color[0] - curr_color[0]) % 6
    lightness = (next_color[1] - curr_color[1]) % 3
    colour_dict = {
        (0, 1): 'push', (0, 2): 'pop', (1, 0): 'add', (1, 1): 'subtract', (1, 2): 'multiply',
        (2, 0): 'divide', (2, 1): 'mod', (2, 2): 'not', (3, 0): 'greater', (3, 1): 'pointer',
        (3, 2): 'switch', (4, 0): 'duplicate', (4, 1): 'roll', (4, 2): 'in_num',
        (5, 0): 'in_char', (5, 1): 'out_num', (5, 2): 'out_char'
    }
    return colour_dict[(hue, lightness)]


class PixelInterpreter:
    def __init__(self, img_arr: np.array, debug:bool=False):
        self.img_arr = img_arr
        self.height, self.width, _ = img_arr.shape
        self.stack = []
        self.visited = np.zeros((self.height, self.width), dtype=bool)
        self.dir_pointer = 0
        self.cod_chooser = 0
        self.cur_pos = self.find_start()
        self.cur_color = self.get_colour(self.cur_pos)
        self.debug = debug

    def find_start(self) -> tuple[int, int]:
        for y in range(self.height):
            for x in range(self.width):
                if self.get_colour((y, x)) not in ('black', 'white', None): return y, x
        return 0, 0

    def get_colour(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        y, x = pos
        if not (0 <= y < self.height and 0 <= x < self.width): return None
        rgb = tuple(self.img_arr[y, x][:3])
        colour_number = '{:02X}{:02X}{:02X}'.format(rgb[0], rgb[1], rgb[2])
        return get_colour_by_number(colour_number)

    def interpreter(self) -> list[int]:
        while True:
            block = self.get_block(self.cur_pos)
            border = self.get_border(block)
            next_pos = self.step_from_border(border)
            if not next_pos or self.get_colour(next_pos) == 'black':
                if not self.try_rotate(): break
                continue
            next_block = self.get_block(next_pos)
            next_color = self.get_colour(next_pos)
            command = get_command(self.cur_color, next_color)
            if command: self.execute_command(command)
            self.cur_pos = get_next_position_in_block(next_block)
            self.cur_color = next_color
        return self.stack

    def try_rotate(self) -> bool:
        for i in range(8):
            if i % 2 == 0:
                self.cod_chooser = (self.cod_chooser + 1) % 2
            else:
                self.dir_pointer = (self.dir_pointer + 1) % 4
            block = self.get_block(self.cur_pos)
            border = self.get_border(block)
            next_pos = self.step_from_border(border)
            if next_pos and self.get_colour(next_pos) not in ('black', None): return True
        return False

    def step_from_border(self, border):
        dy, dx = [(0, 1), (1, 0), (0, -1), (-1, 0)][self.dir_pointer]
        border_y, border_x = border
        ny, nx = border_y + dy, border_x + dx
        if 0 <= ny < self.height and 0 <= nx < self.width:
            return ny, nx
        return None

    def get_block(self, start_pos: tuple[int, int]) -> set:
        colour = self.get_colour(start_pos)
        visited = set()
        queue = deque([start_pos])
        while len(queue) > 0:
            y, x = queue.popleft()
            if (y, x) in visited: continue
            visited.add((y, x))
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    if self.get_colour((ny, nx)) == colour and (ny, nx) not in visited:
                        queue.append((ny, nx))
        return visited

    def get_border(self, block: set) -> tuple[int, int]:
        return max(block, key=lambda pos: self.border_priority(pos))

    def border_priority(self, pos: tuple[int, int]) -> tuple[int, int]:
        y, x = pos
        if self.dir_pointer == 0: return x, -y if self.cod_chooser == 0 else y  # →
        if self.dir_pointer == 1: return y, x if self.cod_chooser == 0 else -x  # ↓
        if self.dir_pointer == 2: return -x, y if self.cod_chooser == 0 else -y  # ←
        if self.dir_pointer == 3: return -y, -x if self.cod_chooser == 0 else x  # ↑

    def execute_command(self, command: str):
        try:
            if self.debug:
                print(command)
            if command == 'push':
                self.stack.append(len(self.get_block(self.cur_pos)))
            elif command == 'pop':
                self.stack.pop()
            elif command == 'add':
                a, b = self.stack.pop(), self.stack.pop()
                self.stack.append(b + a)
            elif command == 'subtract':
                a, b = self.stack.pop(), self.stack.pop()
                self.stack.append(b - a)
            elif command == 'multiply':
                a, b = self.stack.pop(), self.stack.pop()
                self.stack.append(b * a)
            elif command == 'divide':
                a, b = self.stack.pop(), self.stack.pop()
                self.stack.append(b // a)
            elif command == 'mod':
                a, b = self.stack.pop(), self.stack.pop()
                self.stack.append(b % a)
            elif command == 'not':
                self.stack.append(0 if self.stack.pop() else 1)
            elif command == 'greater':
                a, b = self.stack.pop(), self.stack.pop()
                self.stack.append(1 if b > a else 0)
            elif command == 'duplicate':
                self.stack.append(self.stack[-1])
            elif command == 'roll':
                depth = self.stack.pop()
                rolls = self.stack.pop()
                if depth <= 0 or depth > len(self.stack):
                    return
                sl = self.stack[-depth:]
                rolls = rolls % depth
                self.stack[-depth:] = sl[-rolls:] + sl[:-rolls]
            elif command == 'pointer':
                self.dir_pointer = (self.dir_pointer + self.stack.pop()) % 4
            elif command == 'switch':
                self.cod_chooser = (self.cod_chooser + self.stack.pop()) % 2
            elif command == 'out_num':
                print(self.stack.pop(), end='')
            elif command == 'out_char':
                print(chr(self.stack.pop()), end='')
            elif command == 'in_num':
                self.stack.append(int(input()))
            elif command == 'in_char':
                self.stack.append(ord(input()[0]))
            '''if command not in ['out_num', 'out_char', 'in_num', 'in_char']:
                print(self.stack)'''
        except IndexError:
            pass
