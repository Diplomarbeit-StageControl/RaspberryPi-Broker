import paho.mqtt.client as mqtt

broker = "10.0.0.13" 
port = 1883
input_topic = "esp32/movements"
output_topic = "servo/data"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(input_topic)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode()
        print(f"Received data from ESP32: {data}")

        movements = data.split(",")
        x = float(movements[0])

        angle = (x + 8) * 10
        angle = max(0, min(180, angle))
        print(f"Processed angle: {angle}")

        client.publish(output_topic, str(angle))
        print(f"Published angle: {angle} to topic: {output_topic}")

    except Exception as e:
        print(f"Error processing data: {e}")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_forever()
