from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import json
from interfaccia import routine


from interfaccia.models import Configurazione

def index(request):
    template = loader.get_template('index.html')
    context ={
        "time1":Configurazione.objects.get(pk=1).durata,
        "time2":Configurazione.objects.get(pk=2).durata}
    return HttpResponse(template.render(context, request))

def post_manager(request):
    form_data = request.body.decode()
    print(str(form_data))
    print(str(request.POST))
    if request.method == 'POST':
        if "tempo1" in request.POST.keys():
            routine.set_interval(1,request.POST['tempo1'])
        if "tempo2" in request.POST.keys():
            routine.set_interval(2,request.POST['tempo2'])
    return HttpResponseRedirect('/')
