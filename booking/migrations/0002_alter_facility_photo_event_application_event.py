# Generated by Django 4.1.7 on 2023-03-22 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='photo',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.CreateModel(
            name='Event_application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_present', models.BooleanField(default=False)),
                ('comment', models.CharField(max_length=1000)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.facility')),
                ('guestuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.guestuser')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('event_detail', models.CharField(max_length=1000)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('deadline', models.DateField()),
                ('max_paticipants', models.IntegerField()),
                ('current_paticipants', models.IntegerField(default=0)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.facility')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='booking.hostuser')),
            ],
        ),
    ]
