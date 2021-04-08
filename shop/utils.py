from content.models import tariffModel, TariffOptionsModel
from shop.serializers import tariffserializers, tabsareserializer

def tozihat(otariff,onote):
    dic={}
    posts = tariffModel.objects.filter(id__in=otariff)
    ser=tariffserializers(posts,many=True)
    notes = TariffOptionsModel.objects.filter(id__in=onote)
    sernote=tabsareserializer(notes,many=True)

    dic.update({"tariff" : [dict(i) for i in ser.data]})
    dic.update({"Note" :  [dict(i) for i in sernote.data]})
    return dic

