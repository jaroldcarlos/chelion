# Generated by Django 4.1.2 on 2023-02-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_rename_new_user_client_new_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('geoposition', models.CharField(max_length=200, verbose_name='geoposition')),
            ],
        ),
    ]
