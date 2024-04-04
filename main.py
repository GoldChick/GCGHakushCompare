'''
# 进行4.5.50版本和4.5.54版本的比对：
python main.py --old 4.5.50 --new 4.5.54
# 进行4.5版本和最新版本的比对：
python main.py --old 4.5
'''
import json
import requests
import argparse
from util import check_version
from compare import compare
from convert import action2md

if __name__ == '__main__':
    default_old = '4.5.53'
    parser = argparse.ArgumentParser(description='parser example')
    parser.add_argument('--old', default=default_old, type=str,
                        help=f'来自hakush的一个旧版本。默认为{default_old}。')
    parser.add_argument('--new', default='latest', type=str,
                        help='来自hakush的一个新版本。默认为最新。')
    parser.add_argument('--simple', default=False, type=bool,
                        help='是否生成简单的Markdown文件（方便不能预览的人阅读），默认为否。')
    args = parser.parse_args()

    old_version = args.old
    new_version = args.new
    simple = args.simple

    print(f"将进行{old_version}和{new_version}关于角色牌、行动牌和状态的比较！并且生成{'简单' if simple else '复杂'}markdown文件！")

    res = requests.get('https://api.hakush.in/v2/gi/new.json')

    if res.status_code == 200:
        info_dict = json.loads(res.text)
        if isinstance(info_dict, dict) and 'version' in info_dict.keys():
            print(f"hakush七圣召唤最新版本为{info_dict['version']}！")
            old_version = check_version(old_version, info_dict['version'])
            new_version = check_version(new_version, info_dict['version'])

            _, compare_a = compare(old_version, new_version)
            action2md(old_version, new_version, compare_a, simple)
        else:
            raise Exception('未得到正确hakush版本介绍json！请检查hakush网站是否正常！')
    else:
        raise Exception(
            '无法正常连接到hakush，可能是网站出现问题！status code:'+str(res.status_code))
