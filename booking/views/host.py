from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms.host import FacilityForm, RoomForm, EventForm
from booking.models import Facility, Room, ReservationFrame, Event, EventApplication
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..decorators import host_login_required
#ホストでログインしている場合のみ表示するための関数をdecorators.pyに定義した
#@method_decorator(host_login_required)で認証できる

class facility_list(View):
    @method_decorator(host_login_required)
    def get(self, request):
        facilities = Facility.objects.filter(host=request.user.hostuser)
        param = {'facilities': facilities}
        return render(request, "booking/host/facility/list.html", param)


class facility_register(View):
    @method_decorator(host_login_required)
    def get(self, request):
        form = FacilityForm()
        param = {'form': form}
        return render(request, "booking/host/facility/register.html", param)
    
    @method_decorator(host_login_required)
    def post(self, request):
        form = FacilityForm(request.POST)
        if form.is_valid():
            #必要なデータ
            name = form.cleaned_data['name']
            post_code = form.cleaned_data['post_code']
            address = form.cleaned_data['address']
            bio = form.cleaned_data['bio']
            website = form.cleaned_data['website']
            host = request.user.hostuser
            #保存処理
            facility = Facility(
                name = name,
                post_code = post_code,
                address = address,
                bio = bio,
                website = website,
                host = host
            )
            facility.save()
        return redirect('/')

class room_register(View):
    @method_decorator(host_login_required)
    def get(self, request):
        form = RoomForm()
        form.fields['facility'].queryset = Facility.objects.filter(host=request.user.hostuser)
        param = {'form': form}
        return render(request, "booking/host/room/register.html", param)
    
    @method_decorator(host_login_required)
    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            #予約枠自動生成
            date_time = datetime.now()
            room = Room.objects.order_by('id').reverse().first()
            for i in range(7):
                date_time += timedelta(days=1)
                date = date_time.date()
                reservation_frame = ReservationFrame(
                    date = date,
                    room = room
                )
                reservation_frame.save()
        return redirect('/')
class event_list(View):
    @method_decorator(host_login_required)
    def get(self, request):
        events = Event.objects.filter(host=request.user.hostuser)
        param = {'events': events}
        return render(request, "booking/host/event/list.html", param)


class event_register(View):
    @method_decorator(host_login_required)
    def get(self, request):
        form = EventForm()
        param = {'form': form}
        return render(request, "booking/host/event/register.html", param)
    
    @method_decorator(host_login_required)
    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            #必要なデータ
            event_name = form.cleaned_data['event_name']
            event_detail = form.cleaned_data['event_detail']
            begin_date = form.cleaned_data['begin_date']
            end_date = form.cleaned_data['end_date']
            deadline = form.cleaned_data['deadline']
            max_participants = form.cleaned_data['max_participants']
            facility = form.cleaned_data['facility']
            host = request.user.hostuser
            #保存処理
            event = Event(
                event_name = event_name, 
                event_detail = event_detail, 
                facility = facility, 
                host = host, 
                begin_date = begin_date, 
                end_date = end_date, 
                deadline = deadline, 
                max_participants = max_participants, 
            )
            event.save()
        return redirect('/')
