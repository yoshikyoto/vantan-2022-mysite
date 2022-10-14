from django.shortcuts import render
from django.http import HttpResponse
 
def index(request):
    return render(request, "blog/index.html")

def detail(request):
    return HttpResponse("detail page")
