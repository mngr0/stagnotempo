"""
WSGI config for stagnotempo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
#import threading
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stagnotempo.settings')

#from multiprocessing import Process

#from interfaccia import routine

#p = Process(target=routine.thread_function, args=())
#p.start()

#x = threading.Thread(target=routine.thread_function, args=())
application = get_wsgi_application()

#x.start()



