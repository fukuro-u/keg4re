from django.shortcuts import render
from django.conf import settings
import os
from datetime import datetime
from django.http import HttpResponse

# Create your views here.
def time(request):
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


def image_selector(request):
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    images = []
    
    for root, dirs, files in os.walk(media_root):
        for file in files:
            if file.endswith(('jpg', 'jpeg', 'png', 'gif')):
                images.append(os.path.join(root, file).replace(media_root, media_url))
    
    return render(request, 'image_selector.html', {'images': images})