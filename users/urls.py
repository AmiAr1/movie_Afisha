from django.urls import path
from .views import *


urlpatterns = [
    path('authorization/', authorization_api_view),
    path('registration/', registration_api_view)
]