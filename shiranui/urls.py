from django.urls import path
from shiranui.views import time, run_migrations_view, post_list, post_create, ListPost
# from .views import post_list, post_create

urlpatterns = [
    path('', post_list, name='post_list'),
    path('list/', ListPost.as_view(), name='list'),
    path('create/', post_create, name='post_create'),
    path('time/', time),
    path('run-migrations/', run_migrations_view, name='run_migrations')
]