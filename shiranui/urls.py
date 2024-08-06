from django.urls import path
from shiranui.views import index

urlpatterns = [
    path('', index),
]