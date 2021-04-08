# Generated by Django 3.1.4 on 2021-04-06 08:36

from django.db import migrations, models
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='create_time',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='items',
            field=models.TextField(verbose_name='توضیحات'),
        ),
    ]
