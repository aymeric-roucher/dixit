from django.urls import path
from .views import show_searchbar


urlpatterns = [
    # ex: /polls/
    path('', show_searchbar, name='searchbar'),
]