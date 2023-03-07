import urllib3 as ub
import json

ua = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    'referer' : 'https://www.bilibili.com',
    'Content-Type' : 'application/json'
}
ub.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
rq=ub.PoolManager(cert_reqs = 'CERT_NONE')
ub.disable_warnings()

while True:
    u = input('id：').strip()
    if u.isdigit() and u==str(int(u)):
        try:
            suit = 'https://api.bilibili.com/x/garb/mall/item/suit/v2?&part=suit&item_id='+u
            a = rq.request('GET' , suit , headers = ua)
            a = json.loads(a.data.decode('utf-8'))
            a = a['data']['item']
            data = {}
            data["name"] = a['name']
            data["item_id"] = eval(u)
            data["category"] = "new_items"
            data["desc"] = a["properties"]["desc"]
            data["cover"] = a["properties"]["image_cover"]
            data = json.dumps(data).encode('utf-8').decode('unicode_escape')
            print('\n'+str(data)+','+'\n')
        except Exception as e:
            print('\nError:\n'+str(e)+'\n')
    else:
        print('\n乱扣字是吧\n')
            
