from django.http import HttpResponse, Http404
from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms import auth
from ..models import Facility, ReservationFrame, Room
import datetime

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
            reservation_frames = ReservationFrame.objects.filter(is_reserved = 0).filter(room_id__in = rooms).order_by("date")
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

            #available_date_listsとcapacity_listを結合する。一応対応する予約枠のidもつけておく(実装に応じて要変更)
            available_frames = []
            for i in range(len(capacity_list)):
                first_frame = ReservationFrame.objects.filter(is_reserved = 0).filter(room_id__in = rooms).filter(date = available_date_lists[i]).first()
                available_frames.append({"date":available_date_lists[i],"number":capacity_list[i], \
                                         "first_frame_id":first_frame.id})

            
            param = {
                'facility':selected_facility,
                'capacity_list': capacity_list,
                'available_frames': available_frames,
            }
        except selected_facility.DoesNotExist:
            raise Http404("Facility does not exist")
        return render(request, "booking/auth/guest/reserve_frame.html", param)

#チェックイン先のfacilityとチェックイン日付(リンク生成の都合上reservation_frameで渡している)が与えられたとき、チェックアウト可能な最も遅い日付をdeadlineに格納する。
#チェックアウト可能な最も遅い日付 == チェックイン日付から、利用可能なreservation_frameが連続的に確保できる日付
#while文を与えているので、雑に編集すると無限ループの可能性があるので注意。
class reserve_frame_apply(View):
    def get(self, request, selected_facility_id, selected_frame_id):
        if ReservationFrame.objects.filter(is_reserved = 0).filter(pk=selected_frame_id).exists():
            selected_reservation = ReservationFrame.objects.filter(is_reserved = 0).filter(pk=selected_frame_id).get()
            deadline = ReservationFrame.objects.filter(is_reserved = 0).filter(pk=selected_frame_id).first().date
            rooms = Room.objects.filter(facility_id=selected_facility_id)
            while ReservationFrame.objects.filter(is_reserved = 0).filter(room_id__in = rooms).filter(date__gt=deadline).exists():
                deadline = deadline + datetime.timedelta(days=1)
                print(deadline)
            param = {'selected_reservation': selected_reservation,
                     'facility' : Facility.objects.get(pk=selected_facility_id), 
                     'selected_date':selected_reservation.date.isoformat(), 
                     'deadline':deadline.isoformat()}
            return render(request, 'booking/auth/guest/reserve_apply.html', param)
        else:
            return HttpResponse("空いている予約枠がありません。")
        
