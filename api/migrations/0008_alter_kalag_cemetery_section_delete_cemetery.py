# Generated by Django 5.0.6 on 2024-08-15 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_cemetery_remove_rental_posted_by_kalag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kalag',
            name='cemetery_section',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='Cemetery',
        ),
    ]