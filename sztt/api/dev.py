# import jieba
# from jieba.analyse import extract_tags
# # from api.libs import odict
# from collections import OrderedDict

# jieba.setLogLevel(20)


# class odict(OrderedDict):
#     def __init__(self, *args, **kwargs):
#         super(OrderedDict, self).__init__(*args, **kwargs)

#     def __getitem__(self, k):
#         if not isinstance(k, slice):
#             return OrderedDict.__getitem__(self, k)
#         x = odict()
#         for idx, key in enumerate(self.keys()):
#             if k.start <= idx < k.stop:
#                 x[key] = self[key]
#         return x


# def keyword_extraction(_str, limit=0):
#     od = odict()
#     for keyword, weight in extract_tags(_str, withWeight=True):
#         od[keyword] = weight
#     return od if limit == 0 else od[0:limit]


# print(keyword_extraction("习近平：推动我国生态文明建设迈上新台阶", limit=2))


from collections import OrderedDict


class odict(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(OrderedDict, self).__init__(*args, **kwargs)

    def __getitem__(self, k):
        print(k)
        print(k.start)
        print(k.stop)
        print(k.step)
        ndict = odict()
        for index, key in enumerate(self.keys()):
            print(index, key)
            


od = odict()
od['2'] = 1
od[1:2:3]
