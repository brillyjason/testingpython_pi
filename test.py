import paho.mqtt.client as mqtt 
import time
import psutil, os
import GPUtil
import json
import wmi
import yaml
from pathlib import Path
import msvcrt

path_to_file = 'config.yaml'
path = Path(path_to_file)

if path.is_file():
    

    fileconfig = yaml.safe_load(open("config.yaml", "rb"))

    host= fileconfig.get("host")
    topik= fileconfig.get("topik")



    mqttBroker = host

#192.168.1.198
    client = mqtt.Client()
    client.connect(mqttBroker) 


    while True:

        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType==u'Temperature':
                print(sensor.Name)
            c = print(sensor.Value) 

        a=int(psutil.virtual_memory().percent)
        b=int(psutil.cpu_percent())
        c=int(psutil.disk_usage('/').percent)
        d=float(c)


        x = {"RAM": a, "CPU": b, "DISK": c, "TEMP": d}   

        y = json.dumps(x)
    #y = json.loads(x)

    #client.publish("TUTOR", psutil.virtual_memory().percent )
    #client.publish("TUTOR", psutil.cpu_percent() )
    #client.publish("TUTOR", psutil.disk_usage('/').percent )
        client.publish(topik, y )


    #print(psutil.disk_io_counters())
    #cpu = CPUTemperature()

    #cpu = CPUTemperature()
    #print(cpu.temperature) 

        print(psutil.disk_usage('/').percent, "%")
        print(psutil.cpu_percent())
        print(psutil.virtual_memory().percent)
        print("----------------------")
        time.sleep(1)

else:
    print(f'File {path_to_file} tidak ditemukan')
    char = msvcrt.getch()

    