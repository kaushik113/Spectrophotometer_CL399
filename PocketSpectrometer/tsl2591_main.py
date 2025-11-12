import display
from machine import Pin
from time import sleep_ms
from tsl2591 import Tsl2591, INTEGRATIONTIME_100MS, GAIN_LOW
from m5stack import btnA

# Initialize the TSL2591 sensor.
sensor = Tsl2591(sensor_id=0, integration=INTEGRATIONTIME_100MS, gain=GAIN_LOW)

# Create the TFT display object.
tft = display.TFT()

# Function to display the intensity (lux) value on the screen.
def show_intensity(lux):
    tft.clear(tft.BLACK)
    tft.font(tft.FONT_DejaVu24)
    tft.text(10, 50, "lux:", tft.WHITE)
    tft.text(10, 80, "{:.5f}".format(lux), tft.GREEN)

while True:
    if btnA.wasPressed():
        lux = sensor.sample()  # Get lux reading from TSL2591
        show_intensity(lux)
        print("Intensity (lux):", lux)
    sleep_ms(100)

