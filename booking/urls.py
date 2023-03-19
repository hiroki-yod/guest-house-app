from django.urls import path
from .views import main, auth, host, guest


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

    #guest.py
    path('guest/mypage/', guest.guest_mypage.as_view(), name='guest_mypage'),
    path('facility/index/', guest.facility_index.as_view(), name='facility_index'),
    path('facility/<uuid:facility_id>/', guest.facility_detail.as_view(), name='facility_detail'),
    path('reserve/<uuid:selected_facility_id>/frame/index', guest.reserve_frame_index.as_view(), name='reserve_frame_index'),
    path('reserve/<uuid:selected_facility_id>/<int:selected_frame_id>/', guest.reserve_frame_apply.as_view(), name='reserve_frame_apply'),
    path('reserve/save/', guest.reserve_save.as_view(), name='reserve_save'),
]