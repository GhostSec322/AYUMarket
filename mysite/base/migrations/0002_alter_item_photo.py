# Generated by Django 5.0.6 on 2024-05-26 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.CharField(max_length=255),
        ),
    ]
