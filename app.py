# Importing modules for Flask app
from flask import Flask, render_template, request
import json # To retrieve js data
import random # For random light mode

# Declare global light mode and RGB variables
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

# Visualizer function is called when music mode button selected
# Logic sourced from:
# https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
# https://electronicshobbyists.com/raspberry-pi-analog-sensing-mcp3008-raspberry-pi-interfacing/
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

    for i in range(19, -1, -1):
        pixels[i] = (0,0,0)

    global light_mode
    while light_mode == 5:

        # Use sound sensor input to determine LED indexing and output
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

# light_switch function called when any of the other light modes are selected
def light_switch():
    # Reset pixels on LED strips
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, -1, -1):
        pixels[i] = (0,0,0)
    global light_mode
    global rgb_list
    # Make sure one of the light modes is on
    while light_mode != 0:
        rand_prev = 0
        # Light mode 1: random LED
        while light_mode == 1:
            pixels[rand_prev] = (0,0,0)
            rand_num = random.randint(0,19)
            pixels[rand_num] =  (rgb_list[0], rgb_list[1], rgb_list[2])
            rand_prev = rand_num
            sleep(0.1)
            pixels.show()
            print("mode 1")
            print(rgb_list[0])
        # Light mode 2: snake flash
        while light_mode == 2:
            for i in range(19, -1, -1):
                pixels[i] = (rgb_list[0], rgb_list[1], rgb_list[2])
                pixels.show()
                sleep(0.2)
            for i in range(19, -1, -1):
                pixels[i] = (0, 0, 0)
                pixels.show()
                sleep(0.2)
            for i in range(0, 20, 1):
                pixels[i] = (rgb_list[0], rgb_list[1], rgb_list[2])
                pixels.show()
                sleep(0.2)
            for i in range(0, 20, 1):
                pixels[i] = (0, 0, 0)
                pixels.show()
                sleep(0.2)
            print("mode 2")
            print(rgb_list[0])
        # Light mode 3: strobe party
        while light_mode == 3:
            for i in range(19, -1, -1):
                pixels[i] = (0,0,0)
                pixels.show()
            sleep(.5)
            for i in range(19, -1, -1):
                pixels[i] = (rgb_list[0], rgb_list[1], rgb_list[2])
                pixels.show()
                sleep(.002)
            print("mode 3")
            print(rgb_list[0])
        # Light mode 4: illuminate
        while light_mode == 4:
            for i in range(19, -1, -1):
                pixels[i] = (rgb_list[0], rgb_list[1], rgb_list[2])
            pixels.show()
            print("mode 4")
            print(rgb_list[0])
    # Reset the LEDs once more
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, -1, -1):
        pixels[i] = (0,0,0)

# light_switch tester function to ensure button events can enter and exit while loops
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

# Render interface
@app.route("/")
def home():
    return render_template("dashboard.html")

# Receives color_picker events and assign RGB values from colorpicker.js
@app.route("/color_picker", methods =["GET", "POST"])
def color_picker():
    choice = request.data
    color = choice.decode('utf-8')
    global rgb_list
    rgb_list = [int(i) for i in color.split(",")]
    return "ok"

# Receives button1 events and calls light_switch with light_mode = 1
@app.route("/light_mode1_on", methods =["POST"])
def light_mode1_on():
    global light_mode
    light_mode = 1
    light_switch()
    return "ok"

# Resets LEDs and sets light mode to 0
@app.route("/light_mode1_off", methods =["POST"])
def light_mode1_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

# Receives button2 events and calls light_switch with light_mode = 2
@app.route("/light_mode2_on", methods =["POST"])
def light_mode2_on():
    global light_mode
    light_mode = 2
    light_switch()
    return "ok"

# Resets LEDs and sets light mode to 0
@app.route("/light_mode2_off", methods =["POST"])
def light_mode2_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

# Receives button3 events and calls light_switch with light_mode = 3
@app.route("/light_mode3_on", methods =["POST"])
def light_mode3_on():
    global light_mode
    light_mode = 3
    light_switch()
    return "ok"

# Resets LEDs and sets light mode to 0
@app.route("/light_mode3_off", methods =["POST"])
def light_mode3_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

# Receives button4 events and calls light_switch with light_mode = 4
@app.route("/illuminate_on", methods =["POST"])
def illuminate_on():
    global light_mode
    light_mode = 4
    light_switch()
    return "ok"

# Resets LEDs and sets light mode to 0
@app.route("/illuminate_off", methods =["POST"])
def illuminate_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

# Receives button5 events and calls light_switch with light_mode = 5
@app.route("/music_mode_on", methods =["POST"])
def music_mode_on():
    global light_mode
    light_mode = 5
    Visualizer()
    return "ok"

# Resets LEDs and sets light mode to 0
@app.route("/music_mode_off", methods =["POST"])
def music_mode_off():
    GPIO.setmode(GPIO.BCM)
    pixels = neopixel.NeoPixel(board.D18, 20)
    for i in range(19, 0, -1):
        pixels[i] = (0,0,0)
    global light_mode
    light_mode = 0
    return "ok"

# Necessary to run app on localhost
# if __name__ == '__main__':
#     app.run(debug=True)
