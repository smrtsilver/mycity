
from io import BytesIO  #basic input/output operation
from PIL import Image #Imported to compress images
from django.core.files import File #to store files

def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    # im = im.resize([500,500])
    im = im.convert("RGB")
    # resize = im.resize((240, 240), Image.ANTIALIAS)
    # w, h = image.size
    #
    # image = image.resize((w / 2, h / 2), Image.ANTIALIAS)

    im.save(im_io, 'JPEG', quality=35)
    # optimize=True REDUCE SIZE AS MUCH AZ POSSIBLE
    new_image = File(im_io, name=image.name)
    return new_image


def modify_input_for_multiple_files(property_id, image):
    dict = {}
    dict['album'] = property_id.id
    dict['image'] = image
    return dict
# def send_sms(instance,method):
#     pass

# def find_by_key(data, target):
#     for k, v in data.items():
#         if k == target:
#             return True
#         elif isinstance(v, dict):
#             if find_by_key(v, target):
#                 return k
#             else:
#                 continue
#     return False
# def foreingkeylimit(id):
#
#     childs = {"city_prob": {}, "employment": {}}
#     dict = childs.copy()
#     from content.models import content
#     obj = content.objects.all()
#     for o in obj:
#         for child in childs:
#             if hasattr(o, child):
#                 dict[child].update({o.id: o})
#                 break
#             else:
#                 continue
#     # find_by_key(childs, )
#     print(childs)
#     return {"id": id}
#
