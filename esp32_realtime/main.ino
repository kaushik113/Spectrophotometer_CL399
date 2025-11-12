#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Wire.h>
#include <Adafruit_TSL2591.h>

#define SERVICE_UUID        "12345678-1234-5678-1234-56789abcdef0"  // ✅ Unique Service UUID
#define CHARACTERISTIC_UUID "87654321-4321-8765-4321-abcdef987654"  // ✅ Unique Characteristic UUID

Adafruit_TSL2591 tsl = Adafruit_TSL2591(2591);
BLECharacteristic *pCharacteristic;

void setup() {
    Serial.begin(115200);
    BLEDevice::init("ESP32_LightSensor");  // ✅ Advertise ESP32 Name

    BLEServer *pServer = BLEDevice::createServer();
    BLEService *pService = pServer->createService(SERVICE_UUID);

    pCharacteristic = pService->createCharacteristic(
                        CHARACTERISTIC_UUID,
                        BLECharacteristic::PROPERTY_READ | 
                        BLECharacteristic::PROPERTY_NOTIFY
                      );

    pCharacteristic->addDescriptor(new BLE2902());  // ✅ Enable notifications
    pService->start();

    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->start();

    Serial.println("✅ BLE Advertising Started...");

    // ✅ Setup TSL2591 Sensor
    if (!tsl.begin()) {
        Serial.println("❌ TSL2591 not found! Check connections.");
        while (1);
    }
    tsl.setGain(TSL2591_GAIN_HIGH);
    tsl.setTiming(TSL2591_INTEGRATIONTIME_300MS);
}

void loop() {
    int lum = tsl.getLuminosity(TSL2591_VISIBLE);  // ✅ Read luminosity
    String jsonData = "{\"time\":" + String(millis()) + ",\"luminosity\":" + String(lum) + "}";

    Serial.println(jsonData);
    pCharacteristic->setValue(jsonData.c_str());
    pCharacteristic->notify();  // ✅ Send BLE data

    delay(500);  // ✅ Send every 500ms
}
