'''
从玉衡杯获取角色技能数据
'''
import json
import requests
import re


def get_json() -> dict:
    '''
    version: 比如 '4.5.50'这样的
    '''

    res = requests.get('https://homdgcat.wiki/gi/CH/gcg_2.js')
    res.encoding = 'utf-8'

    new_skills = {}
    if res.status_code == 200:
        skills = re.match(r'.+var _skills = (.+)var _ref', res.text, re.DOTALL)[1]
        skills = json.loads(skills)
        assert (isinstance(skills, dict))

        for k, v in skills.items():
            desc = re.sub(r"<color style='color:#[A-F0-9;]+'>", '', v['Desc'])
            desc = re.sub(r"<[a-z/A-Z]+>", '', desc)
            desc = re.sub(r"\[b\]\d+\[a\]", '', desc)
            desc = re.sub(" ", '', desc)
            new_skills[k] = {
                'Name': v['Name'],
                'Desc':  desc
            }

        with open('./keqing_skills.json', '+w', encoding='utf-8')as f:
            f.write(json.dumps(new_skills, indent=2, ensure_ascii=False))

    else:
        print('未成功连接到玉衡杯网站！')

    return new_skills


def compare_skill(old_version: str):
    '''
    old to latest
    '''
    keqing_skill = get_json()
    with open(f'./detail/{old_version}/skill.json', '+r', encoding='utf-8') as f:
        skill = json.load(f)
        assert (isinstance(skill, dict))

    diffs = {}

    for k in skill.keys() & keqing_skill.keys():
        if skill[k]['Desc'] != keqing_skill[k]['Desc']:
            diffs[k] = {
                "Name": {
                    "old": skill[k]['Name'],
                    "new": re.sub(' ', '', keqing_skill[k]['Name'])
                },
                "Desc": {
                    "old": skill[k]['Desc'],
                    "new": keqing_skill[k]['Desc']
                }
            }
    with open('./keqing_diffs.json', '+w', encoding='utf-8')as f:
        f.write(json.dumps(diffs, ensure_ascii=False, indent=2))
