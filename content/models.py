import jdatetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import profile
from django_jalali.db import models as jmodels

# from content.utils import foreingkeylimit
# from content.utils import find_by_key


#
from content.utils import compress


def get_upload_path(instance, filename):
    # model = instance.content.__class__._meta
    year = instance.album.album.create_time.date().year
    month = instance.album.album.create_time.date().month
    albumid = instance.album.id
    return f'{year}-{month}/{albumid}/{filename}'


# def get_album_name(instance,):
#     name = instance.modelAlbum.title
#     # group = instance.modelAlbum.group.category_title
#     return f"{name}-{group}"


# def get_image_filename(instance, filename):
#     title = instance.post.title
#     slug = slugify(title)
#     return "post_images/%s-%s" % (slug, filename)

class Image(models.Model):
    class Meta:
        ordering = ["-mainpic"]

    image = models.ImageField(upload_to=get_upload_path, default="no-image.png")
    album = models.ForeignKey("ImageAlbum", related_name="imagesA", on_delete=models.CASCADE)
    mainpic = models.BooleanField(default=False)

    def __str__(self):
        return str(self.album.id)

    def save(self, *args, **kwargs):
        if self.mainpic:
            try:
                temp = Image.objects.get(mainpic=True)
                if self != temp:
                    temp.mainpic = False
                    temp.save()
            except Image.DoesNotExist:
                pass
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)
        # super(Image, self).save(*args, **kwargs)
        # instance = super(Image, self).save(*args, **kwargs)
        # image = Image.open(instance.photo.path)
        # image.save(instance.photo.path, quality=50, optimize=True)
        # return instance
        # else:
        #
        #     try:
        #         temp= Image.objects.get(mainpic=True)
        #
        #     except:
        #
        #         self.mainpic = True
        #         self.save()

    # content_connect = models.ForeignKey("content", related_name='images', on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)
    # default = models.BooleanField(default=False)
    # width = models.FloatField(default=100)
    # length = models.FloatField(default=100)


class base_content(models.Model):
    valid_choices = (
        (True, "تایید"),
        (False, "تایید نشد")
    )

    author = models.ForeignKey(profile, on_delete=models.CASCADE)
    group = models.ForeignKey("group", on_delete=models.PROTECT)
    title = models.CharField(max_length=20)
    description = models.TextField()
    create_time = jmodels.jDateTimeField(auto_now_add=True)
    update_time = jmodels.jDateTimeField(auto_now=True)
    city = models.ForeignKey("citymodel", on_delete=models.DO_NOTHING, related_name="content_city", null=True)
    valid = models.BooleanField(blank=True, null=True, choices=valid_choices)
    phonenumber = models.CharField(max_length=12)
    address = models.TextField(null=True, blank=True)
    NOTSHOW = models.BooleanField(default=False)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def delete_post(self):
        self.NOTSHOW = True
        return True

    # todo share post
    def get_main_pic(self):
        return self.modelAlbum.get_main_image()

    def get_date(self):
        year = self.create_time.date().year
        day = self.create_time.date().day
        month = self.create_time.date().month
        return f"{year}/{day}/{month}"

    def get_time(self):
        hour = self.create_time.time().hour
        minute = self.create_time.time().minute
        second = self.create_time.time().second
        return f"{hour}:{minute}:{second}"

    def get_bookmark(self, user_id):
        return self.post_bookmark.filter(user_connect_id=user_id)

    def get_like(self, user_id):
        return self.likes.filter(user_connect_id=user_id)

    @property
    def get_album(self):
        return self.modelAlbum

    @property
    def fulltime(self):
        date = self.get_date()
        time = self.get_time()
        return f"{date} {time}"

    @property
    def number_of_comments(self):
        return Comment.objects.filter(blogpost_connected=self).filter(approved_comment=True).count()

    @property
    def number_of_likes(self):
        return like.objects.filter(content_connect=self).count()

    @property
    def content_city(self):
        return self.city.city_name

    def __str__(self):
        return self.title
    # ToDo compress image

    # create_time = models.DateTimeField(auto_now=True)
    # image = models.Imag()eField
    # content_connect = models.ForeignKey("content", related_name='images', on_delete=models.CASCADE)
    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     if not self.id:
    #         self.created = timezone.now()
    #     self.modified = timezone.now()
    #     return super(User, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('blogpost-detail', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 400 or img.width > 400:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class citymodel(models.Model):
    city_name = models.CharField(max_length=20)

    def __str__(self):
        return self.city_name


class Comment(models.Model):
    class Meta:
        ordering = ['create_time']

    blogpost_connected = models.ForeignKey(
        base_content, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(profile, on_delete=models.CASCADE)
    # todo set default for on_delete
    text = models.TextField()
    create_time = jmodels.jDateTimeField(auto_now_add=True)

    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]


class bookmark(models.Model):
    content_connect = models.ForeignKey(base_content, related_name="post_bookmark", on_delete=models.CASCADE)
    user_connect = models.ForeignKey(profile, on_delete=models.CASCADE, related_name="profile_bookmarks")

    def __str__(self):
        return f"{self.content_connect}-{self.user_connect}"


class like(models.Model):
    content_connect = models.ForeignKey(base_content, related_name="likes", on_delete=models.CASCADE)
    user_connect = models.ForeignKey(profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content_connect}-{self.user_connect}"

    def dislike(self):
        self.delete()


class city_prob(base_content):
    district = models.CharField(max_length=20)

    # group = models.ForeignKey("group", on_delete=models.CASCADE, limit_choices_to={"category_title":"مشکلات شهری"})
    def create_instance(self):
        pass


class news(models.Model):
    pass


class realstate(models.Model):
    pass


class employment(base_content):
    salary = models.IntegerField()
    # address = models.CharField(max_length=100)
    # bime=models.CharField(max_length=10)


class group(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="child")
    category_title = models.CharField(max_length=50, unique=True, blank=False, null=False)
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="category_images")

    def __str__(self):
        return ' {} ({})'.format(self.category_title, self.id)

    @property
    def has_child(self):
        if self.child.all().count():
            return True
        else:
            return False

    def path(self):
        full_path = [self.category_title]
        k = self.parent
        while k is not None:
            full_path.append(k.parent)
            k = k.parent
        return ' -> '.join(full_path[::-1])


# class sub_group(models.Model):
#     category_connect = models.ForeignKey(group, related_name="sub_group", on_delete=models.CASCADE)
#     sub_categoryname = models.CharField(max_length=50, unique=True, blank=False, null=False)
#     id = models.AutoField(primary_key=True)
#
#     def __str__(self):
#         return ' {} ({})'.format(self.sub_categoryname, self.id)
class platform(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class tariff(models.Model):
    platform = models.ForeignKey(platform, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    prize = models.IntegerField()

    def __str__(self):
        return "{} - {} ".format(self.platform, self.description)


# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE)


# class Table(Product):
#     length = models.FloatField()
#     width = models.FloatField()
#
#
# class Apple(Product):
#     weight = models.FloatField()


# class BlogPost(models.Model):
#     name = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE)
class ImageAlbum(models.Model):
    album = models.OneToOneField("base_content", related_name='modelAlbum', on_delete=models.CASCADE, null=True,
                                 editable=False)

    # class Meta:
    #     verbose_name="آلبوم"
    #     verbose_name_plural="آلبوم ها"
    # albumname = models.CharField(max_length=30, default=get_album_name, editable=False)
    def get_images(self):
        image = self.imagesA.all()
        return image

    def set_images(self, images):
        for i in images:
            self.imagesA.create(image=i)

    def get_main_image(self):
        return self.imagesA.filter(mainpic=True)

    def default(self):
        return self.imagesA.filter(default=True).first()

    def thumbnails(self):
        return self.imagesA.filter(width__lt=100, length_lt=100)

    def __str__(self):
        return f"{str(self.id)}"

    @receiver(post_save, sender=city_prob)
    @receiver(post_save, sender=employment)
    @receiver(post_save, sender=news)
    @receiver(post_save, sender=base_content)
    def create_or_update_album(sender, instance, created, **kwargs):
        if created:
            ImageAlbum.objects.create(album=instance)

        # instance.ImageAlbum.save()


@receiver(pre_save, sender=base_content)
def do_something_if_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass  # Object is new, so field hasn't technically changed, but you may want to do something else here.
    else:
        if not obj.valid == instance.valid:
            if instance.valid:  # Field has changed
                print("hi")
