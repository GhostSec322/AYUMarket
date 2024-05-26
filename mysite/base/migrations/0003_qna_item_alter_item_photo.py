# Generated by Django 5.0.6 on 2024-05-26 01:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_category_qna_userlogin_item_cart_order_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='qna',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qnas', to='base.item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]
