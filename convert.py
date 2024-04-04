'''
将比较后的dict，转化为md格式保存在./md/中
'''
import os
import re
import json
from difflib import SequenceMatcher


def _get_str_diff(old: str, new: str, simple=False):
    matcher = SequenceMatcher(None, old, new)
    diff = ""
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'replace':
            diff += f"{old[i1:i2]}->{new[j1:j2]}" if simple else f"<del><font color=red>{old[i1:i2]}</font></del>-><font color=green>{new[j1:j2]}</font>"
        elif op == 'delete':
            diff += f"[{old[i1:i2]}]->[NONE]" if simple else f"<del><font color=red>{old[i1:i2]}</font></del>"
        elif op == 'insert':
            diff += f"[{new[j1:j2]}]" if simple else f"<font color=green>{new[j1:j2]}</font>"
        else:
            diff += f"{old[i1:i2]}"
    return diff


def action2md(old_version: str, new_version: str, compare_dict: dict, simple=False):
    old_items = {}
    new_items = {}

    for obj in compare_dict.values():
        new_key = 'tmp'
        new_obj = {}
        assert (isinstance(obj, dict))

        old_flag = True
        if 'new' in obj.keys():
            old_flag = False
            obj = obj['new']

        for k, v in obj.items():
            if k == 'Name':
                if isinstance(v, str):
                    new_key = f"## {obj[k]}"
                elif simple:
                    new_key = f'## {obj[k]["old"]}->{obj[k]["new"]}'
                else:
                    new_key = f'## ~~<font color=red>{obj[k]["old"]}~~-><font color=green>{obj[k]["new"]}</font>'
            else:
                if isinstance(v, str):
                    new_obj[k] = obj[k]
                else:
                    new_obj[k] = _get_str_diff(
                        obj[k]['old'], obj[k]['new'], simple)
        if old_flag:
            old_items[new_key] = new_obj
        else:
            new_items[new_key] = new_obj

    def inner_write(name: str, obj: dict, md):
        md.write(name+'\n')
        for k, v in obj.items():
            match k:
                case 'Desc':
                    k = '描述'
                case 'Cost':
                    k = '费用'
            if not simple:
                k = f"<font color=cyan>{k}</font>"
            v = re.sub(r'\\n', '  \n', v)
            md.write(f"{k} : {v}  \n  \n")

    if not os.path.exists('./md'):
        os.mkdir('./md')
    with open(f"./md/{old_version}_{new_version}_actions_compare.md", '+w', encoding='utf-8')as md:
        md.write('# <font color=#FF00FF>OLD</font>\n')
        for name, obj in old_items.items():
            inner_write(name, obj, md)

        md.write('# <font color=#FF00FF>NEW</font>\n')
        for name, obj in new_items.items():
            inner_write(name, obj, md)


# 没有投入使用，但是其实是可以用的
def _load2md(old_version: str, new_version: str):
    with open(f"./compare/{old_version}_{new_version}_actions_compare.json", '+r', encoding='utf-8')as actions:
        actions = json.load(actions)
        action2md(old_version, new_version, actions)


# load2md('4.5', '4.5.54')
