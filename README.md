#  GCG Hakush Compare Script
调取hakush的api进行比对，生成json文件和md文件
## 运行
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