#!/usr/bin/python3

from matrix_keypad import RPi_GPIO

kp = RPi_GPIO.keypad(columnCount = 3)
import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="keypad")
client.username_pw_set("keypad", password="Cu1X8X7nwGy7")
client.connect("192.168.50.80")

code = ""
nones = 5
lastkey = None

client.loop_start();
while True:
    digit = kp.getKey()

    if digit is not None and digit != lastkey and nones == 0:
        
        nones = 5
        print("Got {}"_format(digit))
        code = code + str(digit)

        if len(code) == 4:
            print("publishing {}"_format(code))
            #client.publish("keypad/code", payload=code)
            code = ""
    elif digit is None and nones > 0:
        nones -= 1


    lastkey = digit
            
