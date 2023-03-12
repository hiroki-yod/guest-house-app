from django.urls import path, include
from .views import main, auth, guest


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

    #ここから編集 認証の仕組みがわからなかったのでとりあえずguest.pyというのをauth関係から隔離して実装
    path('facility/index', guest.facility_index.as_view(), name='facility_index'),
    path('facility/<uuid:facility_id>/', guest.facility_detail.as_view(), name='facility_detail'),

]