# Generated by Django 5.1.1 on 2024-10-29 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_appliance_code_appliance_name_appliance_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appliance',
            old_name='code',
            new_name='brand',
        ),
        migrations.RemoveField(
            model_name='appliance',
            name='name',
        ),
        migrations.AddField(
            model_name='appliance',
            name='model',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.AddField(
            model_name='appliance',
            name='observations',
            field=models.TextField(default=''),
        ),
    ]