# Generated by Django 5.0.6 on 2024-11-05 06:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_memories_speech'),
    ]

    operations = [
        migrations.AddField(
            model_name='kalag',
            name='qr',
            field=models.FileField(blank=True, upload_to='qrs/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='memories',
            name='qr',
            field=models.FileField(blank=True, upload_to='qrs/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])]),
        ),
    ]
