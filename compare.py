'''
从./detail/文件夹内，比较本地储存的json文件，保存在./compare/中
如果本地没有储存json文件，将会从hakush网站上收集
'''
import os
import json
from util import load_all_cards
from fill import fill


def _inner_compare(old: dict, new: dict):
    compare_dict = {}
    if old != new:

        old_keys = old.keys()
        new_keys = new.keys()

        compare_dict = {}
        for k in old_keys & new_keys:
            if new[k] != old[k]:
                if isinstance(old[k], dict):
                    compare_dict[k] = _inner_compare(
                        old[k], new[k])
                else:
                    compare_dict[k] = {
                        'old':   old[k],
                        'new':   new[k]
                    }
            elif k in ['Name']:
                compare_dict[k] = new[k]

        for k in (old_keys ^ new_keys) & new_keys:
            compare_dict[k] = {
                'old':  'none',
                'new':   new[k]
            }

    return compare_dict


def compare(old_version: str, new_version: str, another_save_with_no_version=False):
    old_c, old_a = load_all_cards(old_version)
    old_a = fill(old_version, old_a)

    new_c, new_a = load_all_cards(new_version)
    new_a = fill(new_version, new_a)

    if not os.path.exists('./compare'):
        os.mkdir('./compare')

    compare_c = _inner_compare(old_c, new_c)
    with open('./compare/'+old_version+'_'+new_version+'_characters_compare.json', '+w', encoding='utf-8')as compare:
        compare.write(json.dumps(compare_c, ensure_ascii=False, indent=2))
        print(f'已成功生成{old_version}和{new_version}角色牌信息比对的文件！')

    compare_a = _inner_compare(old_a, new_a)
    with open(f"./compare/{old_version}_{new_version}_actions_compare.json", '+w', encoding='utf-8')as compare:
        compare.write(json.dumps(compare_a, ensure_ascii=False, indent=2))
        print(f"已成功生成{old_version}和{new_version}行动牌、状态信息比对的文件！")

    if another_save_with_no_version:
        with open('./characters_compare.json', '+w', encoding='utf-8')as compare:
            compare.write(json.dumps(compare_c, ensure_ascii=False, indent=2))
        with open(f"./actions_compare.json", '+w', encoding='utf-8')as compare:
            compare.write(json.dumps(compare_a, ensure_ascii=False, indent=2))

    return compare_c, compare_a
