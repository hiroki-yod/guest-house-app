from django.contrib import admin
from .models import CommonUser, HostUser, GuestUser, Facility, Room, ReservationFrame, Reservation, Event, EventApplication


admin.site.register(CommonUser)
admin.site.register(HostUser)
admin.site.register(GuestUser)
admin.site.register(Facility)
admin.site.register(Room)
admin.site.register(ReservationFrame)
admin.site.register(Reservation)
admin.site.register(Event)
admin.site.register(EventApplication)