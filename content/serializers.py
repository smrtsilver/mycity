from rest_framework import serializers

from accounts.serializers import userserializer, profileserializer
from content.models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("image",)


class topcontentserializers(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    # image = ImageSerializer(many=True, source="album.get_images")
    number_of_likes = serializers.ReadOnlyField()
    class Meta:
        model = base_content
        fields = ("id","title", "image", "number_of_likes")
    def get_image(self, obj):
        results = obj.get_main_pic()
        ser = ImageSerializer(results, many=True)
        return ser.data


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
    base_content.objects.all()

    class Meta:
        model = base_content
        exclude = ('valid', 'create_time', 'update_time',)
        # read_only_fields = ()

    # def get_topN(self, obj):
    #     results = sorted(content.objects.all(), key=lambda m: m.number_of_likes,reverse=True)[:2]
    #     ser = topcontentserializers(results, many=True)
    #     return ser.data

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
