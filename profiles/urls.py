from django.urls import path
from profiles.views import *

app_name = 'profiles'

urlpatterns = [
    path('preference/', preference, name='preference'),
    path('showprofile/', showprofile, name='showprofile'),
    path('pref_json/', pref_json, name='pref_json'),
    path('ret_review/', ret_review, name='ret_review'),
    path('ret_profile/', ret_profile, name='ret_profile'),
    path('change_pref/', change_pref, name='change_pref'),
]
