"""quotation_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .sitemaps import StaticSitemap, AuthorSitemap
from django.contrib.sitemaps.views import sitemap
from author.views import author_summary, search_author


sitemaps = {
    'static':StaticSitemap, #add StaticSitemap to the dictionary
    'authors': AuthorSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('/searchbar/')),
    path('search_author/', search_author, name='search_author'),
    path('author/<str:name>/', author_summary, name='author'),
    path('searchbar/', include('searchbar.urls'), name="searchbar"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
 