from django.views.generic import View
from django.shortcuts import render


class index(View):
    def get(self, request):
        return render(request, "booking/index.html")