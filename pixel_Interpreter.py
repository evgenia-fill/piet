import numpy as np
from collections import deque
from errors import UnknownColorError
from colored_text import colored_text
from typing import Iterable


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
    def __init__(self, img_arr: np.array, 
                 debug:bool=False, 
                 step_by_step:bool=False, 
                 breakpoints: Iterable[tuple[int, int]] = [],
                 breakpoint_mode: str = 'some'):
        self.img_arr = img_arr
        self.height, self.width, _ = img_arr.shape
        self.stack = []
        self.visited = np.zeros((self.height, self.width), dtype=bool)
        self.dir_pointer = 0
        self.cod_chooser = 0
        self.block = set()
        self.cur_pos = self.find_start()
        self.cur_color = self.get_colour(self.cur_pos)
        self.physical_cur_color = self.get_physical_colour(self.cur_pos)
        
        self.debug = debug
        self.output = ""
        self.step_by_step = step_by_step
        self.breakpoints = set(breakpoints)
        if breakpoint_mode == 'all':
            for y in range(self.height):
                for x in range(self.width):
                    self.breakpoints.add((y, x))
        self.breakpoint_found = False
        self.next_color = None
        self.physical_next_color = '000000'

    def find_start(self) -> tuple[int, int]:
        for y in range(self.height):
            for x in range(self.width):
                if self.get_colour((y, x)) not in ('black', 'white', None): return y, x
        return 0, 0
    
    def to_hex_colour(self, rgb: tuple[int, int, int]):
        return '{:02X}{:02X}{:02X}'.format(rgb[0], rgb[1], rgb[2])

    def get_colour(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        y, x = pos
        if not (0 <= y < self.height and 0 <= x < self.width): return None
        rgb = tuple(self.img_arr[y, x][:3])
        colour_number = self.to_hex_colour(rgb)
        colour = get_colour_by_number(colour_number)
        if colour is None: raise UnknownColorError
        return colour

    def interpreter(self) -> str:
        while True:            
            self.block = self.get_block(self.cur_pos)
            border = self.get_border(self.block)
            next_pos = self.step_from_border(border)
            if not next_pos or self.get_colour(next_pos) == 'black':
                if not self.try_rotate(): break
                continue
            
            next_block = self.get_block(next_pos)
            self.next_color = self.get_colour(next_pos)
            self.physical_next_color = self.get_physical_colour(next_pos)
            if self.debug and self.breakpoint_found:
                self.print_debug_info()
            command = get_command(self.cur_color, self.next_color)
            if command: self.execute_command(command)
            
            self.cur_pos = get_next_position_in_block(next_block)
            self.cur_color = self.next_color
            self.physical_cur_color = self.physical_next_color
            
            if self.step_by_step and self.breakpoint_found:
                input()
        return self.output

    def get_physical_colour(self, pos: tuple[int, int]) -> str:
        rgb = tuple(self.img_arr[*pos][:3])
        return self.to_hex_colour(rgb)

    @property
    def str_direction(self) -> str:
        directions = ['→', '↓', '←', '↑']
        return directions[self.dir_pointer]
    
    @property
    def str_cod_chooser(self) -> str:
        if self.dir_pointer == 0 and self.cod_chooser == 0 or self.dir_pointer == 1 and self.cod_chooser == 1:
            return '↘'
        elif self.dir_pointer == 1 and self.cod_chooser == 0 or self.dir_pointer == 2 and self.cod_chooser == 1:
            return '↙'
        elif self.dir_pointer == 2 and self.cod_chooser == 0 or self.dir_pointer == 3 and self.cod_chooser == 1:
            return '↖'
        elif self.dir_pointer == 3 and self.cod_chooser == 0 or self.dir_pointer == 0 and self.cod_chooser == 1:
            return '↗'
    
    def print_debug_info(self):
        res = f'{self.cur_pos} {colored_text(self.physical_cur_color, self.physical_cur_color)}->' + \
              f'{colored_text(self.physical_next_color, self.physical_next_color)} ' + \
              f'{self.str_direction}{self.str_cod_chooser}'
        print(res)

    def try_rotate(self) -> bool:
        for i in range(8):
            if i % 2 == 0:
                self.cod_chooser = (self.cod_chooser + 1) % 2
            else:
                self.dir_pointer = (self.dir_pointer + 1) % 4
            # block = self.get_block(self.cur_pos)
            border = self.get_border(self.block)
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
        self.breakpoint_found = False
        while len(queue) > 0:
            y, x = queue.popleft()
            if (y, x) in visited: continue
            if not self.breakpoint_found and (y, x) in self.breakpoints:
                self.breakpoint_found = True
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
            if self.debug and self.breakpoint_found and command != 'push':
                print(command, end=" ")
            if command == 'push':
                value = len(self.block)
                if self.debug and self.breakpoint_found:
                    print(f'push {value}', end="")
                self.stack.append(value)
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
                rolls = self.stack.pop()
                depth = self.stack.pop()
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
                n = self.stack.pop()
                print(n, end='')
                self.output += str(n)
            elif command == 'out_char':
                ch = chr(self.stack.pop())
                print(ch, end='')
                self.output += ch
            elif command == 'in_num':
                self.stack.append(int(input()))
            elif command == 'in_char':
                self.stack.append(ord(input()[0]))
            if self.debug and self.breakpoint_found:
                print()
            if self.debug and self.breakpoint_found:
                end = "" if self.step_by_step else "\n"
                print(self.stack, end=end)
        except IndexError:
            pass
