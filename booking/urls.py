from django.urls import path
from .views import main, auth, host


urlpatterns = [
    #main.py
    path('', main.index.as_view(), name='index'),
    #auth.py
    path('host/signup/', auth.signup_host.as_view(), name='signup_host'),
    path('signup/', auth.signup_guest.as_view(), name='signup_guest'),
    path('login/', auth.login_common.as_view(), name='login'),
    path('logout/', auth.logout_common.as_view(), name='logout'),
    #host.py
    path('host/facility', host.facility_list.as_view(), name='facility_list'),
    path('host/facility/register', host.facility_register.as_view(), name='facility_register'),
    path('host/room/register', host.room_register.as_view(), name='room_register'),
]