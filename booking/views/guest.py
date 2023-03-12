from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms import auth
from ..models import Facility

class facility_guest(View):
    def get(self, request):
        Facility_list = Facility.objects.order_by('name')[:5]
        param = {
            'Facility_list':Facility_list,
        }
        return render(request, "booking/auth/guest/facility_index.html", param)
        #return HttpResponse("You're looking at facility_index")