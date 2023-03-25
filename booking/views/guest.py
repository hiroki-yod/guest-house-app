from django.http import HttpResponse, Http404
from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms import auth
from ..models import Facility, Reservation, ReservationFrame, Room, Event, EventApplication
import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from ..decorators import guest_login_required
from django.utils.decorators import method_decorator

class guest_mypage(View):
    @method_decorator(guest_login_required)
    def get(self, request):
        current_guest_id = request.user.guestuser.uid
        reservations = Reservation.objects.filter(guest_id = current_guest_id).order_by('check_in_date')
        event_applications_list = EventApplication.objects.filter(guestuser_id = current_guest_id).distinct().values_list('event', flat = True)
        events = Event.objects.filter(pk__in = event_applications_list)
        param={
            'reservations':reservations,
            'events':events
        }
        return render(request, "booking/guest/mypage.html", param)

class facility_index(View):
    @method_decorator(login_required)
    def get(self, request):
        Facility_list = Facility.objects.order_by('name')
        param = {
            'Facility_list':Facility_list,
            'words' : ' ', 
            'places' : ' ', 
            'selected_checkin' : datetime.datetime.now().date().isoformat(),
            'selected_checkout' : datetime.datetime.now().date().isoformat(),
        }
        return render(request, "booking/guest/facility_index.html", param)
        #return HttpResponse("You're looking at facility_index")
    
    @method_decorator(guest_login_required)
    def post(self, request):
        #検索文字列POST["words"]の全角スペースを半角スペースに変換し、半角スペースで区切る。区切った各ワードを配列wordsに格納
        words = request.POST["words"].replace("　"," ").split(" ")
        places = request.POST["places"].replace("　"," ").split(" ")


        #配列wordsの各要素wordでand検索をかける
        searched_facility_list = Facility.objects
        for word in words:
            searched_facility_list = searched_facility_list.filter(name__icontains = word)

        #placeでのor検索
        q = Q()
        for place in places:
            q.add(Q(address__icontains =place), Q.OR)
        searched_facility_list = searched_facility_list.filter(q)

        selected_checkin = datetime.datetime.strptime(request.POST["checkin"], "%Y-%m-%d").date()
        selected_checkout = datetime.datetime.strptime(request.POST["checkout"], "%Y-%m-%d").date()
        
        
        #is_date_searchがtrueのとき、checkinからcheckoutまでの日程が確保できる施設のみを検索
        if request.POST["is_date_search"] == "1":
            #チェックイン日付がチェックアウト日付より後の場合は初期値を空にしてからの絞り込み = 施設を表示しない
            if selected_checkin > selected_checkout:
                available_facilities_name = []
            else:
                #予約可能な施設の初期値は全施設 = 全集合からの絞り込みによって正常に検索を行う
                available_facilities_name = list(Facility.objects.all().distinct().values_list("name", flat=True))

            for i in range(( selected_checkout - selected_checkin).days + 1): #日付についてfor文を回す
                currentdate = selected_checkin + datetime.timedelta(i)

                #currentdateに対して空いている予約枠を取得
                current_available_frames = ReservationFrame.objects.filter(is_reserved = 0).filter(date = currentdate).order_by("date")

                #currentdateに対して空いている予約枠に属するfacilityを全て取得、施設名をcurrent_available_facilities_nameに格納
                current_available_facilities_name = []
                for current_available_frame in current_available_frames:
                    current_available_facilities_name.append(current_available_frame.room.facility.name)

                #currentdateに対して空きのある施設のみに絞り込んでいく
                available_facilities_name= list(set(available_facilities_name) & set(current_available_facilities_name)) 

            #検索結果を予約枠に空きがある施設のみに限定
            searched_facility_list = searched_facility_list.filter(name__in = available_facilities_name)
        
        #nameで並び替え
        searched_facility_list = searched_facility_list.order_by('name')
        words = ' '.join(map(str, words))
        places = ' '.join(map(str, places))
        param = {
            'Facility_list':searched_facility_list,
            'words': words, 
            'places': places, 
            'selected_checkin': selected_checkin.isoformat(),
            'selected_checkout':selected_checkout.isoformat(), 
        }
        return render(request, "booking/guest/facility_index.html", param)

class facility_detail(View):
    @method_decorator(guest_login_required)
    def get(self, request, facility_id):
        #return HttpResponse("You're looking at facility_detail")
        try:
            facility = Facility.objects.get(pk=facility_id)
            events = Event.objects.filter(facility=facility)
        except facility.DoesNotExist:
            raise Http404("Facility does not exist")
        return render(request, 'booking/guest/facility_detail.html', {'facility': facility, 'events' : events})
    
class reserve_frame_index(View):
    @method_decorator(guest_login_required)
    def get(self, request, selected_facility_id):
        try:
            selected_facility = Facility.objects.get(pk=selected_facility_id)
            rooms = Room.objects.filter(facility_id=selected_facility_id)
            reservation_frames = ReservationFrame.objects.filter(is_reserved = 0).filter(room_id__in = rooms).order_by("date")
            available_date_lists = list(reservation_frames.distinct().values_list('date', flat = True))
            
            #capacity_listはavailable_date_listsとkeyが対応しており、その日付における空き部屋の数を格納している
            capacity_list = []
            for available_date in available_date_lists:
                capacity_list.append(reservation_frames.filter(date = available_date).count())

            #available_date_listsとcapacity_listを結合する。一応対応する予約枠のidもつけておく(実装に応じて要変更)
            available_frames = []
            for i in range(len(capacity_list)):
                first_frame = ReservationFrame.objects.filter(is_reserved = 0).filter(room_id__in = rooms).filter(date = available_date_lists[i]).order_by("room_id").first()
                available_frames.append({"date":available_date_lists[i],"number":capacity_list[i], \
                                         "first_frame_id":first_frame.id})

            
            param = {
                'facility':selected_facility,
                'capacity_list': capacity_list,
                'available_frames': available_frames,
            }
        except selected_facility.DoesNotExist:
            raise Http404("Facility does not exist")
        return render(request, "booking/guest/reserve_frame.html", param)

#チェックイン先のfacilityとチェックイン日付(リンク生成の都合上reservation_frameで渡している)が与えられたとき、チェックアウト可能な最も遅い日付をdeadlineに格納する。
#チェックアウト可能な最も遅い日付 == チェックイン日付から、利用可能なreservation_frameが連続的に確保できる日付
#while文を与えているので、雑に編集すると無限ループの可能性があるので注意。
class reserve_frame_apply(View):
    @method_decorator(guest_login_required)
    def get(self, request, selected_facility_id, selected_frame_id):
        if ReservationFrame.objects.filter(is_reserved = 0).filter(pk=selected_frame_id).exists():
            selected_reservation = ReservationFrame.objects.filter(is_reserved = 0).filter(pk=selected_frame_id).get()
            deadline = ReservationFrame.objects.filter(is_reserved = 0).filter(pk=selected_frame_id).first().date
            rooms = Room.objects.filter(facility_id=selected_facility_id)
            while ReservationFrame.objects.filter(is_reserved = 0).filter(room_id__in = rooms).filter(date__gt=deadline).exists():
                deadline = deadline + datetime.timedelta(days=1)
            param = {'selected_reservation': selected_reservation,
                     'facility' : Facility.objects.get(pk=selected_facility_id), 
                     'selected_date':selected_reservation.date.isoformat(), 
                     'deadline':deadline.isoformat()}
            return render(request, 'booking/guest/reserve_apply.html', param)
        else:
            return HttpResponse("空いている予約枠がありません。")

class reserve_save(View):
    @method_decorator(guest_login_required)
    def post(self, request):
        selected_guest_id = request.user.guestuser.uid
        selected_check_in_date = datetime.datetime.strptime(request.POST["checkin"], "%Y-%m-%d")
        selected_check_out_date = datetime.datetime.strptime(request.POST["checkout"], "%Y-%m-%d")
        rooms = Room.objects.filter(facility_id=request.POST["facility_uid"])
        selected_reservation = ReservationFrame.objects.filter(is_reserved=0).filter(room_id__in=rooms).filter(date=selected_check_in_date)\
            .order_by("room_id").first()
        selected_room_id = selected_reservation.room.id

        #保存処理を行う前に、日程が確保できているか一応確認する。selected_check_in_dateからselected_check_out_dateまで、その日付かつselected_roomに空きがあることを
        #確認し、空きがあれば{exists() == True}、変更対象のframeを格納する配列reserved_framesに追加し、一つでも空きがなければ予約失敗と表示する。
        #一つも予約枠確保が失敗しなかったときのみ保存処理を実行
        reserved_frames = []
        for i in range(( selected_check_out_date - selected_check_in_date).days + 1):
            currentdate = selected_check_in_date + datetime.timedelta(i)
            reserved_frame = ReservationFrame.objects.filter(is_reserved=0).filter(room_id=selected_room_id).filter(date=currentdate)
            if reserved_frame.exists():
                reserved_frames.append(reserved_frame)
            else:
                return HttpResponse("予約枠を確保できませんでした。再度お試しください。")
        for reserved_frame in reserved_frames:
            reserved_frame = reserved_frame.get()
            reserved_frame.is_reserved = 1
            reserved_frame.save()
        Reservation.objects.create(is_canceled = 0, is_checked_in = 0, check_in_date = selected_check_in_date, check_out_date = selected_check_out_date,\
                                room_id = selected_room_id, guest_id = selected_guest_id)
        #マイページに飛ばす
        return redirect('/guest/mypage')

class guest_event_apply(View):
    @method_decorator(guest_login_required)
    def get(self, request, facility_uid, event_id):
        
        try:
            facility = Facility.objects.get(pk=facility_uid)
            event = Event.objects.get(pk=event_id)

        except facility.DoesNotExist:
            raise Http404("Facility does not exist")
        except event.DoesNotExist:
            raise Http404("event does not exist")

        return render(request, 'booking/guest/event_apply.html', {'facility': facility, 'event' : event})    

class guest_event_apply_save(View):
    @method_decorator(guest_login_required)
    def post(self, request):
        selected_guest = request.user.guestuser
        selected_event = Event.objects.get(pk=request.POST["event_id"])
        selected_facility = Facility.objects.get(pk=request.POST["facility_uid"])
        if Reservation.objects.filter(guest_id = selected_guest.uid).filter(check_in_date__lte = selected_event.begin_date)\
            .filter(check_out_date__gte = selected_event.end_date).exists():
            EventApplication.objects.create(event = selected_event, guestuser = selected_guest, comment = request.POST["comment"])
            selected_event.current_participants += 1
            selected_event.save()
            #マイページに飛ばす
            return redirect('/guest/mypage')
        else:
            return HttpResponse('まず施設予約を行なってください。')

        