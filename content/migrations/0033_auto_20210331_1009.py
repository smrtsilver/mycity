# Generated by Django 3.1.4 on 2021-03-31 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0032_auto_20210331_0927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tariffmodel',
            name='content_connect',
        ),
        migrations.AddField(
            model_name='base_content',
            name='tariff',
            field=models.ManyToManyField(blank=True, null=True, related_name='content_tariff', to='content.tariffModel', verbose_name='تعرفه'),
        ),
    ]
