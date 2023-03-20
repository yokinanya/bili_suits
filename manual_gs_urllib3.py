import urllib3 as ub
from os.path import exists as osPathExists
from os import makedirs as osMakedirs
from json import dumps, loads

ua = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    'referer' : 'https://www.bilibili.com',
    'Content-Type' : 'application/json'
}
ub.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
rq = ub.PoolManager(cert_reqs = 'CERT_NONE')
ub.disable_warnings()

def get_suit(suit_id, base_dir='./src/'):
    '''
    获取单个装扮素材

    输入:
        - suit_id: 装扮ID
        - base_dir: 存储路径
    输出: 素材文件夹
    '''
    try:
        suit_info = 'https://api.bilibili.com/x/garb/mall/item/suit/v2?&part=suit&item_id='+ str(suit_id)
        rq_get = rq.request('GET' , suit_info , headers = ua)
    except Exception as e:
        print(e)

    res = loads(rq_get.data.decode())

    #if res['data']['item']['item_id'] == 0:
        #errors._show_error(0)
        #return dict(), 0

    base_dir += res['data']['item']['name']

    # Save suit !!
    if not osPathExists(base_dir):
        osMakedirs(base_dir)
    with open(base_dir + '/suit_info.json', 'w', encoding='utf-8') as suit_json_file:
        suit_json_file.write(str(rq_get.data.decode()))

    # part 1. Emoji
    emoji_list = [
        (item['name'][1:-1], item['properties']['image'])
        for item in res['data']['suit_items']['emoji_package'][0]['items']
    ]
    if not osPathExists(base_dir + '/emoji/'):
        osMakedirs(base_dir + '/emoji/')

    for i, item in enumerate(emoji_list):
        img_name = item[0]
        try:
            with open(base_dir + '/emoji/' + img_name + '.png',
                      'wb') as emoji_file:
                emoji_file.write(rq.request('GET' , item[1]).data)
        except OSError:
            img_name = img_name.split('_')[0] + '_{}'.format(i)
            try:
                with open(base_dir + '/emoji/' + img_name + '.png', 'wb') as emoji_file:
                    emoji_file.write(rq.request('GET' , item[1]).data)
            except:
                pass
        except Exception as e:
            print(e)

    # part 2. Background
    bg_dict = res['data']['suit_items']['space_bg'][0]['properties']
    bg_list = list()

    for key, value in bg_dict.items():
        if key[0] == 'i':
            bg_list.append((key, value))

    if not osPathExists(base_dir + '/background/'):
        osMakedirs(base_dir + '/background/')

    for item in bg_list:
        try:
            with open(base_dir + '/background/' + item[0] + '.jpg',
                      'wb') as bg_file:
                bg_file.write(rq.request('GET' , item[1]).data)
        except Exception as e:
            print(e)

    # part 3. Others
    if not osPathExists(base_dir + '/properties/'):
        osMakedirs(base_dir + '/properties/')
    try:
        pro_list = [
            ('skin_properties.zip',
             res['data']['suit_items']['skin'][0]['properties']['package_url']),
            ('fan_share_image.jpg',
             res['data']['item']['properties']['fan_share_image']),
            ('image_cover.jpg', res['data']['item']['properties']['image_cover']),
            ('avatar.jpg', res['data']['fan_user']['avatar'])
        ]
    except Exception as e:
        print(str(e))

    try:
        pro_list.append(
            ('card_bg.png', res['data']['suit_items']['card_bg'][0]['properties']['image_preview_small'])
            )
    except:
        pass

    try:
        pro_list.append(
            ('card.png', res['data']['suit_items']['card'][0]['properties']['image'])
            )
    except:
        pass
    
    try:
        pro_list.append(
            ('fans_card.png', res['data']['suit_items']['card'][1]['properties']['image_preview_small'])
            )
    except:
        pro_list.append(
            ('fans_card.png', res['data']['suit_items']['card'][1]['properties']['image'])
            )

    try:
        pro_list.append(
            ('thumbup.png',res['data']['suit_items']['thumbup'][0]['properties']['image_preview'])
            )
    except:
        pass
    
    try:
        pro_list.append(
            ('loading.webp', res['data']['suit_items']['loading'][0]['properties']['loading_url'])
            )
    except:
        pass
    
    try:
        pro_list.append(
            ('loading_preview.png', res['data']['suit_items']['loading'][0]['properties']['image_preview_small'])
            )
    except:
        pass
    
    try:
        pro_list.append(
            ('pendant.png', res['data']['suit_items']['pendant'][0]['properties']['image'])
            )
    except:
        pass
    
    try:
        pro_list.append(
            ('play_icon.png', res['data']['suit_items']['play_icon'][0]['properties']['static_icon_image'])
            )
    except:
        pass

    try:
        pro_list.append(
            ('play_icon_left.png', res['data']['suit_items']['play_icon'][0]['properties']['drag_left_png'])
            )
    except:
        pass

    try:
        pro_list.append(
            ('play_icon_right.png', res['data']['suit_items']['play_icon'][0]['properties']['drag_right_png'])
            )
    except:
        pass
    
    for item in pro_list:
        try:
            with open(base_dir + '/properties/' + item[0], 'wb') as pro_file:
                pro_file.write(rq.request('GET' , item[1]).data)
        except Exception as e:
            print(e)

    return res
while True:
    sid = eval(input("sid: ").strip())
    get_suit(sid)
