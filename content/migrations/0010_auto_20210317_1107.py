# Generated by Django 3.1.4 on 2021-03-17 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_auto_20210317_1100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='platformmodel',
            options={'verbose_name': 'پلتفرم', 'verbose_name_plural': 'پلتفرم'},
        ),
        migrations.AlterModelOptions(
            name='tariffmodel',
            options={'verbose_name': 'تعرفه', 'verbose_name_plural': 'تعرفه'},
        ),
        migrations.AlterField(
            model_name='platformmodel',
            name='name',
            field=models.CharField(max_length=20, verbose_name='اسم پلتفرم'),
        ),
        migrations.AlterField(
            model_name='tariffmodel',
            name='description',
            field=models.CharField(max_length=100, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='tariffmodel',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tariff_platform', to='content.platformmodel', verbose_name='مربوط به پلتفرم'),
        ),
        migrations.AlterField(
            model_name='tariffmodel',
            name='prize',
            field=models.PositiveIntegerField(verbose_name='قیمت'),
        ),
    ]
