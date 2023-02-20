from django.urls import path

from . import views

urlpatterns = [
    path('', views.no_author, name='author'),
    path('<str:author_name>/', views.author_summary, name='author_summary'),
]