# Generated by Django 5.0.6 on 2024-06-09 05:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_order_price_alter_order_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='approve',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(upload_to='photos/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]