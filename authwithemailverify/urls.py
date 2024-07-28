from django.urls import path, re_path

from .views import activate, signup

app_name = 'authwithemailverify'


urlpatterns = [

    path('activate/<uidb64>/<token>/', activate, name='activate'),



    path("", signup, name="signup")
]
