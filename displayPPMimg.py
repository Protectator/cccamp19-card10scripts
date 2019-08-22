"""
displayPPMimg
Displays a .PPM image on the card10 badge
The PPM has to have the following format :
format: binary (magic number P6)
width: 160px
height: 80px
max value: 255
Author: Kewin Dousse (Protectator)
"""
import color
import display

FILENAME = 'data.ppm'

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def main():
    image_file = open(FILENAME, "rb")
    magic = image_file.readline()
    with display.open() as disp:
        if magic.decode('utf-8')[:2] != "P6":
            disp.print('Incorrect', fg=color.WHITE, bg=color.RED)
            disp.print('image', fg=color.WHITE, bg=color.RED, posy=20)
            disp.print('format', fg=color.WHITE, bg=color.RED, posy=40)
        dimensions = image_file.readline()
        dimensions_array = dimensions.decode('utf-8').split(" ")
        width = dimensions_array[0]
        height = dimensions_array[1]
        max_value = image_file.readline()
        disp.print('Loading img', fg=color.WHITE, bg=color.BLACK)
        disp.print(width, fg=color.WHITE, bg=color.BLACK, posy=20)
        disp.print(height, fg=color.WHITE, bg=color.BLACK, posy=40)
        disp.update()
        for y in range(int(height)):
            for x in range(int(width)):
                r_string = bytes_to_int(image_file.read(1))
                g_string = bytes_to_int(image_file.read(1))
                b_string = bytes_to_int(image_file.read(1))
                pixelColor = [r_string, g_string, b_string]
                disp.pixel(x, y, col=pixelColor)
        disp.update()
        disp.close()
    image_file.close()

if __name__ == "__main__":
    main()
