# card10slide
# by @scy
# see https://github.com/scy/card10slide

import display
import os
import utime

WIDTH = 160
HEIGHT = 80

IMAGE_DIR = "/slideshow"

def render_error(err1, err2):
    with display.open() as disp:
        disp.clear()
        disp.print(err1, posx=80 - round(len(err1) / 2 * 14), posy=18)
        disp.print(err2, posx=80 - round(len(err2) / 2 * 14), posy=42)
        disp.update()
        disp.close()

def test_image():
    with display.open() as d:
        for x in range(WIDTH):
            for y in range(HEIGHT):
                d.pixel(x, y, col=(0, x, y))
        d.update()

def read_number(file):
    buffer = ""
    ignore_until_newline = False
    while True:
        byte = file.read(1)
        if ignore_until_newline:
            if byte == "\r" or byte == "\n":
                ignore_until_newline = False
        elif byte >= "0" and byte <= "9":
            buffer += byte
        elif byte == "#": # comment
            ignore_until_newline = True
        elif buffer != "": # we already have some digits and now a non-digit
            return int(buffer)

def render_ppm(filename):
    with open(filename, "r") as file:
        try:
            if file.read(2) != "P6":
                raise RuntimeError("no P6 file")
            if read_number(file) != WIDTH:
                raise RuntimeError("width != " + str(WIDTH))
            if read_number(file) != HEIGHT:
                raise RuntimeError("height != " + str(HEIGHT))
            max_color = read_number(file)
            if max_color < 1 or max_color > 255:
                raise RuntimeError("8bit only")
            with display.open() as d:
                for y in range(HEIGHT):
                    row = bytearray(file.read(3 * WIDTH))
                    for x in range(WIDTH):
                        offset = 3 * x
                        d.pixel(x, y, col=(row[offset], row[offset + 1], row[offset + 2]))
                d.update()
        except RuntimeError as e:
            render_error(filename, str(e))

def run_slideshow():
    filenames = list(filter(lambda filename: filename.endswith(".ppm"), os.listdir(IMAGE_DIR)))
    while True:
        for filename in filenames:
            render_ppm(IMAGE_DIR + "/" + filename)
            utime.sleep(15)

run_slideshow()
