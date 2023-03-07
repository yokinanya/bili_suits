import requests
from json import dumps

ua = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    'referer' : 'https://www.bilibili.com',
    'Content-Type' : 'application/json'
}
url = 'https://api.bilibili.com/x/garb/internal/mall/suit/all'
res = requests.get(url , headers = ua)
res = res.json()
base_list = list()
for cat in res['data']['category']:
    try:
        for suit in cat['suits']:
                base_list.append({
                    'name': suit['name'],
                    'item_id': suit['item_id'],
                    'category': cat['name'],
                    'desc': suit['properties']['desc'],
                    'cover': suit['properties']['image_cover']
                })
    except TypeError:
        continue
with open('suit_list.json', 'w', encoding='utf-8') as json_file:
    json_file.write(dumps(base_list, ensure_ascii=False))
input('done')
