# Generated by Django 4.0.2 on 2022-06-21 01:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointmentDate',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.DeleteModel(
            name='PatientDischargeDetails',
        ),
    ]