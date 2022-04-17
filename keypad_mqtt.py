#!/usr/bin/python3

from matrix_keypad import RPi_GPIO

kp = RPi_GPIO.keypad(columnCount = 3)
import paho.mqtt.client as mqtt
import datetime

client = mqtt.Client(client_id="keypad")
client.username_pw_set("keypad", password="Cu1X8X7nwGy7")
client.connect("192.168.50.80")

code = ""
nones = 5
last_registered = None
last_registered_ts = datetime.datetime.now()
last_input = None
last_input_ts = datetime.datetime.now()

bounce_duration = datetime.timedelta(milliseconds=20)
code_duration = datetime.timedelta(seconds = 5)

client.loop_start();

while True:
    digit = kp.getKey()
    now_ts = datetime.datetime.now()

    if digit == last_input:
        if now_ts - last_input_ts > bounce_duration and last_input != last_registered:
            if last_input != None and now_ts - last_registered_ts > bounce_duration:
                print("Got {}".format(digit))
                if digit == '#':
                    code = ""
                    print("force reset")
                else:
                    code = code + str(digit)
                    print("Code is now [{}]".format(code))
                    if len(code) == 4:
                        print("publishing {}".format(code))
                        client.publish("keypad/code", payload=code)
                        code = ""

                
            last_registered = last_input
            last_registered_ts = now_ts
    else:
        print("New {}".format(digit))
        last_input = digit
        last_input_ts = now_ts

    lastkey = digit

    if code != "" and last_registered == None and now_ts - last_registered_ts > code_duration:
        print("reset")
        code = ""
        
            
