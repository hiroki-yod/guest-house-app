from django import forms
from booking.models import Facility, Room


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'post_code', 'address', 'bio', 'website']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', 'facility']