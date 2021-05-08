from flask import Flask, render_template, request
import json
import random

# Importing modules for sensor
import spidev # To communicate with SPI devices
from numpy import interp    # To scale values
from time import sleep  # To add delay
import RPi.GPIO as GPIO # To use GPIO pins
import board
import neopixel


def Visualizer():

    # Start SPI connection
    spi = spidev.SpiDev() # Created an object
    spi.open(0,0)

    # Initializing LED pin as OUTPUT pin
    GPIO.setmode(GPIO.BCM)

    # Initialize the LEDs
    pixels = neopixel.NeoPixel(board.D18, 20)

    # Read MCP3008 data
    def analogInput(channel):
        spi.max_speed_hz = 1350000
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

    previous_output=0

    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)

    while True:

        output = analogInput(0) # Reading from CH0
        output = interp(output, [0, 200], [0, 20])
        output = int(output.item())

        if (previous_output > output):
            pixels_to_clear = previous_output-output
            for i in range(previous_output-1, previous_output-pixels_to_clear-1, -1):
                pixels[i] = (0,0,0)

        for i in range(output):
            if (i<10):
                blue = int(255-i*25.5)
                green = int(i*25.5)
                pixels[i] = (0,green,blue)

            if (i>=10):
                red = int((i-10)*25.5)
                green = int(255-(i-10)*25.5)
                pixels[i] = (red,green,0)

        pixels.show()
        previous_output = output

def Light_Modes(color, pattern):
    mode = pattern
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    if mode == 1:
        rand_num = random.randint(0,19)
        while True:
            for i in range(19, 0, -1):
                pixels[i] = (0,0,0)
            for i in range(rand_num, 0, -1):
                pixels[i] = (color[0], color[1], color[2])
            sleep(0.1)
            pixels.show()

    elif mode == 2:
        while True:
            for i in range(19, 0, -1):
                pixels[i] = (0,0,0)
            for i in range(19, 0, -1):
                pixels[i] = (color[0], color[1], color[2])
                sleep(0.2)
            for i in range(0, 19, 1):
                pixels[i] = (color[0], color[1], color[2])
                sleep(0.2)
            pixels.show()

    elif mode == 3:
        while True:
            for i in range(19, 0, -1):
                pixels[i] = (0,0,0)
            for i in range(19, 0 -1):
                pixels[i] = (color[0], color[1], color[2])
            sleep(.5)
            pixels.show()

    elif mode == 4:
        while True:
            for i in range(19, 0, -1):
                pixels[i] = (color[0], color[1], color[2])
            pixels.show()

    else:
        while True:
            for i in range(19, 0, -1):
                pixels[i] = (0,0,0)
            pixels.show()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/color_picker", methods =["GET", "POST"])
def color_picker():
    choice = request.data
    color = choice.decode('utf-8')
    global rgb_list = [int(i) for i in color.split(",")]
    return "ok"

@app.route("/light_mode1_on", methods =["POST"])
def light_mode1_on():
    Light_Modes(rgb_list, 1)
    return "ok"

@app.route("/light_mode1_off", methods =["POST"])
def light_mode1_off():
    Light_Modes(rgb_list, 5)
    return "ok"

@app.route("/light_mode2_on", methods =["POST"])
def light_mode2_on():
    Light_Modes(rgb_list, 2)
    return "ok"

@app.route("/light_mode2_off", methods =["POST"])
def light_mode2_off():
    Light_Modes(rgb_list, 5)
    return "ok"

@app.route("/light_mode3_on", methods =["POST"])
def light_mode3_on():
    Light_Modes(rgb_list, 3)
    return "ok"

@app.route("/light_mode3_off", methods =["POST"])
def light_mode3_off():
    Light_Modes(rgb_list, 5)
    return "ok"

@app.route("/illuminate_on", methods =["POST"])
def illuminate_on():
    Light_Modes(rgb_list, 4)
    return "ok"

@app.route("/illuminate_off", methods =["POST"])
def illuminate_off():
    Light_Modes(rgb_list, 5)
    return "ok"

@app.route("/music_mode_on", methods =["POST"])
def music_mode_on():
    Visualizer()
    return "ok"

@app.route("/music_mode_off", methods =["POST"])
def music_mode_off():
    Light_Modes(rgb_list, 5)
    return "ok"

# if __name__ == '__main__':
#     app.run(debug=True)
