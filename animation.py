import math
from subprocess import call


def clear_screen():
    call('clear')


class Animator:
    def __init__(self, init_str, width=100, height=50):
        # put string to middle of width X height
        lines = init_str.split('\r\n')
        len_lines = len(lines)
        if len_lines > height:
            raise ValueError('given string height should be smaller than height')

        half = (height - len_lines) / 2
        upper_rows_length = math.ceil(half)
        bottom_rows_length = int(half)

        self._init_matrix = []
        for _ in range(upper_rows_length):
            self._init_matrix.append(width * [' '])

        for line in lines:
            row = list(line)
            if len(row) > width:
                raise ValueError('given string length should be smaller than length')
            self._init_matrix.append(self._extend_row_to_width(width, row))

        for _ in range(bottom_rows_length):
            self._init_matrix.append(width * [' '])

        self._width = 100
        self._height = 50
        self._x = 0
        self._y = 0

    def _extend_row_to_width(self, width, init_row):
        init_row_length = len(init_row)
        half = (width - init_row_length) / 2
        front_spaces = math.ceil(half)
        back_spaces = int(half)
        return [' '] * front_spaces + init_row + [' '] * back_spaces

    def to_string(self):
        x = self._x
        y = self._y
        lines = []

        if y > 0:
            matrix = self._init_matrix[y:] + [[' '] * self._width for _ in range(min(y, self._height))]
        elif y < 0:
            matrix = [[' '] * self._width for _ in range(min(-y, self._height))] + self._init_matrix[:y]
        else:
            matrix = self._init_matrix

        for row in matrix:
            if x < 0:
                line = ''.join(row[-x:] + min(-x, self._width) * [' '])
            elif x > 0:
                line = ''.join(min(x, self._width) * [' '] + row[:-x])
            else:
                line = ''.join(row)
            lines.append(line)
        return '\r\n'.join(lines)

    def move(self, x, y):
        self._x += x
        self._y += y
