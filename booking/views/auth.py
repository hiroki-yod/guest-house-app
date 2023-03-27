from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms import auth
from booking.models import HostUser
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist


class signup_host(View):

    def get(self, request):
        form = auth.HostSignupForm()
        param = {'form': form}
        return render(request, "booking/auth/host/signup.html", param)
    
    def post(self, request):
        form = auth.HostSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            return redirect('/signup')


class signup_guest(View):

    def get(self, request):
        form = auth.GuestSignupForm()
        param = {'form': form}
        return render(request, "booking/auth/guest/signup.html", param)
    
    def post(self, request):
        form = auth.GuestSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            return redirect('/signup')


class login_common(View):

    def get(self, request):
        form = auth.LoginForm()
        param = {'form': form,}
        return render(request, 'booking/auth/login.html', param)
    
    def post(self, request):
        form = auth.LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            try:
                user.hostuser
                return redirect('/host')
            except ObjectDoesNotExist:
                pass

            try:
                user.guestuser
                return redirect('/')
            except ObjectDoesNotExist:
                pass
        return redirect('/login')


class logout_common(View):
    def post(self, request):
        logout(request)
        return redirect('/')