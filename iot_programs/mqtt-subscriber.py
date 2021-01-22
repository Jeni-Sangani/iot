import paho.mqtt.client as mqtt
import time
import sqlite3

connection = sqlite3.connect('sensor.db')

def on_connect(client, userdata, flags, resultCode):
    print('Connected with client')
    client.subscribe('raspi/topic')
    table_cursor = connection.cursor()
    table_cursor.execute('''
        CREATE TABLE IF NOT EXISTS cpu_ram_status(
            STATUS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CPU_STATUS TEXT,
            RAM_STATUS TEXT,
            LOGTIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
def on_message(client, userdata, message):
    payload_data = message.payload.decode('utf-8')
    payload_array = payload_data.split(',')
    ram_status = payload_array[0]
    cpu_status = payload_array[1]
    record_cursor = connection.cursor()
    record_cursor.execute("INSERT INTO cpu_ram_status(CPU_STATUS, RAM_STATUS) VALUES("+str(cpu_status)+", "+str(ram_status)+");")
    connection.commit()
    print(payload_data)

client = mqtt.Client()
client.on_connect  = on_connect
client.on_message = on_message
client.connect('broker.emqx.io', 1883, 60);
client.loop_forever()