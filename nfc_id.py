import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import nxppy
import time


def serverComm(uid):
    client = mqtt.Client()
    client.connect("192.168.1.66",1883,60)
    #client.connect("148.202.23.200",1883,60) #server cici
#   client.publish("puertas/principal",uid)
    client.publish("puertas/prototipado",uid)
    client.disconnect()

button_id = "f55418be36"
#button_id = "ABCD1234"
mifare = nxppy.Mifare()

GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP) #BOTON    

while True:
    button_state = GPIO.input(32)
    uid = 0
      
    if button_state == False:
        print('Boton presionado')
        uid = button_id
    try:
        uid = mifare.select()
        print(uid)
                         
    except nxppy.SelectError:
        pass
    
    if uid != 0:
        serverComm(uid)
    time.sleep(0.2)
