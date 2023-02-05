import framebuf
import gc
import sys


class ImageGenerator:
    image_widths = {
        '-': 12,
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
        '9': 18
    }

    def float_to_image(self, num: float, places: int = 1, size: str = 'lg') -> dict:

        # Convert the number into a string with the defined number of decimal places.
        value_string = '{:.{prec}f}'.format(num, prec=places)

        buffer_width = self.get_buffer_width(value_string)

        if size == 'lg':
            buffer_height = 23
        else:
            buffer_height = 15

        buffer = bytearray((buffer_height * buffer_width) // 8)
        image_buffer = framebuf.FrameBuffer(buffer, buffer_width, buffer_height, framebuf.MONO_HLSB)
        del buffer
        gc.collect()

        buffer_offset = 0
        for character in value_string:
            character_buffer = self.get_frame_buffer(character, size)
            image_buffer.blit(character_buffer['buffer'], buffer_offset, (buffer_height - character_buffer['height']))
            buffer_offset += character_buffer['width']
            del character_buffer
            gc.collect()

        del value_string
        gc.collect()
        return {
            'buffer': image_buffer,
            'offset': buffer_offset
        }

    def get_frame_buffer(self, character: str, size: str) -> dict:
        if size == 'lg':
            if character == '.':
                filename = '../pics/dec.pbm'
            elif character == '-':
                filename = '../pics/neg.pbm'
            else:
                filename = '../pics/{}.pbm'.format(character)
        else:
            if character == '.':
                filename = '../pics/sdec.pbm'
            elif character == '-':
                filename = '../pics/sneg.pbm'
            else:
                filename = '../pics/s{}.pbm'.format(character)

        try:
            with open(filename, 'rb') as f:
                f.readline()  # Magic number
                image_width = int(f.readline())
                image_height = int(f.readline())
                data = bytearray(f.read())
        except EnvironmentError:
            sys.exit()

        fbuf = framebuf.FrameBuffer(data, image_width, image_height, framebuf.MONO_HLSB)
        del data
        gc.collect()

        return {
            'buffer': fbuf,
            'width': image_width,
            'height': image_height
        }

    def get_sym_buffer(self, sym: str) -> framebuf.FrameBuffer:
        filename = '../pics/{}.pbm'.format(sym)

        with open(filename, 'rb') as f:
            f.readline()  # Magic number
            image_width = int(f.readline())
            image_height = int(f.readline())
            data = bytearray(f.read())

        fbuf = framebuf.FrameBuffer(data, image_width, image_height, framebuf.MONO_HLSB)
        del data
        gc.collect()

        return fbuf

    def get_buffer_width(self, value_string: str) -> int:
        buffer_width = 0

        for character in value_string:
            buffer_width += self.image_widths[character]

        return buffer_width
