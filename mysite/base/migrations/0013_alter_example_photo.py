# Generated by Django 5.0.6 on 2024-06-10 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_example_photo_alter_order_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='example',
            name='photo',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]
