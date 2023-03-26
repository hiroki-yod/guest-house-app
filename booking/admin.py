from django.contrib import admin
from .models import CommonUser, HostUser, GuestUser, Facility, Room, ReservationFrame, Reservation, Price

class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]

admin.site.register(CommonUser)
admin.site.register(HostUser)
admin.site.register(GuestUser)
admin.site.register(Facility)
admin.site.register(Room)
admin.site.register(ReservationFrame, ProductAdmin)
admin.site.register(Reservation)
admin.site.register(Price)