from rest_framework import serializers


class loginserializers(serializers.Serializer):
    username = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)

class signupserializers(serializers.Serializer):
    username = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)
    city = serializers.CharField(required=True)

class resetserializers(serializers.Serializer):
    username = serializers.IntegerField(required=True)
    oldpassword = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
class smsserializers(serializers.Serializer):
    username=serializers.IntegerField(required=True)
    smscode=serializers.IntegerField(required=False)
    sendsms=serializers.BooleanField(required=True)


class userserializer(serializers.ModelSerializer):
    class Meta:
        pass


def PhoneNumberSerializer():
    return None