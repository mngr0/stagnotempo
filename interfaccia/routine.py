import logging
import threading
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

inputs = [2,3]
output=14
# GPIO 23 set up as input. It is pulled up to stop false signals
for gpio in inputs:
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(output, GPIO.OUT)

GPIO.output(output, 0)

ttw = 0

from interfaccia.models import Configurazione

def foo(par):
    global ttw
    print("clicked foo")
    if ttw == 0:
        print("waiting for ", Configurazione.objects.get(pk=1).durata)
        ttw = Configurazione.objects.get(pk=1).durata
        #GPIO.output(output, 1)
        #time.sleep(int(Configurazione.objects.get(pk=1).durata)/1000)
        #print("done waiting")
        #GPIO.output(output, 0)


def bar(par):
    global ttw
    print("clicked bar")
    if ttw == 0:
        print("waiting for ", Configurazione.objects.get(pk=2).durata)
        ttw = Configurazione.objects.get(pk=2).durata


def check():
    global ttw
    if ttw != 0:
        print("check ")
        GPIO.output(output, 1)
        time.sleep(int(ttw)/1000)
        print("done waiting")
        GPIO.output(output, 0)
        ttw=0

def thread_function():
    GPIO.add_event_detect(2, GPIO.RISING, callback=foo, bouncetime=400)
    GPIO.add_event_detect(3, GPIO.RISING, callback=bar, bouncetime=400)
    print("Thread  starting")
    while 1:
        check()
        time.sleep(10/1000)
        #for index,gpio in enumerate(inputs):
        #    if GPIO.input(gpio):
        #        print("clicked ",index, " waiting for ", Configurazione.objects.get(pk=index+1).durata)
        #        #GPIO.wait_for_edge(23, GPIO.FALLING) 
        #        GPIO.output(output, 1)
        #        time.sleep(int(Configurazione.objects.get(pk=index+1).durata)/1000)
        #        print("done waiting")
        #        GPIO.output(output, 0)

def set_interval(idx,new_interval):
    global interval
    interval = new_interval
    ogg=Configurazione.objects.get(pk=idx)
    ogg.durata=new_interval
    ogg.save()
