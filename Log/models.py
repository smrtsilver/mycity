from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels
# Create your models here.
from accounts.models import profile
from content.models import base_content


class log_action(models.Model):
    action_choices = ((1, "View post"),
                      (2, "Call number"))
    user_connect = models.ForeignKey(profile, on_delete=models.DO_NOTHING, null=True, related_name="log_profile")
    content_connect = models.ForeignKey(base_content, on_delete=models.DO_NOTHING, related_name="log_content")

    action = models.SmallIntegerField(choices=action_choices)
    date_time = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_connect.id}"


class VersionModel(models.Model):
    class Meta:
        ordering = ["create_time"]

    choices = (
        (0, "deactive"),
        (1, "active"),
    )
    versionCode = models.PositiveSmallIntegerField()
    create_time = jmodels.jDateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=choices, default=0)

    # url=models.URLField()

    def __str__(self):
        return str(self.versionCode)


class FeedbackModel(models.Model):
    class Meta:
        verbose_name="انتقادات و پیشنهادات"
        verbose_name_plural="انتقادات و پیشنهادات"
    choices=((1,"مفید"),
             (2,"غیرمفید"))
    description = models.TextField(verbose_name="توضیحات")
    user_connect= models.ForeignKey("accounts.profile",verbose_name="توسط کاربر",on_delete=models.PROTECT)
    status=models.PositiveSmallIntegerField(verbose_name="وضعیت",choices=choices,null=True,blank=True)
    date_time = jmodels.jDateTimeField(verbose_name="زمان ثبت",auto_now_add=True,editable=False)

    def __str__(self):
        return str(self.id)

    def get_date(self):
        year = self.date_time.date().year
        day = self.date_time.date().day
        month = self.date_time.date().month
        hour = self.date_time.time().hour
        minute = self.date_time.time().minute
        second = self.date_time.time().second
        time=f"{hour}:{minute}:{second}"
        date=f"{year}/{day}/{month}"
        return f"{time} - {date}"


