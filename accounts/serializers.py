from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import profile


class PhoneNumberSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^(\098|98|0)?9\d{9}$',
                                      error_messages={
                                          "eeror": "Phone number must be entered in the format: '09xxxxxxxxx'. Up to "
                                                   "11 digits allowed."},required=True)


class loginserializers(serializers.Serializer):
    username = PhoneNumberSerializer()
    password = serializers.CharField(required=True)


# class signupserializers(serializers.Serializer):
#     username = serializers.IntegerField(required=True)
#     password = serializers.CharField(required=True)



class resetserializers(serializers.Serializer):
    username = serializers.IntegerField(required=True)
    oldpassword = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class smsserializers(serializers.Serializer):
    username = serializers.IntegerField(required=True)
    smscode = serializers.IntegerField(required=False)
    sendsms = serializers.BooleanField(required=True)


class userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class profileserializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField("get_fullname")

    def get_fullname(self, obj):
        if obj.user.get_full_name() == "":
            name = "بی نام"
            return name
        else:
            return obj.user.get_full_name()

    # fullname=serializers.CharField(source=get_artists_name)
    # firstname=serializers.CharField(source="user.first_name",default="بی نام")

    class Meta:
        model = profile
        fields = ("profile_image", "fullname")
