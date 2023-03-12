from django.urls import path, include
from .views import main, auth


urlpatterns = [
    #main.py
    path('', main.index.as_view(), name='index'),
    #auth.py
    path('host/signup/', auth.signup_host.as_view(), name='signup_host'),
    path('signup/', auth.signup_guest.as_view(), name='signup_guest'),
    path('login/', auth.login.as_view(), name='login'),
    path('logout/', auth.logout.as_view(), name='logout_host'),
    # path('signup/', auth.signup_guest.as_view(), name='signup_guest'),
    # path('login/', auth.login_guest.as_view(), name='login_guest'),
    # path('logout/', auth.logout_guest.as_view(), name='logout_guest'),
]