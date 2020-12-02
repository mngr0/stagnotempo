import logging
import threading
import time
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  
  
# GPIO 23 set up as input. It is pulled up to stop false signals  
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.OUT)

GPIO.output(24, 1)


from interfaccia.models import Configurazione



def thread_function():

    print("Thread  starting")
    while 1:
        print("thread running at ",Configurazione.objects.get(pk=1).durata)
        #GPIO.wait_for_edge(23, GPIO.FALLING) 
        GPIO.output(24, 1)
        time.sleep(int(Configurazione.objects.get(pk=1).durata)/1000)
        GPIO.output(24, 0)
        time.sleep(int(Configurazione.objects.get(pk=1).durata)/1000)
        GPIO.output(24, 1)


def set_interval(idx,new_interval):
    global interval
    interval = new_interval
    ogg=Configurazione.objects.get(pk=idx)
    ogg.durata=new_interval
    ogg.save()
