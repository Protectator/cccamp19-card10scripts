"""
debugPython

This is a custom version of the original menu.py version.
It is only able to run micropython scripts, but it shows the
exception if the script raises an exception.

You can just run it from the original menu.py and then choose
a file to "debug".
"""
import buttons
import color
import display
import os
import leds
import utime

def list_apps():
    """Create a list of available apps."""
    apps = sorted(os.listdir("."))

    # Filter for apps
    apps = [app for app in apps if app.endswith(".py")]

    if "menu.py" in apps:
        apps.remove("menu.py")
        apps.remove("debugPython.py")

    return apps


def button_events():
    """Iterate over button presses (event-loop)."""
    yield 0
    button_pressed = False
    while True:
        v = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT | buttons.TOP_RIGHT)

        if v == 0:
            button_pressed = False

        if not button_pressed and v & buttons.BOTTOM_LEFT != 0:
            button_pressed = True
            yield buttons.BOTTOM_LEFT

        if not button_pressed and v & buttons.BOTTOM_RIGHT != 0:
            button_pressed = True
            yield buttons.BOTTOM_RIGHT

        if not button_pressed and v & buttons.TOP_RIGHT != 0:
            button_pressed = True
            yield buttons.TOP_RIGHT


COLOR1, COLOR2 = ([142, 54, 0], [107, 42, 0])


def draw_menu(disp, applist, idx, offset):
    disp.clear()

    # Wrap around the app-list and draw entries from idx - 3 to idx + 4
    for y, i in enumerate(range(len(applist) + idx - 3, len(applist) + idx + 4)):
        disp.print(
            " " + applist[i % len(applist)] + "      ",
            posy=offset + y * 20 - 40,
            bg=COLOR1 if i % 2 == 0 else COLOR2,
        )

    disp.print(">", posy=20, fg=color.COMMYELLOW, bg=COLOR2 if idx % 2 == 0 else COLOR1)
    disp.update()


def main():
    disp = display.open()
    applist = list_apps()
    numapps = len(applist)
    current = 0
    for ev in button_events():
        if numapps == 0:
            disp.clear(color.COMMYELLOW)
            disp.print(
                " No apps ",
                posx=17,
                posy=20,
                fg=color.COMMYELLOW_DARK,
                bg=color.COMMYELLOW,
            )
            disp.print(
                "available",
                posx=17,
                posy=40,
                fg=color.COMMYELLOW_DARK,
                bg=color.COMMYELLOW,
            )
            disp.update()
            continue

        if ev == buttons.BOTTOM_RIGHT:
            # Scroll down
            draw_menu(disp, applist, current, -8)
            current = (current + 1) % numapps
        elif ev == buttons.BOTTOM_LEFT:
            # Scroll up
            draw_menu(disp, applist, current, 8)
            current = (current + numapps - 1) % numapps
        elif ev == buttons.TOP_RIGHT:
            # Select & start
            disp.clear().update()
            disp.close()
            
            try:
                script_file = open(str(applist[current]), "r")
                script_content_list = script_file.readlines()
                script_content = ''.join(script_content_list)
                exec(script_content)
            except OSError as e:
                print("Loading failed: ", e)
                os.exit(1)
            except Exception as e:
                orange = [255, 106, 0]
                orange_bg = [50, 20, 0]
                black = [0, 0, 0]
                blink_delay = 100
                
                with display.open() as disp:
                    leds.set_all([orange, orange])
                    disp.rect(0,0,160,80,col=orange)
                    disp.update()
                    utime.sleep_ms(blink_delay)
                    leds.set_all([black, black])
                    disp.rect(0,0,160,80,col=black)
                    disp.update()
                    utime.sleep_ms(blink_delay)
                    leds.set_all([orange, orange])
                    disp.rect(0,0,160,80,col=orange)
                    disp.update()
                    utime.sleep_ms(blink_delay)
                    leds.set_all([black, black])
                    disp.rect(0,0,160,80,col=black)
                    disp.update()
                    utime.sleep_ms(blink_delay)
                    leds.set_all([orange, orange])
                    disp.rect(0,0,160,80,col=orange)
                    disp.update()
                    utime.sleep_ms(blink_delay)
                    leds.set_all([black, black])
                    disp.rect(0,0,160,80,col=black)
                    disp.update()
                    utime.sleep_ms(blink_delay)
                    disp.clear()
                    disp.rect(0,0,160,80,col=orange_bg)
                    disp.print(str(e), fg=color.WHITE, bg=orange_bg, posx=0, posy=0)
                    disp.update()
                    disp.close()

        draw_menu(disp, applist, current, 0)


if __name__ == "__main__":
    main()
