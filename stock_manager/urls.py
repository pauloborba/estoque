"""stock_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from manager import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls, name="admPage"),
    url(r'^$', views.home_login, name="home_login"),
    url(r'^help/$', views.help, name="help"),
    url(r'^signUp_old/$', views.sign_up, name="sign_up"),
    url(r'^newPrice/$', views.new_price, name="new_price"),
    url(r'^newItem_old/$', views.new_item, name="new_item"),
    url(r'^editItem/$', views.edit_item, name="new_editItemById"),
    url(r'^newCategory_old/$', views.new_category, name="new_category"),
    url(r'^newStore/$', views.new_store, name="new_store"),
    url(r'^home/$', views.home, name="home"),
    url(r'^generate_list/$', views.generate_list, name="generate_list"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^priceList/$', views.price_list, name="price_list"),
    url(r'^newListByStore/$', views.create_list_by_store, name="listByStore"),
]
urlpatterns += staticfiles_urlpatterns()
