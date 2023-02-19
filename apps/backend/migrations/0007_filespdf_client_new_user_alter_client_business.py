# Generated by Django 4.1.2 on 2023-02-19 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_client_a_meter_alter_client_zipcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilesPDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('file', models.FileField(blank=True, null=True, upload_to='file/', verbose_name='file')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='new_user',
            field=models.BooleanField(default=False, help_text='if true is a new client', verbose_name='new client'),
        ),
        migrations.AlterField(
            model_name='client',
            name='business',
            field=models.CharField(choices=[('1', 'Chelion Iberia'), ('2', 'Iberian Trade Europe'), ('3', 'Ambos')], default='1', max_length=1, verbose_name='business'),
        ),
    ]
