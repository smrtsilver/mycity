from rest_framework import serializers

from Log.models import log_action, VersionModel, FeedbackModel


class logactionserializers(serializers.ModelSerializer):

    class Meta:
        model=log_action
        exclude=("date_time",)

        extra_kwargs = {
            'user_connect': {'write_only': True},
            'content_connect': {'write_only': True},
            'action': {'write_only': True},
        }

    def create(self,validated_data):

        obj=super().create(validated_data)
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return obj
        else:
            obj.user_connect=user.userprofile
            obj.save()
            return obj

class feedbackserializers(serializers.ModelSerializer):

    class Meta:
        model=FeedbackModel
        exclude=("date_time","status")

        extra_kwargs = {
            'user_connect': {'write_only': True},
            'description': {'write_only': True},
        }

    def create(self,validated_data):

        obj=super().create(validated_data)
        request = self.context.get('request')
        user = request.user
        obj.user_connect=user.userprofile
        obj.save()
        return obj

class statusserializers(serializers.ModelSerializer):
    class Meta:
        model=VersionModel
        fields = ("versionCode",)
