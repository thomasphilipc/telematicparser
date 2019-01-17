import paho.mqtt.client as mqtt


def process(data):
    return data.split('/')[1]

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/+/test")

def on_message(client, userdata, msg):
  print("{} from {}".format(msg.payload.decode(),process(msg.topic)))


client = mqtt.Client()
client.connect("broker.hivemq.com")

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

client.disconnect()
