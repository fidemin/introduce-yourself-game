import numpy as np
from PIL import Image


class AsciiView:
    # From: http://paulbourke.net/dataformats/asciiart/
    # 70 levels of gray scale
    GRAY_SCALES = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '

    def __init__(self, file_name):
        self._image = Image.open(file_name).convert('L')

    def convert(self, cols=80, scale=0.43):
        width, height = self._image.size[0], self._image.size[1]
        width_of_tile = width/cols
        height_of_tile = width_of_tile/scale
        rows = int(height/height_of_tile)
        if cols > width or rows > height:
            raise ValueError('image is too small to convert with given cols and scale')

        ascii_image_array = []

        for j in range(rows):
            y1 = int(j * height_of_tile)
            y2 = int((j + 1) * height_of_tile)

            # if last row, extends y2 to height
            if j == rows-1:
                y2 = height

            ascii_image_row_array = []
            for i in range(cols):
                x1 = int(i * width_of_tile)
                x2 = int((i + 1) * width_of_tile)

                # if last col, extends x2 to width
                if i == cols-1:
                    x2 = width

                cropped_image = self._image.crop((x1, y1, x2, y2))
                avg = int(self._average_gray_scale(cropped_image))
                gray_scale_value = self.GRAY_SCALES[int((avg * 69) / 255)]

                ascii_image_row_array.append(gray_scale_value)
            ascii_image_array.append(''.join(ascii_image_row_array))

        return '\r\n'.join(ascii_image_array)

    def _average_gray_scale(self, image):
        image_array = np.array(image)
        w, h = image_array.shape
        return np.average(image_array.reshape(w*h))
