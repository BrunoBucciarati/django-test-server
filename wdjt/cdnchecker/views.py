# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import cdnurl
import os
import cdnchecker

cdnUrl = None
platName = None
# Create your views here.
def index(request):
    cdnurls = cdnurl.objects.all()
    context = {'cdnurls':cdnurls}
    return render(request, 'index.html', context)

def callSetInfo(request):
    global cdnUrl, platName
    cdn = request.GET.get('cdn')
    plat = request.GET.get('plat')
    cdnUrl = cdn
    platName = plat
    return render(request, 'uploadInfo.html', {})

def uploadFile(request):
    if request.method == 'POST':
        myFile = request.FILES.get("fileUpload", None)
        if myFile:
            destPath = os.path.join("cdnchecker/buffer", "info.info")
            try:
                os.remove(destPath)
            except:
                pass
            destFile = open(destPath, 'wb+')
            configFile = open(os.path.join("cdnchecker/buffer", "config.info"), 'w')
            configFile.write(myFile.name)
            configFile.close()
            for chunk in myFile.chunks():
                destFile.write(chunk)
            destFile.close()
            cdnchecker.runCheck(cdnUrl, platName)
            return render(request, 'wait.html', {"txt":"等待CDN中", "state":"waiting"})
        else:
            return HttpResponse("upload failed")
    return HttpResponse("您访问的页面不存在")

def wait(request):
    flag = cdnchecker.isFinish()
    if flag == 1:
        return HttpResponse("success")
    elif flag == 0:
        #return render(request, 'wait.html', {"txt":"等待CDN中", "state":"waiting"})
        return HttpResponse("waiting")
    else:
        return HttpResponse("error")
