import copy
import json

with open(r'C:\Users\Nusa\Desktop\weddinglist\weddinglist\api\custom_json\products.json') as dataf, \
        open(r'C:\Users\Nusa\Desktop\weddinglist\weddinglist\api\fixtures\output.json', 'w') as out:
    data = json.load(dataf)
    newdata = []
    for i, block in enumerate(data):
        new = dict(model="api.Gift", pk=block['id'])
        new['fields'] = dict(name=block['name'],
                             brand=block['brand'],
                             price=block['price'][:-3],
                             stock=block['in_stock_quantity'])
        newdata.append(copy.deepcopy(new))
    json.dump(newdata, out, indent=2)
