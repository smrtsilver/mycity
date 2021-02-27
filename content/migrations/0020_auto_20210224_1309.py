# Generated by Django 3.1.4 on 2021-02-24 09:39

import content.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210224_1309'),
        ('content', '0019_auto_20210224_1132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='base_content',
            options={'verbose_name': 'آگهی', 'verbose_name_plural': 'آگهی ها'},
        ),
        migrations.AlterModelOptions(
            name='bookmark',
            options={'verbose_name': 'علاقه مندی ها', 'verbose_name_plural': 'علاقه مندی'},
        ),
        migrations.AlterModelOptions(
            name='citymodel',
            options={'verbose_name': 'شهر', 'verbose_name_plural': 'شهر'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name_plural': 'گروه'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-mainpic'], 'verbose_name': 'عکس', 'verbose_name_plural': 'عکس'},
        ),
        migrations.AlterModelOptions(
            name='imagealbum',
            options={'verbose_name': 'آلبوم', 'verbose_name_plural': 'آلبوم'},
        ),
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': 'لایک ها', 'verbose_name_plural': 'لایک'},
        ),
        migrations.AlterField(
            model_name='base_content',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='base_content',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile', verbose_name='نویسنده'),
        ),
        migrations.AlterField(
            model_name='base_content',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='content_city', to='content.citymodel', verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='base_content',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='base_content',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.group', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='base_content',
            name='phonenumber',
            field=models.CharField(max_length=12, verbose_name='شماره تماس'),
        ),
        migrations.AlterField(
            model_name='base_content',
            name='title',
            field=models.CharField(max_length=20, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='base_content',
            name='valid',
            field=models.BooleanField(blank=True, choices=[(True, 'تایید'), (False, 'تایید نشد')], null=True, verbose_name='تایید شدن'),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='content_connect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_bookmark', to='content.base_content', verbose_name='آگهی'),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='user_connect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_bookmarks', to='accounts.profile', verbose_name='پروفایل کاربر'),
        ),
        migrations.AlterField(
            model_name='citymodel',
            name='city_name',
            field=models.CharField(max_length=20, verbose_name='نام شهر'),
        ),
        migrations.AlterField(
            model_name='group',
            name='category_title',
            field=models.CharField(max_length=50, unique=True, verbose_name='عنوان دسته بندی'),
        ),
        migrations.AlterField(
            model_name='group',
            name='image',
            field=models.ImageField(upload_to='category_images', verbose_name='تصویر دسته بندی'),
        ),
        migrations.AlterField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='content.group', verbose_name='دسته بندی والد'),
        ),
        migrations.AlterField(
            model_name='group',
            name='slider',
            field=models.BooleanField(default=False, verbose_name='قابلیت اسلایدر'),
        ),
        migrations.AlterField(
            model_name='image',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagesA', to='content.imagealbum', verbose_name='آلبوم'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default='no-image.png', upload_to=content.models.get_upload_path, verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='image',
            name='mainpic',
            field=models.BooleanField(default=False, verbose_name='تصویر اصلی'),
        ),
        migrations.AlterField(
            model_name='like',
            name='content_connect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='content.base_content', verbose_name='آگهی'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user_connect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile', verbose_name='پروفایل کاربر'),
        ),
    ]
