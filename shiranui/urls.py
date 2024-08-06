from django.urls import path
from shiranui.views import index, run_migrations_view

urlpatterns = [
    path('', index),
    path('run-migrations/', run_migrations_view, name='run_migrations'),
]