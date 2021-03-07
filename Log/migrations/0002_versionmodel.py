# Generated by Django 3.1.4 on 2021-03-06 07:18

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('Log', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VersionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('versionCode', models.PositiveSmallIntegerField()),
                ('create_time', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'deactive'), (1, 'active')])),
            ],
            options={
                'ordering': ['create_time'],
            },
        ),
    ]
