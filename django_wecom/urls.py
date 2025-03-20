from django.urls import path
from .views import *

urlpatterns = [
    path('callback/', callback),
    path('login/', login),
    path('logout/', logout),
    path('clearpassword/<int:uid>/', clearpassword),
]