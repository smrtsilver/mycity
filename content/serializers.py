from rest_framework import serializers

from content.models import *


class contentserializers(serializers.ModelSerializer):
    class Meta:
        model = content
        fields = "__all__"
        read_only_fields = ("create_time", "update_time")

    # def clean(self):
    #     super.clean()
    # def clean_title(self):
    #     raise ""
    # return

class getcontentserializers(serializers.ModelSerializer):
    class Meta:
        model = content
        fields = "__all__"

    # group_id = serializers.IntegerField()
    #   TODO sth
    def query(self):
        pass  # self.group_id

class groupserializers(serializers.ModelSerializer):
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
