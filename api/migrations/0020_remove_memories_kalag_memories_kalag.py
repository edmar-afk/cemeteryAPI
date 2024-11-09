# Generated by Django 5.0.6 on 2024-11-09 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_remove_memories_kalag_memories_kalag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memories',
            name='kalag',
        ),
        migrations.AddField(
            model_name='memories',
            name='kalag',
            field=models.ForeignKey(default=18, on_delete=django.db.models.deletion.CASCADE, to='api.kalag'),
            preserve_default=False,
        ),
    ]
