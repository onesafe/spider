from django.shortcuts import render
from django.http import HttpResponse



def test(request, catagory):
    return HttpResponse("catagory: %s" % catagory) 

