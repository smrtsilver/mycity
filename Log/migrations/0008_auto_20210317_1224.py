# Generated by Django 3.1.4 on 2021-03-17 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Log', '0007_auto_20210317_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackmodel',
            name='status',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'مفید'), (2, 'غیرمفید')], null=True, verbose_name='وضعیت'),
        ),
    ]
