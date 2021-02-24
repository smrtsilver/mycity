from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from accounts.serializers import userserializer, profileserializer
from content.models import *


class ImageSerializer(serializers.ModelSerializer):
    # image = serializers.ListField(child=serializers.ImageField(required=True))
    #
    # image = serializers.ListField(
    #     child=serializers.ImageField(allow_empty_file=False)
    # )

    class Meta:
        model = Image
        fields = ("image", "album", "mainpic")

        extra_kwargs = {
            'album': {'write_only': True},
            'mainpic': {'write_only': True},
        }
    # def to_representation(self, value):
    #     if value is None:
    #         return 0
    #     return super(ImageSerializer, self).to_representation(value)
    # def create(self, validated_data):
    #     images = validated_data.pop('image')
    #     for image in images:
    #         photo = Image.objects.create(image=image, **validated_data)
    #     return photo
    # def create(self, validated_data):
    #     listingName = validated_data.get('listingName', None)
    #     property = validated_data.get('property', None)
    #     city = validated_data.get('city', None)
    #     room = validated_data.get('room', None)
    #     price = validated_data.get('price', None)
    #     image = validated_data.pop('image')
    #     return Rental.objects.create(listingName=listingName, property=property, city=city,
    #                                  room=room, price=price, image=image)

    # def create(self, validated_data):
    #
    #     for attr, value in validated_data.items():
    #         if attr == 'image':
    #             for x in value:
    #                 c = Image.objects.create(image=x, album=1)
    #                 # album=ImageAlbum.objects.get(
    #                 # modelAlbum=self.context[''].user.id).id)
    #                 c.save()
    #         return validated_data


class topcontentserializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    # image = ImageSerializer(many=True, source="album.get_images")
    number_of_likes = serializers.ReadOnlyField()

    class Meta:
        model = base_content
        fields = ("id", "title", "image", "number_of_likes")

    def get_image(self, obj):
        results = obj.get_main_pic()
        ser = ImageSerializer(results, many=True)
        return ser.data


class contentserializers(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # profile= serializers.ReadOnlyField(source='profile.field_in_profile')
    # author=profileserializer()
    # author = serializers.ReadOnlyField(source='author.user.fullname',default="بی نام")
    # image = ImageSerializer(many=True)
    # base_content.objects.all()
    profileimage = profileserializer(source="author", read_only=True)
    images = ImageSerializer(many=True, source="modelAlbum.get_images", read_only=True)
    fulltime = serializers.ReadOnlyField()
    number_of_comments = serializers.ReadOnlyField()
    number_of_likes = serializers.ReadOnlyField()
    liked = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()
    content_city=serializers.ReadOnlyField()

    class Meta:
        model = base_content
        exclude = ('create_time', 'update_time')
        # read_only_fields = ()
        extra_kwargs = {
            'author': {'read_only': True},
            "city" : {'write_only' : True}

        }

    # def get_topN(self, obj):
    #     results = sorted(content.objects.all(), key=lambda m: m.number_of_likes,reverse=True)[:2]
    #     ser = topcontentserializers(results, many=True)
    #     return ser.data

    def get_bookmarked(self, instance):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        obj = instance.get_bookmark(user.userprofile.id)
        return obj.exists()

    def get_liked(self, instance):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        obj = instance.get_like(user.userprofile.id)
        return obj.exists()

    def to_representation(self, instance):
        # Result = dict()
        ret = super(contentserializers, self).to_representation(instance)
        profile = ret.pop("profileimage")
        ret.update({"profileiamge": profile["profile_image"]})
        ret.update({"user": profile["fullname"]})
        # TOP=ret.pop("topN")
        #
        # representation = {
        #     'image': self.profileimage.data
        #                  }

        # Result["result"] = ret
        # Result.update({"TOP": TOP})
        return ret


        # def get_tax_status_all(self, obj):  # "get_" + field name
        #     return obj.tax_status(check_item_bought=False)
        # todo use this to check if name is None or not
class getcontentserializer(serializers.Serializer):
    city=serializers.IntegerField(required=True)
    skip=serializers.IntegerField(required=True)
    search=serializers.CharField(required=False)
    group=serializers.IntegerField(required=True)
    # artist_name = serializers.SerializerMethodField('get_artists_name')
    #
    # def get_artists_name(self, obj):
    #     return obj.artist.name

    # def clean(self):
    #     super.clean()
    # def clean_title(self):
    #     raise ""
    # return


# class createcontenserializers(serializers.ModelSerializer):
#     # author=serializers.SerializerMethodField()
#     # author = serializers.HiddenField(
#     #     default=serializers.CurrentUserDefault()
#     # )
#     # image = ImageSerializer(many=True)
#     # author=serializers.SerializerMethodField()
#     # author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
#     class Meta:
#         model = base_content
#         exclude = ('valid', 'create_time', 'update_time',"author")
#
#     # def get_author(self):
#     #     request = self.context.get("request")
#     #     user = request.user
#     #     return user

# class subgroupserializers(serializers.ModelSerializer):

class groupserializers(serializers.ModelSerializer):
    has_child = serializers.ReadOnlyField()

    class Meta:
        model = group
        fields = "__all__"


class tariffserializers(serializers.ModelSerializer):
    class Meta:
        model = tariff
        fields = "__all__"
        depth = 1


class cityprobserializers(serializers.ModelSerializer):
    class Meta:
        model = city_prob
        fields = "__all__"


class employmentserializers(serializers.ModelSerializer):
    class Meta:
        model = employment
        field = "__all__"


class commentserializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'text', "blogpost_connected")

# class subgrouoserializers(serializers.ModelSerializer):
#     class Meta:
#         model = sub_group
#         fields = "__all__"
# class UserAvatarSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["avatar"]
#
#     def save(self, *args, **kwargs):
#         if self.instance.avatar:
#             self.instance.avatar.delete()
#         return super().save(*args, **kwargs)
class cityserializers(serializers.ModelSerializer):

    class Meta:
        model = citymodel
        fields = "__all__"

