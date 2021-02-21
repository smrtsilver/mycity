from rest_framework import serializers

from Log.models import log_action


class logactionserializers(serializers.ModelSerializer):

    class Meta:
        model=log_action
        exclude=("date_time",)

        extra_kwargs = {
            'user_connect': {'write_only': True},
            'content_connect': {'write_only': True},
            'action': {'write_only': True},
        }