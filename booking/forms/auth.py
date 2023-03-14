from booking.models import HostUser, GuestUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class HostSignupForm(UserCreationForm):
    class Meta:
        model = HostUser
        fields = ['username', 'email', 'password1', 'password2', 'birth_date']


class GuestSignupForm(UserCreationForm):
    class Meta:
        model = GuestUser
        fields = ['username', 'email', 'password1', 'password2', 'birth_date']


class LoginForm(AuthenticationForm):
    pass