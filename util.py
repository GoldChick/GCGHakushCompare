import os
import re
import json
import requests
from tqdm import tqdm
from typing import Literal


def get_json(version: str, category: Literal['all', 'card', 'skill', 'keyword',  '1101'] = "all") -> dict:
    '''
    version: 比如 '4.5.50'这样的
    '''
    save = True
    match category:
        case 'all':
            url = 'https://api.hakush.in/v2/gi/data/gcg.json'
        case category if category in ['card', 'skill', 'keyword']:
            url = f'https://api.hakush.in/v2/gi/data/zh/gcg/{category}.json'
        case _:
            save = False
            url = f'https://api.hakush.in/v2/gi/data/zh/gcg/{category}.json'

    res = requests.get(url.replace('data', version))
    res.encoding = 'utf-8'

    if res.status_code == 200:
        res_dict = json.loads(
            re.sub(r'</*color=*#*[a-z0-9A-Z]*>', '', res.text))

        if isinstance(res_dict, dict):
            if save:
                if not os.path.exists('./data'):
                    os.mkdir('./data')
                if not os.path.exists(f'./data/{version}'):
                    os.mkdir(f'./data/{version}')
                with open(f"./data/{version}/{category}.json", '+w', encoding='utf-8')as f:
                    f.write(json.dumps(res_dict, indent=2, ensure_ascii=False))
                    print(f"成功保存{version}版本的{category}信息！")
            return res_dict
        else:
            raise Exception('未得到正确的json！请检查hakush网站上是否已经上传了指定版本' +
                            str(version)+'的json！')
    else:
        raise Exception(
            '无法正常连接到hakush并获得'+category+'，可能是网站或输入出现问题！status code:'+str(res.status_code))


def _skill_category_process(skill: str) -> str:
    match skill.split('_')[-1]:
        case 'A':
            return '普通攻击'
        case 'E':
            return '元素战技'
        case 'Q':
            return '元素爆发'
        case 'PASSIVE':
            return '被动技能'


def _element_process(element: str, default='物理') -> str:
    match element.split('_')[-1]:
        case 'CRYO':
            return '冰元素'
        case 'HYDRO':
            return '水元素'
        case 'PYRO':
            return '火元素'
        case 'ELECTRO':
            return '雷元素'
        case 'GEO':
            return '岩元素'
        case 'DENDRO':
            return '草元素'
        case 'ANEMO':
            return '风元素'
        case 'ENERGY':
            return '冲'
        case 'LEGEND':
            return '秘'
        case 'PAIMON':
            return '白'
        case 'SAME':
            return '白'
        case 'VOID':
            return default
        case _:
            return default


def _d_key_process(d_key: str, d_value) -> str:
    match d_key:
        case 'D__KEY__DAMAGE':
            return str(d_value)
        case "D__KEY__ELEMENT":
            return _element_process(d_value)+'伤害'
        case _:
            if isinstance(d_value, dict):
                return f"[{d_value['Name']}]"
            return str(d_value)


def _skill_loader(skill: dict):
    assert (isinstance(skill['Desc'], str))

    for pattern in re.findall(r'\$\[([^]]*)\]', skill['Desc']):
        children = skill['Child']
        assert (isinstance(children, dict))
        if pattern in children.keys():
            skill['Desc'] = skill['Desc'].replace(
                f'$[{pattern}]', _d_key_process(pattern, children[pattern]))
    skill.pop('Child')

    skill['Desc'] = re.sub(r'\{[^}]*\}', '', skill['Desc'])
    if 'Cost' in skill.keys():
        skill['Cost'] = '+'.join(
            [f"{v}{_element_process(k,'黑')[0]}" for k, v in skill['Cost'].items()])
        skill['Tag'] = _skill_category_process(
            skill['Tag']) if 'Tag' in skill.keys() else '无'
    return skill


def _get_all_cards(version: str):
    if not os.path.exists('./detail'):
        os.mkdir('./detail')
    if not os.path.exists(f'./detail/{version}'):
        os.mkdir(f'./detail/{version}')

    characters = {}
    # 这里的cards除了角色牌、行动牌还有状态
    cards = get_json(version, 'card')

    js = get_json(version)
    for key in tqdm(list(filter(lambda k: len(k) == 4, js.keys())), desc=f"正在获取{version}所有角色牌中……", unit='item'):
        card = get_json(version, key)
        char = {}
        char['Name'] = card['Title']
        char['Desc'] = card['Desc']
        char['Tags'] = '+'.join(card['Tag'])
        char['HP+MP'] = f"{card['Hp']}血{card['Cost']}充"
        char['Skills'] = {k: _skill_loader(
            v) for k, v in card['Talent'].items()}
        characters[key] = char

    with open(f"./detail/{version}/characters.json", '+w', encoding='utf-8')as compare:
        compare.write(json.dumps(characters, ensure_ascii=False, indent=2))
        print(f'{version}版本characters信息保存成功！')

    actions = {}
    for key in tqdm(cards.keys(), desc=f"正在获取{version}所有行动牌和状态中……", unit='item'):
        simple_card = {
            'Name': cards[key]['Name'],
            'Desc': re.sub(r'\{[^}]*\}', '', cards[key]['Desc'])
        }
        if key in js.keys():
            if 'tag' in js[key].keys():
                simple_card['Tags'] = '+'.join(js[key]['tag'])
            simple_card['Cost'] = '+'.join([f"{cost['count']}{_element_process(cost['costType'],'黑')}" for cost in list(
                filter(lambda dic: 'count' in dic.keys(), js[key]['cost']))])
        actions[key] = simple_card

    with open(f"./detail/{version}/actions.json", '+w', encoding='utf-8')as compare:
        compare.write(json.dumps(actions, ensure_ascii=False, indent=2))
        print(f'{version}版本actions信息保存成功！')

    return characters, actions


def load_all_cards(version: str):
    if os.path.exists(f'./detail/{version}/characters.json') and os.path.exists(f"./detail/{version}/actions.json"):
        with open(f'./detail/{version}/characters.json', '+r', encoding='utf-8')as chars:
            chars = json.load(chars)
        with open(f"./detail/{version}/actions.json", '+r', encoding='utf-8')as actions:
            actions = json.load(actions)
        return chars, actions
    else:
        print(f'指定路径尚不存在{version}版本的角色牌或行动牌信息！改为自动获取全部并保存！')
        return _get_all_cards(version)


def check_version(version: str, default: str):
    if version == 'latest':
        return default
    if re.match(r'\d\.\d\.\d\d$', version) or re.match(r'\d\.\d$', version):
        return version
    raise Exception(f'版本{version}格式错误！请尝试输入正确的版本号！例：4.4.53|4.5')
