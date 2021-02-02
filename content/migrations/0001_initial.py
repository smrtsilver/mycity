# Generated by Django 3.1.4 on 2021-02-02 07:01

import content.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('city', models.CharField(max_length=20)),
                ('valid', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
        migrations.CreateModel(
            name='group',
            fields=[
                ('category_title', models.CharField(max_length=50)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='category_images')),
            ],
        ),
        migrations.CreateModel(
            name='platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='city_prob',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.content')),
                ('district', models.CharField(max_length=20)),
            ],
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='employment',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='content.content')),
                ('salary', models.IntegerField()),
                ('address', models.CharField(max_length=100)),
            ],
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='tariff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('prize', models.IntegerField()),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.platform')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=content.models.get_upload_path)),
                ('content_connect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='content.content')),
            ],
        ),
        migrations.AddField(
            model_name='content',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.group'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
                ('blogpost_connected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='content.content')),
            ],
        ),
    ]
