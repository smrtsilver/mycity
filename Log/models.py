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
