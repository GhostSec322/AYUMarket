# Generated by Django 5.0.6 on 2024-06-16 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='이름')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='이메일')),
                ('password', models.CharField(max_length=100, verbose_name='비밀번호')),
                ('phone', models.CharField(max_length=20, verbose_name='전화번호')),
                ('bank', models.CharField(choices=[('kb', '국민은행'), ('shinhan', '신한은행'), ('woori', '우리은행'), ('hana', '하나은행'), ('nh', '농협은행'), ('ibk', '기업은행'), ('keb', '외환은행'), ('sc', 'SC제일은행'), ('citi', '씨티은행'), ('kbank', '케이뱅크'), ('kakao', '카카오뱅크')], max_length=10, verbose_name='은행명')),
                ('account_number', models.CharField(max_length=20, verbose_name='계좌번호')),
            ],
            options={
                'verbose_name': '판매자',
                'verbose_name_plural': '판매자들',
            },
        ),
        migrations.DeleteModel(
            name='Example',
        ),
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(upload_to='base/photos/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]