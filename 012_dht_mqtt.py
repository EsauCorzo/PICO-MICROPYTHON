from machine import Pin, I2C
from time import sleep, ticks_ms, ticks_diff
from dht import DHT22
from network import WLAN, STA_IF
from umqtt.simple import MQTTClient
from ujson import dumps
import credentials

# WiFi credentials
SSID = credentials.SSID
PASSWORD = credentials.PASSWORD

# MQTT server
MQTT_SERVER = "10.9.141.1"
MQTT_TOPIC = "/home/pico/micropython"
MQTT_ID = "Micropython Pico Node"

# DHT sensor setup
DHT_PIN = 16
dht_sensor = DHT22(Pin(DHT_PIN))

# Timing variables
INTERVAL = 30000  # 30 seconds
previous_ticks = 0

# Connect to WiFi
def connect_to_wifi():
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        sleep(0.5)
    print("Connected to WiFi:", wlan.ifconfig())

def main():
    # Connect to WiFi
    connect_to_wifi()
    
    # Setup MQTT
    client = MQTTClient(MQTT_ID, MQTT_SERVER)
    client.connect()

    global previous_ticks
    while True:
        # Update current time
        current_ticks = ticks_ms()
        
        if ticks_diff(current_ticks, previous_ticks) >= INTERVAL:
            # Update last reading time
            previous_ticks = current_ticks

            # Read temperature and humidity
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()

            # Create JSON payload
            payload = dumps({"node_id":MQTT_ID,"temp": temperature, "hum": humidity})

            # Publish to MQTT
            client.publish(MQTT_TOPIC, payload)

            # Debug output
            print(payload)

main()