from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms.host import FacilityForm
from booking import models


class facility_register(View):

    def get(self, request):
        form = FacilityForm()
        param = {'form': form}
        return render(request, "booking/host/facility_register.html", param)

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
            facility = models.Facility(
                name = name,
                post_code = post_code,
                address = address,
                bio = bio,
                website = website,
                host = host
            )
            facility.save()
        return redirect('/')