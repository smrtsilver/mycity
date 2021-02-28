# Generated by Django 3.1.4 on 2021-02-27 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0026_auto_20210227_1959'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='image',
            constraint=models.UniqueConstraint(fields=('mainpic',), name='unique mainpic'),
        ),
        migrations.AlterModelTable(
            name='image',
            table='content_image',
        ),
    ]
