import asyncio
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from bleak import BleakClient

# Replace with your ESP32's BLE MAC address
ESP32_ADDRESS = "A0:B7:65:48:2C:76"
CHARACTERISTIC_UUID = "87654321-4321-8765-4321-abcdef987654"

time_data = []
luminosity_data = []
client = None

async def read_ble_data():
    """Reads BLE notifications from ESP32."""
    global client
    client = BleakClient(ESP32_ADDRESS)
    await client.connect()
    print("✅ Connected to ESP32!")

    async def notification_handler(sender, data):
        """Handles incoming BLE data and updates lists."""
        try:
            decoded_data = json.loads(data.decode("utf-8"))
            time_data.append(decoded_data["time"] / 1000)  # Convert ms to seconds
            luminosity_data.append(decoded_data["luminosity"])
            print(f"Time: {time_data[-1]}s, Luminosity: {luminosity_data[-1]}")
        except Exception as e:
            print("Error decoding JSON:", e)

    await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
    await asyncio.sleep(60)  # Keep listening for 60 seconds
    await client.stop_notify(CHARACTERISTIC_UUID)

async def main():
    """Main function to start BLE reading and real-time plotting."""
    await read_ble_data()

# Start BLE communication in the event loop
asyncio.run(main())

# Live update plot function
def update_plot(frame):
    """Updates the plot with the latest BLE data."""
    plt.cla()  # Clear the plot
    plt.plot(time_data, luminosity_data, marker="o", linestyle="-", color="b")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Luminosity")
    plt.title("Real-time Luminosity Data")
    plt.grid()

# Create animated plot
fig = plt.figure()
ani = animation.FuncAnimation(fig, update_plot, interval=500)

# Show the plot
plt.show()
