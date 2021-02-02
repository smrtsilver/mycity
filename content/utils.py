#
#
#
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
