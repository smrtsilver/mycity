# Generated by Django 3.1.4 on 2021-04-03 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0042_auto_20210401_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base_content',
            name='Special',
            field=models.BooleanField(default=False, verbose_name='ویژه'),
        ),
        migrations.CreateModel(
            name='TariffOptionsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptions', models.TextField()),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('tariff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tabsare', to='content.tariffmodel')),
            ],
            options={
                'verbose_name': 'تبصره',
            },
        ),
    ]
