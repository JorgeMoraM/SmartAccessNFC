import RPi.GPIO as GPIO
import nxppy
import time

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP) #BOTON
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #entrada sensor
GPIO.setup(29, GPIO.OUT) #alimentacion sensor
GPIO.setup(31, GPIO.OUT) #LED ROJO
GPIO.setup(33, GPIO.OUT) #LED VERDE

def OpenDoor():
    flagOpen = False
    GPIO.output(31, False)
    GPIO.output(33, True)
    print('Puerta habilitada')
    for i in range(10): #espera 10 segundos o hasta que se abra la puerta
        door_state = GPIO.input(37)
        if door_state == False:
            flagOpen = True
            print('Puerta abierta')
            break
        time.sleep(1)
    if flagOpen == True:
        while True:        #espera hasta que se cierre la puerta para continuar
            door_state = GPIO.input(37)
            if door_state == True:
                print('Puerta cerrada')
                #flagOpen = False 
                break
    print('Puerta deshabilitada')
    

mifare = nxppy.Mifare()

GPIO.output(29, True)

while True:
    GPIO.output(33, False)
    GPIO.output(31, True)
    button_state = GPIO.input(32)
    
    if button_state == False:
        print('Boton presionado')
        OpenDoor()
        
    try:
        uid = mifare.select()               
        print(uid)
        if uid == '044A5FD29C3980':
            OpenDoor()
            
    except nxppy.SelectError:
        pass
    time.sleep(0.2)
        

        
