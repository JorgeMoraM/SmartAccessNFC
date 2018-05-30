import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP) #entrada sensor
GPIO.setup(37, GPIO.OUT) #SALIDA AL RELAY
GPIO.setup(31, GPIO.OUT) #LED ROJO
GPIO.setup(33, GPIO.OUT) #LED VERDE

def OpenDoor():
    flagOpen = False
    GPIO.output(31, False)
    GPIO.output(33, True)
    GPIO.output(37, True)
    print('Puerta habilitada')
    for i in range(10): #espera 10 segundos o hasta que se abra la puerta
        door_state = GPIO.input(29)
        if door_state == True:
            flagOpen = True
            print('Puerta abierta')
            break
        time.sleep(1)
    if flagOpen == True:
        while True:        #espera hasta que se cierre la puerta para continuar
            door_state = GPIO.input(29)
            if door_state == False:
                #GPIO.output(37, False)
                print('Puerta cerrada')
                #flagOpen = False 
                break
    if flagOpen == True and door_state == False:
        time.sleep(4)
    GPIO.output(37, False)
    print('Puerta deshabilitada')
    GPIO.output(33, False)
    GPIO.output(31, True)


def on_connect(client, userdata, flags, rc):
    print("connected with result code "+str(rc))
    #client.subscribe("puertas/principal")     #AJUSTAR DE ACUERDO A LA PUERTA
    client.subscribe("puertas/prototipado")
def on_message(client, userdata, msg):
    doorAcc=msg.payload.decode()
    print(doorAcc) #DEBUG
    if doorAcc == "PERMITTED":
        OpenDoor()
    client.disconnect()

GPIO.output(33, False)
GPIO.output(31, True)
GPIO.output(37, False)

while True:
    client = mqtt.Client() #Crea un cliente mqtt
    client.connect("192.168.1.66",1883,60) #AJUSTAR LA DIRECCIóN AL SERVER
#    client.connect("148.202.23.200",1883,60) #server cici
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever() 
    

    
    
    
