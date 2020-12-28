from rest_framework import serializers


class loginserializers(serializers.Serializer):
    username = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)



class userserializer(serializers.ModelSerializer):
    class Meta:
        pass