from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponse
# from django.core.management import call_command
from .models import Post
from .forms import PostForm

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

def run_migrations_view(request):
    # call_command('makemigrations')
    # call_command('migrate')
    return HttpResponse("Migrations completed")

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})