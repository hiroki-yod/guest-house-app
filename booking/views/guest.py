from django.http import HttpResponse, Http404
from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms import auth
from ..models import Facility

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