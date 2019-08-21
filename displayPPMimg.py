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
import ledfx

FILENAME = 'data.ppm'

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def main():
    image_file = open(FILENAME, "rb")
    magic = image_file.read(8)
    width = image_file.read(2)
    height = image_file.read(2)
    max_value = image_file.read(2)
    with display.open() as disp:
        for y in range(80):
            for x in range(160):
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
