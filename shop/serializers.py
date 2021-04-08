from rest_framework import serializers

from content.models import TariffOptionsModel, tariffModel
from shop.models import payment


class paymentserializer(serializers.ModelSerializer):


    class Meta:
        model = payment
        exclude = (
            "receipt",
            "userpayment",
            "create_time",
            'desc'
        )
        depth = 1

        extra_kwargs = {
            'create_time': {'read_only': True},

        }

class reqpaymentserializer(serializers.Serializer):
    tariff=serializers.ListField(required=True,allow_null=False,allow_empty=False,child=serializers.IntegerField(min_value=1))
    Notes=serializers.ListField(required=True)
    postID=serializers.IntegerField(required=True)
    totalpayment=serializers.IntegerField(required=True)



class tabsareserializer(serializers.ModelSerializer):
    class Meta:
        model = TariffOptionsModel
        fields = "__all__"
class MyChoiceField(serializers.ChoiceField):

    def to_representation(self, data):
        if data not in self.choices.keys():
            self.fail('invalid_choice', input=data)
        else:
            return self.choices[data]

    def to_internal_value(self, data):
        for key, value in self.choices.items():
            if value == data:
                 return key
        self.fail('invalid_choice', input=data)
class tariffserializers(serializers.ModelSerializer):
    platform=MyChoiceField(choices=tariffModel.pchoices)
    # tabsare = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = tariffModel
        fields = "__all__"
        depth = 1

    # def to_representation(self,obj):
    #     rep= super(tariffserializers,self).to_representation(obj)
    #     rep['events']= [ customer.platform for customer in tariffModel.objects.filter(platform=obj.platform)]
    #     return rep
    # def to_representation(self, instance):
    #     # Result = dict()
    #     ret = super(tariffModel, self).to_representation(instance)
    #     profile = ret.pop("profileimage")
    #     ret.update({"profileiamge": profile["profile_image"]})
    #     ret.update({"user": profile["fullname"]})
    #     # TOP=ret.pop("topN")
    #     #
    #     # representation = {
    #     #     'image': self.profileimage.data
    #     #                  }
    #
    #     # Result["result"] = ret
    #     # Result.update({"TOP": TOP})
    #     return ret
    #
    #     # def get_tax_status_all(self, obj):  # "get_" + field name
    #     #     return obj.tax_status(check_item_bought=False)
    #     # todo use this to check if name is None or not