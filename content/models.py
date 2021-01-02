from django.db import models


# Create your models here.
class content(models.Model):
    title = models.CharField(max_length=20)
    # image = models.ImageField()
    description = models.TextField()
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)
    city=models.CharField(max_length=20)

class group(models.Model):
        category_obj=models.ForeignKey(content,on_delete=models.DO_NOTHING)
        category_title=models.CharField(max_length=50,blank=False,null=False)
        # image = models.ImageField()



