# Generated by Django 4.1.2 on 2023-02-22 09:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_alter_client_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 9, 58, 0, 473765, tzinfo=datetime.timezone.utc), verbose_name='date of entry'),
        ),
    ]
