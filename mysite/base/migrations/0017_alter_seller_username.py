# Generated by Django 5.0.6 on 2024-06-16 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_seller_is_superuser_alter_seller_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name='사용자 이름'),
        ),
    ]
