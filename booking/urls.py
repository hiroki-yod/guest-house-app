from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path('host', host.host_index.as_view(), name='host_index'),                                     #TODO
    path('host/facility/register', host.facility_register.as_view(), name='facility_register'),     #TODO
    path('host/room/register', host.room_register.as_view(), name='room_register'),                 #TODO
    path('host/event/register', host.event_register.as_view(), name='event_register'),              #TODO

    #guest.py
    path('mypage/', guest.guest_mypage.as_view(), name='guest_mypage'),
    path('facility/index/', guest.facility_index.as_view(), name='facility_index'),
    path('facility/<uuid:facility_id>/', guest.facility_detail.as_view(), name='facility_detail'),
    path('reserve/<uuid:selected_facility_id>/frame/index', guest.reserve_frame_index.as_view(), name='reserve_frame_index'),
    path('reserve/<uuid:selected_facility_id>/<int:selected_frame_id>/', guest.reserve_frame_apply.as_view(), name='reserve_frame_apply'),
    path('reserve/save/', guest.reserve_save.as_view(), name='reserve_save'),
    path('facility/event/apply/save', guest.guest_event_apply_save.as_view(), name='event_apply_save'),
    path('facility/event/apply/<uuid:facility_uid>/<int:event_id>', guest.guest_event_apply.as_view(), name='event_apply'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)