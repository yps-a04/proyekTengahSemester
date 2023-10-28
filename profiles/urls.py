from django.urls import path
from profiles.views import *

app_name = 'profiles'

urlpatterns = [
    path('preference/', preference, name='preference'),
    path('showprofile/', showprofile, name='showprofile'),
    path('pref_json/', pref_json, name='pref_json')
]
