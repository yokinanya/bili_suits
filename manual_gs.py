from requests import get as rqGet
from os.path import exists as osPathExists
from os import makedirs as osMakedirs
from json import dumps, loads

def suitid(x):
    c = -1
    op = ''
    while x[c].isdigit():
        op+=x[c]
        c-=1
    return op[::-1]
    
def check(u):
    try:
        user = 'http://api.bilibili.com/x/web-interface/card?mid='+u
        a = rqGet(user)
        a = loads(a.text)
        name = a['data']['card']['name']
        title = '\n用户 {} 的粉丝装扮列表：'.format(name)+'\n'
        print(title)
        try:
            for i in range(1,999): 
                suits = 'https://app.bilibili.com/x/v2/space/garb/list?ps=50&vmid='+u+'&pn='+str(i)
                info = rqGet(suits)
                info = loads(info.text)
                l=info['data']['list']
                if l:
                    count=50*(i-1)+1
                    for suit in l:
                        try:
                            data = '{}.「{}」{}    装扮ID：{}'.format(count,suit['garb_title'],suit['fans_number'],suitid(suit['button']['uri']))+'\n'
                            print(data)
                            count+=1
                        except KeyError:
                            if l[i]['garb_id'] == 36398:
                                data = '{}.「舰长装扮」    装扮ID：{}'.format(count,suitid(suit['button']['uri']))+'\n'
                                print(data)
                                count+=1
                            elif l[i]['garb_id'] == 36399:
                                data = '{}.「提督装扮」    装扮ID：{}'.format(count,suitid(suit['button']['uri']))+'\n'
                                print(data)
                                count+=1
                            elif l[i]['garb_id'] == 36400:
                                data = '{}.「总督装扮」    装扮ID：{}'.format(count,suitid(suit['button']['uri']))+'\n'
                                print(data)
                                count+=1
                        except Exception as e:
                            print('Error3:\n'+str(e)+'\n')
                            return
                else:
                    break
        except Exception as e:
            print('Error2:\n'+str(e)+'\n')
            return
    except Exception as e:
        print('Error1:\n'+str(e)+'\n')
        return

def get_suit(suit_id, base_dir='./Bsuits/'):
    '''
    获取单个装扮素材

    输入:
        - suit_id: 装扮ID
        - base_dir: 存储路径
    输出: 素材文件夹
    '''
    try:
        rq_get = rqGet(
            'https://api.bilibili.com/x/garb/mall/item/suit/v2?&part=suit&item_id='
            + str(suit_id))
    except Exception as e:
        print('Error1:\n'+str(e)+'\n')
        return

    res = rq_get.json()

    # Save suit !!
    if not res['data']['item']['item_id'] == 0:
        sname = res['data']['item']['name']
        base_dir += sname
        if not osPathExists(base_dir):
            osMakedirs(base_dir)
        with open(base_dir + '/suit_info.json', 'w', encoding='utf-8') as suit_json_file:
            suit_json_file.write(rq_get.text)
        print(f'Saving suit: {sname}')
    else:
        """
        base_dir += str(suit_id)
        if not osPathExists(base_dir):
            osMakedirs(base_dir)
        with open(base_dir + '/suit_info.json', 'w', encoding='utf-8') as suit_json_file:
            suit_json_file.write(rq_get.text)
        """
        print('Fail to match any suit with this number:(')
        return

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
                emoji_file.write(rqGet(item[1]).content)
        except OSError:
            img_name = img_name.split('_')[0] + '_{}'.format(i)
            try:
                with open(base_dir + '/emoji/' + img_name + '.png', 'wb') as emoji_file:
                    emoji_file.write(rqGet(item[1]).content)
            except:
                pass
        except Exception as e:
            print('Error2:\n'+str(e)+'\n')
            return
    print('Emoji part finished')

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
                bg_file.write(rqGet(item[1]).content)
        except Exception as e:
            print('Error3:\n'+str(e)+'\n')
            return
    print('Background part finished')

    # part 3. Others
    if not osPathExists(base_dir + '/properties/'):
        osMakedirs(base_dir + '/properties/')
    try:
        pro_list = [
            ('fan_share_image.jpg',
             res['data']['item']['properties']['fan_share_image']),
            ('image_cover.jpg', res['data']['item']['properties']['image_cover']),
            ('avatar.jpg', res['data']['fan_user']['avatar'])
        ]
    except Exception as e:
        print('Error4:\n'+str(e)+'\n')
        return

    try:
        pro_list.append(
            ('comment_bg.png', res['data']['suit_items']['card_bg'][0]['properties']['image_preview_small'])
            )
    except:
        pass
    
    try:
        spro_list = res['data']['suit_items']['skin']
        for i,spro in enumerate(spro_list):
            pro_list.append(
            (f'skin_properties_{i+1}.zip', spro['properties']['package_url'])
            )
    except Exception as e:
        print('Error5:\n'+str(e)+'\n')

    try:
        pro_list.append(
            ('card_fans.png', res['data']['suit_items']['card'][0]['properties']['image_preview_small'])
            )
        pro_list.append(
            ('card.png', res['data']['suit_items']['card'][1]['properties']['image'])
            )
    except:
        pass
        
    try:
        pro_list.append(
            ('card_fans.png', res['data']['suit_items']['card'][1]['properties']['image_preview_small'])
            )
        pro_list.append(
            ('card.png', res['data']['suit_items']['card'][0]['properties']['image'])
            )
    except:
        pass

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
                pro_file.write(rqGet(item[1]).content)
        except Exception as e:
            print('Error6:\n'+str(e)+'\n')
            return
        
    print(f'The suit \"{sname}\" has been successfully saved!')

while True:
    spl = '-'*90
    opt = input(spl + "\nInput to check, or skip to download suits: ")
    if opt:
        while True:
            uid = input('\nuid: ').strip()
            if uid.isdigit() and uid==str(int(uid)):
                check(uid)
                break
            else:
                uid = input('\nuid: ').strip()
    else:
        while True:
            sid = input("\nsuit id: ").strip()
            if sid.isdigit() and sid==str(int(sid)):
                get_suit(sid)
                break
            else:
                sid = input("\nsuit id: ").strip()
