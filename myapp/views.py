from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# This is a simple view that returns a plain text response.
def home(request):
    return HttpResponse("Hello Test works!")
