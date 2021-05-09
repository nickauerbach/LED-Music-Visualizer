from flask import Flask, render_template, request
import json
import random

global rgb_list
rgb_list = [1,2,3]
global light_mode

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

    global light_mode
    while light_mode == 5:

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

def light_switch():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    global rgb_list
    while light_mode != 0:
        if light_mode == 1:
            while light_mode == 1:
                rand_num = random.randint(0,19)
                for i in range(19, 0, -1):
                    pixels[i] = (0,0,0)
                for i in range(rand_num, 0, -1):
                    pixels[i] = (color[0], color[1], color[2])
                sleep(0.1)
                pixels.show()
                print("mode 1")
        elif light_mode == 2:
            while light_mode == 2:
                for i in range(19, 0, -1):
                    pixels[i] = (0,0,0)
                for i in range(19, 0, -1):
                    pixels[i] = (color[0], color[1], color[2])
                    sleep(0.2)
                for i in range(0, 19, 1):
                    pixels[i] = (color[0], color[1], color[2])
                    sleep(0.2)
                pixels.show()
                print("mode 2")
        elif light_mode == 3:
            while light_mode == 3:
                for i in range(19, 0, -1):
                    pixels[i] = (0,0,0)
                for i in range(19, 0 -1):
                    pixels[i] = (color[0], color[1], color[2])
                sleep(.5)
                pixels.show()
                print("mode 3")
        elif light_mode == 4:
            while light_mode == 4:
                for i in range(19, 0, -1):
                    pixels[i] = (color[0], color[1], color[2])
                pixels.show()
                print("mode 4")

# def light_switch():
#     global light_mode
#     global rgb_list
#     while light_mode != 0:
#         if light_mode == 1:
#             while light_mode == 1:
#                 print("mode 1")
#                 print(rgb_list[0])
#         elif light_mode == 2:
#             while light_mode == 2:
#                 print("mode 2")
#                 print(rgb_list[0])
#         elif light_mode == 3:
#             while light_mode == 3:
#                 print("mode 3")
#                 print(rgb_list[0])
#         elif light_mode == 4:
#             while light_mode == 4:
#                 print("mode 4")
#                 print(rgb_list[0])
#         elif light_mode == 5:
#             while light_mode ==5:
#                 print ("mode 5")
#                 print(rgb_list[0])

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/color_picker", methods =["GET", "POST"])
def color_picker():
    choice = request.data
    color = choice.decode('utf-8')
    global rgb_list
    rgb_list = [int(i) for i in color.split(",")]
    return "ok"

@app.route("/light_mode1_on", methods =["POST"])
def light_mode1_on():
    global light_mode
    light_mode = 1
    light_switch()
    return "ok"

@app.route("/light_mode1_off", methods =["POST"])
def light_mode1_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

@app.route("/light_mode2_on", methods =["POST"])
def light_mode2_on():
    global light_mode
    light_mode = 2
    light_switch()
    return "ok"

@app.route("/light_mode2_off", methods =["POST"])
def light_mode2_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

@app.route("/light_mode3_on", methods =["POST"])
def light_mode3_on():
    global light_mode
    light_mode = 3
    light_switch()
    return "ok"

@app.route("/light_mode3_off", methods =["POST"])
def light_mode3_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

@app.route("/illuminate_on", methods =["POST"])
def illuminate_on():
    global light_mode
    light_mode = 4
    light_switch()
    return "ok"

@app.route("/illuminate_off", methods =["POST"])
def illuminate_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

@app.route("/music_mode_on", methods =["POST"])
def music_mode_on():
    global light_mode
    light_mode = 5
    Visualizer()
    return "ok"

@app.route("/music_mode_off", methods =["POST"])
def music_mode_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
