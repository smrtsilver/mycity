from django.contrib.auth.models import User
from django.db import models
from accounts.models import profile
# from content.utils import foreingkeylimit


def foreingkeylimit():
    obj = content.objects.all()
    for o in obj:
        if o.returnname() == "city_prob":
            return group.objects.get(id == 2)
        elif o.returnname() == "employment":
            return group.objects.get(id=1)
        else:
            return None


def get_upload_path(instance, filename):
    # model = instance.content.__class__._meta
    model = instance.content_connect.group.category_title
    content = instance.content_connect_id
    user = instance.content_connect.author.user.username

    return f'albums/{model}/{content}-{user}/{filename}'


# def get_image_filename(instance, filename):
#     title = instance.post.title
#     slug = slugify(title)
#     return "post_images/%s-%s" % (slug, filename)

# class ImageAlbum(models.Model):
#     # class Meta:
#     #     verbose_name="آلبوم"
#     #     verbose_name_plural="آلبوم ها"
#     def default(self):
#         return self.images.filter(default=True).first()
#
#     def thumbnails(self):
#         return self.images.filter(width__lt=100, length_lt=100)
#
#     def __str__(self):
#         return str(self.id)
#

class Image(models.Model):
    content_connect = models.ForeignKey("content", related_name='images', on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_upload_path)
    # default = models.BooleanField(default=False)
    # width = models.FloatField(default=100)
    # length = models.FloatField(default=100)


#
class content(models.Model):
    # author = models.ForeignKey(profile, on_delete=models.CASCADE)
    group = models.ForeignKey("group", on_delete=models.PROTECT, limit_choices_to=foreingkeylimit,
                              default=foreingkeylimit)
    title = models.CharField(max_length=20)
    # album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE)
    # image = models.ImageField()
    description = models.TextField()
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=20)

    valid = models.BooleanField(default=False)

    def __str__(self):  # __unicode__ for Python 2
        return self.title

    def returnname(self):
        return self.__class__.__name__


class city_prob(content):
    district = models.CharField(max_length=20)

    # group = models.ForeignKey("group", on_delete=models.CASCADE, limit_choices_to={"category_title":"مشکلات شهری"})
    def create_instance(self):
        pass


class employment(content):
    salary = models.IntegerField()
    address = models.CharField(max_length=100)


class group(models.Model):
    category_title = models.CharField(max_length=50, blank=False, null=False)
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="category_images")

    def __str__(self):
        return ' {} ({})'.format(self.category_title, self.id)


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


class Comment(models.Model):
    blogpost_connected = models.ForeignKey(
        content, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(profile, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.author) + ', ' + self.blogpost_connected.title[:40]

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
