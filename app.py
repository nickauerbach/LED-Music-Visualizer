from flask import Flask, render_template, request
import json

#initialize Flask app
app = Flask(__name__)

# # Importing modules for sensor
# import spidev # To communicate with SPI devices
# from numpy import interp    # To scale values
# from time import sleep  # To add delay
# import RPi.GPIO as GPIO # To use GPIO pins
# import board
# import neopixel
#
# def Visualizer():
#
#     # Start SPI connection
#     spi = spidev.SpiDev() # Created an object
#     spi.open(0,0)
#
#     # Initializing LED pin as OUTPUT pin
#     GPIO.setmode(GPIO.BCM)
#
#     # Initialize the LEDs
#     pixels = neopixel.NeoPixel(board.D18, 20)
#
#     # Read MCP3008 data
#     def analogInput(channel):
#         spi.max_speed_hz = 1350000
#         adc = spi.xfer2([1,(8+channel)<<4,0])
#         data = ((adc[1]&3) << 8) + adc[2]
#         return data
#
#     output = 0
#
#     while True:
#         for i in range(19, 0, -1):
#             pixels[i] = (0,0,0)
#         output = analogInput(0) # Reading from CH0
#         output = interp(output, [0, 200], [0, 20])
#         output = int(output.item())
#         print(output)
#         for i in range(output):
#             pixels[i] = (255,0,0)
#         sleep(0.1)
#         pixels.show()

# def Light_Modes(mode):
#     int mode = mode
#     switch(mode) {
#
#     }


@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/light_mode1_on", methods =["POST"])
def light_mode1_on():
    print("#1 on")
    return "ok"

@app.route("/light_mode1_off", methods =["POST"])
def light_mode1_off():
    print("#1 off")
    return "ok"

@app.route("/light_mode2_on", methods =["POST"])
def light_mode2_on():
    print("#2 on")
    return "ok"

@app.route("/light_mode2_off", methods =["POST"])
def light_mode2_off():
    print("#2 off")
    return "ok"

@app.route("/light_mode3_on", methods =["POST"])
def light_mode3_on():
    print("#3 on")
    return "ok"

@app.route("/light_mode3_off", methods =["POST"])
def light_mode3_off():
    print("#3 off")
    return "ok"

@app.route("/illuminate_on", methods =["POST"])
def illuminate_on():
    print("#4 on")
    return "ok"

@app.route("/illuminate_off", methods =["POST"])
def illuminate_off():
    print("#4 off")
    return "ok"

@app.route("/music_mode_on", methods =["POST"])
def music_mode_on():
    print("#5 on")
    return "ok"

@app.route("/music_mode_off", methods =["POST"])
def music_mode_off():
    print("#5 off")
    return "ok"

@app.route("/color_picker", methods =["GET", "POST"])
def color_picker():
    choice = request.data
    color = choice.decode('utf-8')
    rgb_list = color.split(",")
    rgb_list = [int(i) for i in rgb_list]
    return rgb_list

if __name__ == "__main__":
    app.run(debug=True)
