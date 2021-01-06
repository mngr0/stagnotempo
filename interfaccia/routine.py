import logging
import threading
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

def millis():
    return round(time.monotonic() * 1000)

inputs_empty = [20,21]
inputs_pump = [19,26]

out_pump = 27
led_pump = 13

out_empty = 17
led_empty = 6

led_on=5

outputs= [out_pump,led_pump,out_empty,led_empty,led_on]

for out in outputs:
    GPIO.setup(out, GPIO.OUT)
    GPIO.output(out, 0)

# GPIO 23 set up as input. It is pulled up to stop false signals
for gpio in inputs_pump:
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for gpio in inputs_empty:
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global end_wait
end_wait = 0

global start_wait
start_wait=0

global started
started = False
from interfaccia.models import Configurazione

global empty_state
empty_state=0

def empty_state_edge():
    print("toggle empty _ state")
    global empty_state
    empty_state= not empty_state
    GPIO.output(out_empty, empty_state)
    GPIO.output(led_empty, empty_state)


def empty_on_edge():
    print("toggle empty _ on")
    global empty_state
    empty_state= not empty_state
    GPIO.output(out_empty, empty_state)
    GPIO.output(led_empty, empty_state)

def gen_fun(index):
    def fun():
        global end_wait
        print("clicked ",index)
        if millis() > end_wait:
            print("waiting for ", Configurazione.objects.get(pk=index).durata)
            ttw = Configurazione.objects.get(pk=index).durata
            end_wait = millis() + ttw
    return fun

inputs_state = [
                 {  'pin':inputs_empty[0],
                    'edge_sense':0,
                    'cb':empty_state_edge,
                    'last_state':GPIO.input(inputs_empty[0]),
                    'millis_edge':millis(),
                    'debounce':50,
                    'edge_found':0,
                    'last_edge':None
                 },
                 {  'pin':inputs_empty[1],
                    'edge_sense':1,
                    'cb':empty_on_edge,
                    'last_state':GPIO.input(inputs_empty[1]),
                    'millis_edge':millis(),
                    'debounce':50,
                    'edge_found':0,
                    'last_edge':None
                 },
                 {  'pin':inputs_empty[1],
                    'edge_sense':0,
                    'cb':empty_on_edge,
                    'last_state':GPIO.input(inputs_empty[1]),
                    'millis_edge':millis(),
                    'debounce':50,
                    'edge_found':0,
                    'last_edge':None
                 },
                 {  'pin':inputs_pump[0],
                    'edge_sense':0,
                    'cb':gen_fun(1),
                    'last_state':GPIO.input(inputs_pump[0]),
                    'millis_edge':millis(),
                    'debounce':50,
                    'edge_found':0,
                    'last_edge':None
                 },
                 {  'pin':inputs_pump[1],
                    'edge_sense':0,
                    'cb':gen_fun(2),
                    'last_state':GPIO.input(inputs_pump[1]),
                    'millis_edge':millis(),
                    'debounce':50,
                    'edge_found':0,
                    'last_edge':None
                 }
               ]

def check_bounce(structs):
    for struct in structs:
        new_state=GPIO.input(struct['pin'])
        now_time=millis()
        if new_state is not struct['last_state']:
             struct['last_state']=new_state
             struct['millis_edge']=now_time
             struct['edge_found']=False
        else:
             if struct['edge_found'] is False:
                 if now_time - struct['millis_edge'] > struct['debounce']:
                     if new_state == struct['edge_sense'] and new_state != struct['last_edge']:
                         struct['cb']()
                     else:
                         print('edge ignored newstate=',new_state," last_edge=",struct['last_edge'])
                     struct['edge_found']=True
                     struct['last_edge']=new_state


def check():
    global end_wait
    global start_wait
    global started
    if millis()<end_wait:
        if not started:
            print("start wait  ")
            GPIO.output(out_pump, 1)
            GPIO.output(led_pump, 1)
            start_wait=millis()
            started = True
    else:
        if started:
            started = False
            print("done waiting")
            GPIO.output(led_pump, 0)
            GPIO.output(out_pump, 0)
    #if up for more than given time: go to pwm

def thread_function():
    print("Thread  starting")
    #accendere LED
    GPIO.output(led_on, 1)
    while 1:
        check_bounce(inputs_state)
        check()
        time.sleep(10/1000)

def set_interval(idx,new_interval):
    global interval
    interval = new_interval
    ogg=Configurazione.objects.get(pk=idx)
    ogg.durata=new_interval
    ogg.save()
