# Generated by Django 4.1.2 on 2023-02-19 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_alter_client_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='agent',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_staff': False, 'is_superuser': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clients', to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='agent'),
        ),
    ]
