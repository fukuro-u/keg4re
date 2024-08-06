from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.core.management import call_command

# Create your views here.
def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)
# views.py

def run_migrations_view(request):
    # call_command('makemigrations')
    # call_command('migrate')
    return HttpResponse("Migrations completed")

