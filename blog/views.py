from django.http import HttpResponse
 
def index(request):
    return HttpResponse("Hello, world.")

def detail(request):
    return HttpResponse("detail page")
