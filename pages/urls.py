from django.urls import path
from . import views


urlpatterns = [

   path('', views.index, name='index'),
   path('product/<slug>', views.product, name='product'),
   path('login', views.login_page, name='login'),
   path('logout', views.logout_page, name='logout'),
   path('login_req', views.login_req, name='login_req'),
   path('reg_req', views.reg_req, name='reg_req'),
   path('update_req', views.update_req, name='update_req'),
   path('lk', views.lk, name='lk'),
   path('search/', views.search, name='search'),
   path('addhouse', views.addhouse, name='addhouse'),
   path('edithouse', views.edithouse, name='edithouse'),
   path('addfilter/<id>', views.addfilter, name='addfilter'),
   path('addfilter_req', views.addfilter_req, name='addfilter_req'),
   path('addfav/<id>', views.addfav, name='addfav'),
   path('delfav/<id>', views.delfav, name='delfav'),
   path('edit/<id>', views.edit, name='edit'),
   path('rent/', views.rent, name='rent'),
   path('about/', views.about, name='about'),
   path('post/<slug>', views.post, name='post'),
   path('new_msg/', views.new_msg, name='new_msg'),
   path('add_msg/', views.add_msg, name='add_msg'),
   path('answer_msg/', views.answer_msg, name='answer_msg'),
   path('get_chat_msg/', views.get_chat_msg, name='get_chat_msg'),



]
