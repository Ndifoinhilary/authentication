from django.urls import path

from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('opt/', views.enter_opt, name='opt'),
    path('resend_opt/', views.resend_opt, name='resend_opt'),
]