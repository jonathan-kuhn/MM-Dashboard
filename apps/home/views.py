# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect

import core.settings as settings
import apps.home.api_functions as api_functions
import apps.home.utilites as utilites



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def servers(request):
    server_status=api_functions.ping()
    if not server_status:
        html_template = loader.get_template('home/offline.html')
        return HttpResponse(html_template.render(request=request))
    servers = api_functions.get_servers(request.user.get_username()) if server_status else [[],[]]
    context = { 'segment': 'servers',
                'url': settings.DISPLAY_SERVER_IP,
                'status': server_status,
                'running': servers[0],
                'exited' : servers[1]
                }

    html_template = loader.get_template('home/servers.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def start(request):
    server_name = request.POST['server_name']
    username = request.user.get_username()
    response = api_functions.start(username, server_name)
    return redirect("/") if response !=500 else redirect("/page-500.html") 

@login_required(login_url="/login/")
def stop(request):
    server_name = request.POST['server_name']
    username = request.user.get_username()
    response = api_functions.stop(username, server_name)
    return redirect("/") if response !=500 else redirect("/page-500.html")  

@login_required(login_url="/login/")
def create(request):
    user_profile = utilites.get_user_profile_details(request.user.get_username())
    server_status=api_functions.ping()
    if not server_status:
        html_template = loader.get_template('home/offline.html')
        return HttpResponse(html_template.render(request=request))
    
    context = {'segment': 'create', **user_profile}

    if request.method == "POST":
        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken')
        response = api_functions.create(username=request.user.get_username(), data=data)
        return redirect("/") if response !=500 else redirect("/page-500.html")

    html_template = loader.get_template('home/create.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def edit(request):
    user_profile = utilites.get_user_profile_details(request.user.get_username())
    server_status=api_functions.ping()
    if not server_status:
        html_template = loader.get_template('home/offline.html')
        return HttpResponse(html_template.render(request=request))
    server_name = request.GET.get('server')
    if server_name == None: 
        servers = api_functions.get_servers(request.user.get_username(), separated=False)
        context = {'segment': 'edit', 'server_name': server_name, 'servers': servers}    
    else:   
        server_config = api_functions.get_server_config(request.user.get_username(), server_name)     
        context = {'segment': 'edit', **server_config, **user_profile} # make the used port and memory selected

    if request.method == "POST":
        data = dict(request.POST)
        data.pop('csrfmiddlewaretoken')
        server_name = request.GET.get('server')
        response = api_functions.edit(username=request.user.get_username(), server_name=server_name, data=data)
        return redirect("/edit") if response !=500 else redirect("/page-500.html")

    html_template = loader.get_template('home/edit.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def delete(request):
    if request.method == "POST":
        data = dict(request.POST)
        server_name=data['server_name'][0]
        response = api_functions.delete(username=request.user.get_username(), server_name=server_name)
        return redirect("/edit") if response !=500 else redirect("/page-500.html")

    return redirect("/")

@login_required(login_url="/login/")
def reset(request):
    if request.method == "POST":
        data = dict(request.POST)
        server_name=data['server_name'][0]
        response = api_functions.reset(username=request.user.get_username(), server_name=server_name)
        return redirect("/edit") if response !=500 else redirect("/page-500.html")

    return redirect("/")

@login_required(login_url="/login/")
def exec(request):
    if request.method == "POST":
        data = dict(request.POST)
        server_name=data['server_name'][0]
        mc_username = data['username'][0]
        command = f'op {mc_username}'
        response_code, response = api_functions.exec(username=request.user.get_username(), server_name=server_name, command=command)
        return redirect("/") if response_code !=500 else redirect(f"/page-500.html?error={response}")

    return redirect("/")

@login_required(login_url="/login/")
def user(request):
    profile = utilites.get_user_profile(username=request.user.get_username())
    context = { 'segment': 'user',
                'profile': profile }

    html_template = loader.get_template('home/user.html')
    return HttpResponse(html_template.render(context, request))
