from django.urls import path

from . import views

urlpatterns = [
    path('', views.no_author, name='author'),
    path('<str:name>/', views.author_summary, name='author_summary'),
]