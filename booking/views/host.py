from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms.host import FacilityForm, RoomForm
from booking.models import Facility, Room, ReservationFrame
from datetime import datetime, timedelta


class facility_list(View):

    def get(self, request):
        facilities = Facility.objects.filter(host=request.user.hostuser)
        param = {'facilities': facilities}
        return render(request, "booking/host/facility/list.html", param)


class facility_register(View):

    def get(self, request):
        form = FacilityForm()
        param = {'form': form}
        return render(request, "booking/host/facility/register.html", param)

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

    def get(self, request):
        form = RoomForm()
        form.fields['facility'].queryset = Facility.objects.filter(host=request.user.hostuser)
        param = {'form': form}
        return render(request, "booking/host/room/register.html", param)

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