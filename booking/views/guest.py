from django.http import HttpResponse, Http404
from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms import auth
from ..models import Facility, ReservationFrame, Room

class facility_index(View):
    def get(self, request):
        Facility_list = Facility.objects.order_by('name')[:5]
        param = {
            'Facility_list':Facility_list,
        }
        return render(request, "booking/auth/guest/facility_index.html", param)
        #return HttpResponse("You're looking at facility_index")

class facility_detail(View):
    def get(self, request, facility_id):
        #return HttpResponse("You're looking at facility_detail")
        try:
            facility = Facility.objects.get(pk=facility_id)
        except facility.DoesNotExist:
            raise Http404("Facility does not exist")
        return render(request, 'booking/auth/guest/facility_detail.html', {'facility': facility})
    
class reserve_frame_index(View):
    def get(self, request, selected_facility_id):
        try:
            selectedFacility = Facility.objects.get(pk=selected_facility_id)
            rooms = Room.objects.filter(facility_id=selected_facility_id)
            reservationFrames = []
            for room in list(rooms.values()):
                reservationFrames[str(room["id"])].append(\
                    ReservationFrame.objects.filter(room_id=room.id).order_by('date'))
            # framesは二次元配列で、第一indexが各roomに対する連想配列、
            # 第二indexが各roomにおける予約枠の連想配列
            param = {
                'facility':selectedFacility,
                'frames': reservationFrames, 
            }
        except selectedFacility.DoesNotExist:
            raise Http404("Facility does not exist")
        #return render(request, "booking/auth/guest/facility_index.html", param)
        return HttpResponse("You're looking at reservation_frame")