from django.urls import path, include
from .views import main, auth, guest


urlpatterns = [
    #main.py
    path('', main.index.as_view(), name='index'),
    #auth.py
    path('host/signup/', auth.signup_host.as_view(), name='signup_host'),
    path('signup/', auth.signup_guest.as_view(), name='signup_guest'),
    path('login/', auth.login_common.as_view(), name='login'),
    path('logout/', auth.logout_common.as_view(), name='logout'),
    # path('signup/', auth.signup_guest.as_view(), name='signup_guest'),
    # path('login/', auth.login_guest.as_view(), name='login_guest'),
    # path('logout/', auth.logout_guest.as_view(), name='logout_guest'),

    #ここから編集 認証の仕組みがわからなかったのでとりあえずguest.pyというのをauth関係から隔離して実装
    path('facility/index/', guest.facility_index.as_view(), name='facility_index'),
    path('facility/<uuid:facility_id>/', guest.facility_detail.as_view(), name='facility_detail'),
    path('reserve/<uuid:selected_facility_id>/frame/index', guest.reserve_frame_index.as_view(), name='reserve_frame_index'),
    path('reserve/<uuid:selected_facility_id>/<int:selected_frame_id>/', guest.reserve_frame_apply.as_view(), name='reserve_frame_apply'),
    path('reserve/save/', guest.reserve_save.as_view(), name='reserve_save'),
]