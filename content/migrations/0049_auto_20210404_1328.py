# Generated by Django 3.1.4 on 2021-04-04 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0048_auto_20210403_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariffmodel',
            name='platform',
            field=models.SmallIntegerField(choices=[(1, 'اپلیکیشن'), (2, 'تلگرام'), (3, 'اینستاگرام'), (4, 'بنر در اپلیکیشن')], verbose_name='مربوط به پلتفرم'),
        ),
    ]
