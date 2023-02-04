import framebuf


class ImageGenerator:
    image_widths = {
        '.': 8,
        '0': 19,
        '1': 17,
        '2': 18,
        '3': 19,
        '4': 21,
        '5': 18,
        '6': 18,
        '7': 20,
        '8': 18,
        '9': 18,
    }

    def float_to_image(self, num: float, places: int = 1, size: str = 'lg', suffix: str = '') -> framebuf.FrameBuffer:

        # Convert the number into a string with the defined number of decimal places.
        value_string = '{:.{prec}f}'.format(num, prec=places)

        buffer_width = self.get_buffer_width(value_string)

        if size == 'lg':
            buffer_height = 23
        else:
            buffer_height = 15

        buffer = bytearray((buffer_height * buffer_width) // 8)
        image_buffer = framebuf.FrameBuffer(buffer, buffer_width, buffer_height, framebuf.MONO_HLSB)

        buffer_offset = 0
        for character in value_string:
            character_buffer = self.get_frame_buffer(character)
            image_buffer.blit(character_buffer['buffer'], buffer_offset, 0)
            buffer_offset += character_buffer['width']

        return image_buffer

    def get_frame_buffer(self, character: str) -> dict:
        if character == '.':
            filename = '../pics/dec.pbm'
        else:
            filename = '../pics/{}.pbm'.format(character)

        with open(filename, 'rb') as f:
            f.readline()  # Magic number
            image_width = int(f.readline())
            image_height = int(f.readline())
            data = bytearray(f.read())

        fbuf = framebuf.FrameBuffer(data, image_width, image_height, framebuf.MONO_HLSB)

        return {
            'buffer': fbuf,
            'width': image_width
        }

    def get_buffer_width(self, value_string: str) -> int:
        buffer_width = 0

        for character in value_string:
            buffer_width += self.image_widths[character]

        return buffer_width
