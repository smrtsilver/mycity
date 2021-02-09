from rest_framework import serializers

from accounts.serializers import userserializer, profileserializer
from content.models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("image",)

class topcontentserializers(serializers.ModelSerializer):
    image = ImageSerializer(many=True, source="album.get_images")
    class Meta:
        model = content
        fields = ("title",)
class contentserializers(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # profile= serializers.ReadOnlyField(source='profile.field_in_profile')
    # author=profileserializer()
    # author = serializers.ReadOnlyField(source='author.user.fullname',default="بی نام")
    profileimage = profileserializer(source="author", read_only=True)
    image = ImageSerializer(many=True, source="album.get_images")
    fulltime = serializers.ReadOnlyField()
    number_of_comments = serializers.ReadOnlyField()
    number_of_likes = serializers.ReadOnlyField()
    content.objects.all()
    class Meta:
        model = content
        exclude = ('valid', 'create_time', 'update_time',)
        # read_only_fields = ()

    def to_representation(self, instance):
        ret = super(contentserializers, self).to_representation(instance)
        profile=ret.pop("profileimage")
        ret.update({"profileiamge":profile["profile_image"]})
        ret.update({"user" : profile["fullname"]})

        #
        # representation = {
        #     'image': self.profileimage.data
        #                  }

        return ret

        # todo use this to check if name is None or not

    # artist_name = serializers.SerializerMethodField('get_artists_name')
    #
    # def get_artists_name(self, obj):
    #     return obj.artist.name

    # def clean(self):
    #     super.clean()
    # def clean_title(self):
    #     raise ""
    # return


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
