import paho.mqtt.client as mqtt
import psutil as ps
import time
def on_connect(client, userdata, flags, resultCode):
    print('Client is connnected')

client = mqtt.Client()
client.on_connect = on_connect
client.connect('broker.emqx.io', 1883, 60);

while True:
    ram_status = ps.virtual_memory().percent
    cpu_status = ps.cpu_percent()
    payload = str(ram_status) + ','+str(cpu_status)
    print('send data to client successfully')
    client.publish('raspi/topic', payload= payload, qos = 0, retain=False)
    time.sleep(1)

client.loop_forever()
