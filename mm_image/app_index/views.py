from django.shortcuts import render
from django.http import HttpResponse



def test(request):
    return HttpResponse("it's a test!")
