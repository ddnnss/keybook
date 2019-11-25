from django.urls import path
from . import views

urlpatterns = [
   path('log_in/', views.log_in, name='log_in'),
   path('logout/', views.log_out, name='logout'),
   path('signup/', views.signup, name='signup'),
   path('restore/', views.restore, name='restore'),
   path('update/', views.account_edit, name='update'),
]
