#  GCG Hakush Compare Script
调取hakush.in的api进行比对，生成json文件和md文件  
调用玉衡杯数据库的api进行技能数值的比对（hakush并不频繁更新测试服数值）  
  
将来可能会更多的使用玉衡杯数据库，速度会更快一些（很远的将来！）
## github action
fork之后，在github action进行run workflow  
输入旧版本（如4.5 | 4.5.54）、新版本（不输默认为最新版本latest）,等待后即可下载包含比对文件的压缩包  
压缩包中包含:
- hakush-行动牌比对json
- hakush-行动牌比对markdown
- hakush-角色牌比对(不含技能数值)json
- hakush(old)-玉衡杯数据库-角色技能比对(可能含有技能数值)json

可以打开网站观察目前的最新版本，再决定是否运行   

链接：
[hakush.in](https://gi16.hakush.in/gcg)
[玉衡杯数据库](https://homdgcat.wiki/gi/gcg?lang=CH)
## 本地运行
入口见于main.py，直接运行或者附加参数运行即可（由于时常的更新，推荐至少指定old版本）  
  
[data文件夹](./data/)内存储从hakush下载的json文件  
[detail文件夹](./detail/)内生成经过初步整合的json文件  
[compare文件夹](./compare/)内生成两个版本比对的json文件  
[md文件夹](./md/)内生成两个版本比对的markdown文件

你可能需要一个能阅读markdown文件的编辑器？如果真的没有（为什么没有），可以考虑把simple参数设置为true。  
当然，这种情况下（实际上更多合理的情况下）你应该去阅读json
```
# 进行4.5.50版本和4.5.54版本的比对，同时生成简单的markdown文件：
python main.py --old 4.5.50 --new 4.5.54 --simple true
# 进行4.5版本和最新版本的比对：
python main.py --old 4.5
```
注：由于hakush添加七圣召唤内容比较晚，比较早的七圣内容（4.4及以前）未被收录
## 依赖
因为使用了某些较新语法，推荐使用**python3.11**及以上版本

### requirements:
- requests # 向hakush网站发起请求 
- tqdm # 可视化进度条

```
pip install requests tqdm
```
## 作者
Github: [Gold_Chick](https://github.com/GoldChick)  
Bilibili: [Fried--Chicken](https://space.bilibili.com/442588088)  
原神: <font color=gree>爱打牌的小团雀吖</font> 