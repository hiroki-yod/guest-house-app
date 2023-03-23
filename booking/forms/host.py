from django import forms
from booking.models import Facility, Room, Event


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'post_code', 'address', 'bio', 'website']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', 'facility']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'facility', 'host', 'event_detail', 'begin_date', 'end_date','deadline', 'max_participants']