from django.views.generic import View
from django.shortcuts import render, redirect
from booking.forms import auth
from django.contrib.auth import login, logout


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


class login(View):

    def get(self, request):
        form = auth.LoginForm()
        param = {'form': form,}
        return render(request, 'booking/auth/login.html', param)
    
    def post(self, request):
        form = auth.LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
        return redirect('/')


class logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')