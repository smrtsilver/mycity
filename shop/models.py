import json

from django.db import models
from django_jalali.db import models as jmodels
# Create your models here.
class paymentModel(models.Model):
    class Meta:
        verbose_name="اطلاعات پرداخت"
        verbose_name_plural="اطلاعات پرداخت"
    choices=(
        (1,"پرداخت موفق"),
        (2,"پرداخت ناموفق"),
        (3,"کنسل شده"),
    )
    receipt=models.CharField(max_length=100, verbose_name="رسید بانکی")
    userpayment=models.ForeignKey("accounts.profile",on_delete=models.PROTECT,related_name="payment_profile",verbose_name="توسط کاربر ")
    # contentpayment=models.ForeignKey("content.base_content",on_delete=models.PROTECT,verbose_name="مربوط به آگهی")
    status=models.SmallIntegerField(choices=choices,null=True,verbose_name="وضعیت پرداخت")
    totalpayment=models.PositiveIntegerField(verbose_name="پرداختی")
    desc=models.TextField(verbose_name="توضیحات")
    create_time = jmodels.jDateTimeField(auto_now_add=True,verbose_name="تاریخ پرداخت")

    def set_desc(self, x):
        self.desc = json.dumps(x)

    def get_desc(self):
        return json.loads(self.desc)