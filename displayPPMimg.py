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

def microTry():
    try:
        main()
    except Exception as e:
        ledfx.kitt()
        with display.open() as disp:
            disp.clear()
            disp.print(str(e), fg=color.WHITE, bg=color.BLACK, posx=0, posy=0)
            disp.update()
            disp.close()

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def main():
    image_file = open(FILENAME, "rb")
    image_file.read(14)
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

def sensors():
    light_sensor.start()
    n = 0
    while True:
        n = n + 1
        with display.open() as disp:
            disp.clear()
            level = light_sensor.get_reading()
            disp.print(str(level), fg=color.WHITE, bg=color.BLACK, posx=0, posy=0)

            mapped = level * 160 / 400
            disp.rect(0, 0, int(mapped), 60, col=color.YELLOW)

            disp.update()
            disp.close()

if __name__ == "__main__":
    microTry()