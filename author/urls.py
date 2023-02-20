from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.no_author, name='no_author'),
    # ex: /polls/5/
    path('<str:author_name>/', views.author_summary, name='author_summary'),
]