import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CommonUser(AbstractUser):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    birth_date = models.DateField()

    REQUIRED_FIELDS = ['uid', 'birth_date']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = ('CommonUser')


class HostUser(CommonUser):
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = ('HostUser')


class GuestUser(CommonUser):
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = ('GuestUser')


class Facility(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    post_code = models.CharField(max_length=7)
    address = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='images/', null=True)
    bio = models.CharField(max_length=400, blank=True)
    website = models.URLField(blank=True)
    host = models.ForeignKey(to=HostUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_name = models.CharField(max_length=100)    #後でnameに変更
    event_detail = models.CharField(max_length=1000)
    facility = models.ForeignKey(to=Facility, on_delete=models.CASCADE)
    host = models.ForeignKey(to=HostUser, on_delete=models.DO_NOTHING)
    begin_date = models.DateField()
    end_date = models.DateField()
    deadline = models.DateField()
    max_participants = models.IntegerField()
    current_participants = models.IntegerField(default=0)
    def __str__(self):
        return self.facility.name + '_' + self.event_name

class EventApplication(models.Model):
    event = models.ForeignKey(to=Facility, on_delete=models.CASCADE)
    guestuser = models.ForeignKey(to=GuestUser, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    comment = models.CharField(max_length=1000)
    def __str__(self):
        return str(self.date) + '_' + self.event.facility.name + '_' + self.event.event_name


class Room(models.Model):
    room_name = models.CharField(max_length=100)    #後でnameに変更
    facility = models.ForeignKey(to=Facility, on_delete=models.CASCADE)

    def __str__(self):
        return self.facility.name + '_' + self.room_name

class ReservationFrame(models.Model):
    date = models.DateField()
    is_reserved = models.BooleanField(default=False)
    room = models.ForeignKey(to=Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.date) + '_' + self.room.facility.name + '_' + self.room.room_name


class Reservation(models.Model):
    is_canceled = models.BooleanField(default=False)
    is_checked_in = models.BooleanField(default=False)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guest = models.ForeignKey(to=GuestUser, on_delete=models.SET_NULL, null=True)   #たぶんnullじゃよくない
    room = models.ForeignKey(to=Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.check_in_date) + '_' + self.room.facility.name + '_' + self.guest.username