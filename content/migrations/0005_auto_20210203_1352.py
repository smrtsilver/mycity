# Generated by Django 3.1.4 on 2021-02-03 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_sub_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='subgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='content.group'),
        ),
        migrations.DeleteModel(
            name='sub_group',
        ),
    ]
