# Generated by Django 3.1.4 on 2021-02-13 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='user_connect',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
    ]
