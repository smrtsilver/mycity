from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels
# Create your models here.
from content.models import base_content


class log_action(models.Model):
    action_choices=((1,"View post"),
                    (2,"Call number"))
    user_connect=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    content_connect=models.ForeignKey(base_content,on_delete=models.DO_NOTHING)

    action=models.SmallIntegerField(choices=action_choices)
    date_time=jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_connect.username}-{self.content_connect.id}"