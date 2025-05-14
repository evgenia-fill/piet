def rgb_from_hex(hex_color: str) -> tuple[int, int, int]:
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return r, g, b
    except ValueError:
        return None


def colored_text(text, *args) -> str:
    if len(args) == 3 and all(type(el) == int and 0 <= el <= 255 for el in args):
        r, g, b = args
        color_code = f"\033[38;2;{r};{g};{b}m"
    elif len(args) == 1 and type(args[0]) == str:
        r, g, b = rgb_from_hex(args[0])
        color_code = f"\033[38;2;{r};{g};{b}m"
        if color_code == None:
            return text
    else:
        return text
    reset_code = "\033[0m"
    return color_code + text + reset_code


def create_text_brush(hex_color: str) -> callable:
    def res(text):
        return colored_text(text, hex_color)
    return res


light_red = create_text_brush("FFC0C0")
red = create_text_brush("FF0000")
dark_red = create_text_brush("C00000")

light_yellow = create_text_brush("FFFFC0")
yellow = create_text_brush("FFFF00")
dark_yellow = create_text_brush("C0C000")

light_green = create_text_brush("C0FFC0")
green = create_text_brush("00FF00")
dark_green = create_text_brush("00C000")

light_cyan = create_text_brush("C0FFFF")
cyan = create_text_brush("00FFFF")
dark_cyan = create_text_brush("00C0C0")

light_blue = create_text_brush("C0C0FF")
blue = create_text_brush("0000FF")
dark_blue = create_text_brush("0000C0")

light_magenta = create_text_brush("FFC0FF")
magenta = create_text_brush("FF00FF")
dark_magenta = create_text_brush("C000C0")

black = create_text_brush("000000")
white = lambda text: text