# Generated by Django 4.1.2 on 2023-02-22 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_alter_client_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 11, 37, 3, 15320, tzinfo=datetime.timezone.utc), verbose_name='date of entry'),
        ),
    ]
