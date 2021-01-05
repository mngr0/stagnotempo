import logging
import threading
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

inputs_empty = [2,3]
inputs_pump = [20,21]

out_pump = 17
led_pump = 5

out_empty = 27
led_empty = 7

led_on=15

outputs= [out_pump,led_pump,out_empty,led_empty,led_on]

for out in outputs:
    GPIO.setup(out, GPIO.OUT)
    GPIO.output(out, 0)

# GPIO 23 set up as input. It is pulled up to stop false signals
for gpio in inputs_pump:
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for gpio in inputs_empty:
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

ttw = 0 #time to wait

from interfaccia.models import Configurazione

def gen_fun(index):
    def fun(par):
        global ttw
        print("clicked ",index)
        if ttw == 0:
            print("waiting for ", Configurazione.objects.get(pk=index).durata)
            ttw = Configurazione.objects.get(pk=index).durata
    return fun


def check():
    global ttw
    if ttw != 0:
        print("check ")
        GPIO.output(out_pump, 1)
        GPIO.output(led_pump, 1)
        time.sleep(int(ttw)/1000)
        print("done waiting")
        GPIO.output(led_pump, 0)
        GPIO.output(out_pump, 0)
        ttw=0

def thread_function():
    for index,pin in enumerate(inputs_pump):
        GPIO.add_event_detect(pin, GPIO.RISING, callback=gen_fun(index+1), bouncetime=400)
    #GPIO.add_event_detect(2, GPIO.RISING, callback=foo, bouncetime=400)
    #GPIO.add_event_detect(3, GPIO.RISING, callback=bar, bouncetime=400)
    print("Thread  starting")
    #accendere LED
    GPIO.output(led_on, 1)
    while 1:
        check()
        time.sleep(10/1000)

def set_interval(idx,new_interval):
    global interval
    interval = new_interval
    ogg=Configurazione.objects.get(pk=idx)
    ogg.durata=new_interval
    ogg.save()
