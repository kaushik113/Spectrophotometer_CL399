import display
from machine import I2C, Pin
from time import sleep_ms
import math
from as7341 import *
from m5stack import btnA

# Initialize I2C and AS7341 sensor
i2c = I2C(sda=Pin(32), scl=Pin(33))

sensor = AS7341(i2c)
if not sensor.isconnected():
    print("Failed to contact AS7341, terminating")
    sys.exit(1)

sensor.set_measure_mode(AS7341_MODE_SPM)
sensor.set_atime(29)   # 30 ASTEPS
sensor.set_astep(599)  # 1.67 ms
sensor.set_again(4)    # Factor 8 (with enough light)

# Create the TFT display object
tft = display.TFT()

# Function to calibrate reference intensity (I0)
def calibrate_reference():
    tft.clear(tft.BLACK)
    tft.font(tft.FONT_DejaVu24)
    tft.text(10, 30, "Calibration Mode", tft.WHITE)
    tft.text(10, 60, "Place in Open Air", tft.YELLOW)
    tft.text(10, 90, "Press Button", tft.CYAN)

    print("Place sensor in open air or near a white surface.")
    print("Press button to capture reference intensity.")

    while True:
        if btnA.wasPressed():
            print("Capturing reference intensity...")
            sensor.set_led_current(25)  # Turn on LED
            sensor.enable_led(True)

            # Measure reference intensity (no sample)
            sensor.start_measure("F5F8CN")
            _, _, _, F8_ref, _, _ = sensor.get_spectral_data()

            sensor.enable_led(False)  # Turn off LED

            print("I0 (Red):", F8_ref)
            tft.clear(tft.BLACK)
            tft.text(10, 50, "I0 (Red):", tft.WHITE)
            tft.text(10, 80, str(F8_ref), tft.RED)
            sleep_ms(2000)

            return F8_ref  # Return the reference intensity

        sleep_ms(100)

# Run calibration to get I0
I0_red = calibrate_reference()

# Function to display both the absorbance and the equation's output
def display_result(absorbance, output):
    tft.clear(tft.BLACK)
    tft.font(tft.FONT_DejaVu24)
    tft.text(10, 30, "Abs:", tft.WHITE)
    tft.text(10, 60, "{:.4f}".format(absorbance), tft.RED)
    tft.text(10, 100, "Output:", tft.WHITE)
    tft.text(10, 130, "{:.4f}".format(output), tft.GREEN)

try:
    while True:
        if btnA.wasPressed():  # Check if the button is pressed
            print("Turning on LED")
            sensor.set_led_current(25)  # Set LED current to 25mA
            sensor.enable_led(True)

            # Perform spectral measurement
            sensor.start_measure("F5F8CN")
            _, _, _, F8, _, _ = sensor.get_spectral_data()

            # Calculate absorbance of red (F8)
            if I0_red > 0 and F8 > 0:
                absorbance_red = -math.log10(F8 / I0_red)
            else:
                absorbance_red = 0  # Avoid division errors

            # Plug the absorbance value into the equation: 7.215x^2 + 0.6133x + 0.0872
            eq_output = 7.215 * (absorbance_red ** 2) + 0.6133 * absorbance_red + 0.0872

            # Display the results on the TFT
            display_result(absorbance_red, eq_output)
            print("Absorbance (Red):", absorbance_red)
            print("Equation Output:", eq_output)

            print("Turning off LED")
            sensor.enable_led(False)  # Turn off the LED after measurement
        sleep_ms(100)

except KeyboardInterrupt:
    print("Interrupted from keyboard")

sensor.disable()

