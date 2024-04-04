'''
将{version}_actions.json中的$[K1]这样的东西转写成正常的内容
'''
import re
import json
from util import get_json
from typing import Literal


def _load_single_data(version: str, category: Literal['all', 'card', 'skill', 'keyword']):
    try:
        with open(f'./data/{version}/{category}.json', '+r', encoding='utf-8')as file:
            file = json.load(file)
    except:
        file = get_json(version, category)
    return file


def fill(version: str, data_dict: dict):
    js = json.dumps(data_dict, ensure_ascii=False, indent=2)
    gcg = _load_single_data(version, 'all')
    card = _load_single_data(version, 'card')
    skill = _load_single_data(version, 'skill')
    keyword = _load_single_data(version, 'keyword')

    def _inner_fill(input: re.Match):
        input = input.group(1)
        idx = input[3:-1]
        try:
            match input[2]:
                case 'A':   # char
                    return gcg[idx]['CHS']
                case 'C':   # effect
                    return card[idx]['Name']
                case 'K':   # keyword
                    return re.sub(r'\{[^{}]*\#[^{}]*\}', '', keyword[idx]['Name'])
                case 'S':   # skill
                    return skill[idx]['Name']
        except:
            return f'[{idx}]'

    return json.loads(re.sub(r'(\$\[[^]]*\])', _inner_fill, js))
