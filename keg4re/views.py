from django.shortcuts import render
from django.http import HttpResponse
from django.views.debug import default_urlconf

def view_404(request, exception):
    context = {'message': str(exception) if exception else "Page not found"}
    render(request, '404.html',context)
    
def view_500(request, exception=None):
    context = {'message': str(exception) if exception else "Page not found"}
    render(request, '404.html', context)