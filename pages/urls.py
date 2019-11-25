from django.urls import path
from . import views


urlpatterns = [

   path('', views.index, name='index'),
   path('product/<slug>', views.product, name='product'),
   path('login', views.login_page, name='login'),
   path('login_req', views.login_req, name='login_req'),
   path('reg_req', views.reg_req, name='reg_req'),
   path('update_req', views.update_req, name='update_req'),
   path('lk', views.lk, name='lk'),
   path('search/', views.search, name='search'),
   # path('post/<slug>/', views.showPost, name='showpost'),
   # path('about/', views.about, name='about'),
   # path('services/', views.services, name='services'),
   # path('service/<slug>/', views.service, name='service'),
   # path('robots.txt', views.robots, name='robots'),



]
