from paho.mqtt import client as mqtt_client

MQTT_BROKER="10.0.0.212" # placeholder value
MQTT_PORT=1883
MQTT_TOPIC="wled/001/api"
MQTT_CLIENT_ID="TVAL-001"
MQTT_USERNAME="homeassistant" # placeholder value
MQTT_PASSWORD="Uekaiphee7shieKaiThaenau3aedaegheigahru6Heejausohpeid0joh3eicohd" # placeholder value

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

class MQTTClient:

    def __init__(self) -> None:
        # Set Connecting Client ID
        client = mqtt_client.Client(MQTT_CLIENT_ID)
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        client.on_connect = on_connect
        client.connect(MQTT_BROKER, MQTT_PORT)
        self.client = client


    def publish(self, msg):
        if self.client != None:
            result = self.client.publish(MQTT_TOPIC, msg)
            return result
        else:
            print("Client is not connected to MQTT Broker at: "+ str(MQTT_BROKER))

