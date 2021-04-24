from pyecharts.globals import SymbolType
from pyecharts.charts import WordCloud, Line, Pie, Timeline,Graph
from pyecharts import options as opts
import math

import jieba
import jieba.posseg as pseg
from tqdm import tqdm

import re
import os
import sys

os.chdir(sys.path[0])  # 重新获取路径防止出错

# 加载TXT文本
file_path = '../../hongloumeng/data/hongloumeng.txt'
txt_file = open(file_path, 'r', encoding='utf-8')
novel = txt_file.read()
txt_file.close()
# 加载name文件
name_file_path = '../../hongloumeng/data/name.txt'
name_file = open(name_file_path, 'r', encoding='utf-8')
names = name_file.read()
name_file.close()

# 消除回车影响
novel = novel.replace('\n', "  ")
names = names.replace('\n', "  ")
novel = novel.replace('\r', "")
names = names.replace('\r', "")

# 使用jieba分词
# 统计文章词频


def my_cut(list_, dict_, novel_):
    list_.extend(jieba.lcut(novel_))
    for word in list_:
        if len(word) == 1:
            # if not '\u4e00' <= word <= '\u9fa5':
            continue

        if word in dict_.keys():
            dict_[word] = dict_[word] + 1
        else:
            dict_[word] = 1


word_list = []
word_dict = {}
my_cut(word_list, word_dict, novel)

# 格式化name
names = names.split(' ')
name_list = []
same_name = {}  # 将别名配对储存
for name in names:
    if len(name) <= 1:
        continue
    name = name.split('-')
    name_list.append(name[0])
    for i in name:
        same_name[i] = name[0]


# 合并统计别名出现次数

def my_count(word_dict_, cnt_):
    for word in word_dict_:
        if word in same_name:
            cnt_[same_name[word]] += word_dict_[word]


name_cnt = dict(zip(name_list, [0]*len(name_list)))  # 统计名字出现次数，初始化为0
my_count(word_dict, name_cnt)

sorted_name_cnt = sorted(name_cnt.items(),
                         key=lambda x: x[1], reverse=True)

main_character=[]
for (word, cnt) in sorted_name_cnt[:50]:
    main_character.append(word)

print(main_character)
# 按段落分段
duanluo = re.split("  ", novel)
print("进行段落分析，共"+str(len(duanluo))+"段")
relation_dict = {}
for _ in main_character:
    relation_dict[_]={}

#建立关系字典，用tqdm可视化进度
for _ in tqdm(duanluo):
    tmp_list = []
    tmp_dict = {}
    my_cut(tmp_list, tmp_dict, _)
    ttt=[]
    for word in tmp_list:
        if word not in same_name or same_name[word] not in main_character:
            continue
        ttt.append(word)
    for word1 in ttt:
        for word2 in ttt:
            if word1==word2:
                continue

            name1=same_name[word1]
            name2=same_name[word2]
            if name2 in relation_dict[name1].keys():
                relation_dict[name1][name2] = relation_dict[name1][name2] + 1
            else:
                relation_dict[name1][name2] = 1

nodes=[]
links=[]

for (word, cnt) in sorted_name_cnt[:50]:
    nodes.append(opts.GraphNode(name=word, value=cnt, symbol_size=(int)(math.sqrt(cnt))))

for name1 in main_character:
    for name2 in main_character:
        if name1==name2:
            continue
        if name2 in relation_dict[name1].keys():
            if relation_dict[name1][name2]<=50:
                continue
            links.append(opts.GraphLink(source=name1, target=name2, value=relation_dict[name1][name2]))

c = Graph(init_opts=opts.InitOpts(width='1200px',
                                      height='800px',
                                      page_title="红楼梦关系图"))  
c.add("", 
      nodes, 
      links,
      edge_length=[10,100],
      repulsion=1000,
      )

c.set_global_opts(title_opts=opts.TitleOpts(title="红楼梦关系图"))

c.render('./output/graph.html')
