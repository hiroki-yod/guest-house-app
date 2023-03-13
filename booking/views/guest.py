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
            selected_facility = Facility.objects.get(pk=selected_facility_id)
            rooms = Room.objects.filter(facility_id=selected_facility_id)
            reservation_frames = ReservationFrame.objects.filter(room_id__in = rooms).order_by("date")
            available_dates = reservation_frames.distinct().values_list('date')

            #availableDatesの要素availableDateはtupple配列になっており、availableDate[0]としないとdatetime型で取り出せない。これは不便なので修正しておく
            #availableDateLists はdatetime型の配列であり、予約可能な日時を重複なしで持っている
            available_date_lists = []
            for available_date in available_dates:
                available_date_lists.append(available_date[0])

            #capacity_listはavailable_date_listsとkeyが対応しており、その日付における空き部屋の数を格納している
            capacity_list = []
            for available_date in available_date_lists:
                capacity_list.append(reservation_frames.filter(date = available_date).count())

            #available_date_listsとcapacity_listを結合する
            available_frames = []
            for i in range(len(capacity_list)):
                available_frames.append({"date":available_date_lists[i],"number":capacity_list[i]})

            
            param = {
                'facility':selected_facility,
                'capacity_list': capacity_list,
                'available_frames': available_frames,
            }
        except selected_facility.DoesNotExist:
            raise Http404("Facility does not exist")
        return render(request, "booking/auth/guest/reserve_frame.html", param)