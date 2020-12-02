from django.apps import AppConfig
import threading

class InterfacciaConfig(AppConfig):
    name = 'interfaccia'
    def ready(self):
        from interfaccia import routine
        x = threading.Thread(target=routine.thread_function, args=())
        x.start()
