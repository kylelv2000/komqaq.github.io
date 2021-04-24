from pyecharts.globals import SymbolType
from pyecharts.charts import WordCloud, Line, Pie, Timeline
from pyecharts import options as opts


import jieba
import jieba.posseg as pseg

import re
import os
import sys

os.chdir(sys.path[0])  # 重新获取路径防止出错

# 加载TXT文本
file_path = './data/hongloumeng.txt'
txt_file = open(file_path, 'r', encoding='utf-8')
novel = txt_file.read()
txt_file.close()
# 加载name文件
name_file_path = './data/name.txt'
name_file = open(name_file_path, 'r', encoding='utf-8')
names = name_file.read()
name_file.close()

# 消除回车影响
novel = novel.replace('\n', ' ')
names = names.replace('\n', ' ')
novel = novel.replace('\r', ' ')
names = names.replace('\r', ' ')

# 按章节分段
zhangjie = re.split("(第\w+回\s)", novel)
new_novel = []
for i in range(len(zhangjie)):
    if re.search("(第\w+回\s)", zhangjie[i]):
        new_novel.append(zhangjie[i]+zhangjie[i+1])

print("分段完成，共分成%d段" % len(new_novel))

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

# 根据value（即出现次数）从大到小排序
sorted_word_dict = sorted(word_dict.items(),
                          key=lambda x: x[1], reverse=True)

# 输出总词频前50
out_file = open('./output/总词频.csv', 'w')
out_file.write('词组,出现次数\n')
for (word, cnt) in sorted_word_dict[:50]:
    out_file.write(word+','+str(cnt)+'\n')
print("输出总词频前50完成")
out_file.close()

# 重新按照章节分词
new_word_list = []
new_word_dict = []
for chapter in new_novel:
    tmp_list = []
    tmp_dict = {}
    my_cut(tmp_list, tmp_dict, chapter)
    new_word_list.append(tmp_list)
    new_word_dict.append(tmp_dict)

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

# 输出人名总出现次数前50
out_file = open('./output/总人物词频.csv', 'w')
out_file.write('人名,出现次数\n')
for (word, cnt) in sorted_name_cnt[:50]:
    out_file.write(word+','+str(cnt)+'\n')
print("输出总人物词频前50完成")
out_file.close()

new_name_cnt = []
sorted_new_name_cnt = []
# 分章节统计人物出现次数
for i in range(len(new_novel)):
    tmp = dict(zip(name_list, [0]*len(name_list)))
    my_count(new_word_dict[i], tmp)
    new_tmp = {}
    for k in tmp.keys():  # 删除0元素
        if tmp[k] > 0:
            new_tmp[k] = tmp[k]
    new_name_cnt.append(new_tmp)
    sorted_new_name_cnt.append(sorted(new_tmp.items(),
                                      key=lambda x: x[1], reverse=True))


# 分章节输出前10人名
out_file = open('./output/分章节人物词频.csv', 'w')

sout = ''
for i in range(len(new_novel)):
    sout += ",第%d回" % (i+1)
sout += '\n'
out_file.write(sout)

out_list = []
for tmp in sorted_new_name_cnt:
    out_list.append(tmp[:10])
for i in range(10):
    sout = str(i+1)
    for tmp in out_list:
        sout += ','+'\"'+str(tmp[i])+'\"'
    sout += '\n'
    out_file.write(sout)
print("输出分章节人物词频前10完成")
out_file.close()


# 分析主要人物各章节出现次数
main_character = ['贾宝玉', '林黛玉', '薛宝钗', '贾母', '王熙凤', '王夫人', '史湘云', '袭人']
main_character_cnt = []
for _ in range(len(new_novel)):
    main_character_cnt.append(
        dict(zip(main_character, [0]*len(main_character))))

for i in range(len(new_novel)):
    tmp = new_name_cnt[i]
    for name in main_character:
        if same_name[name] in tmp.keys():
            main_character_cnt[i][name] += tmp[same_name[name]]

# 输出主要人物各章节出现次数
out_file = open('./output/主要人物词频.csv', 'w')
sout = ''
for i in range(len(new_novel)):
    sout += ",第%d回" % (i+1)
sout += '\n'
out_file.write(sout)
for name in main_character:
    sout = name
    for tmp in main_character_cnt:
        sout += ','+str(tmp[name])
    sout += '\n'
    out_file.write(sout)
print("输出主要人物各章节出现次数完成")
out_file.close()


# 将词云图片导出到当前文件夹
c = (
    WordCloud(init_opts=opts.InitOpts(width='900px', height='900px',
                                      page_title="红楼梦总词频词云"))
    .add(series_name="红楼梦总词频词云",
         data_pair=sorted_word_dict[:600],
         word_size_range=[10, 60],
         width="100%",
         shape="circle",
         word_gap=3
         )
    .set_global_opts(title_opts=opts.TitleOpts(title="红楼梦总词频词云",
                                               pos_left='center'))
    .render("./output/words.html")
)
c = (
    WordCloud(init_opts=opts.InitOpts(width='900px', height='900px',
                                      page_title="红楼梦人物词云"))
    .add(series_name="红楼梦人物词云",
         data_pair=sorted_name_cnt,
         width="100%",
         height="100%",
         word_gap=3,
         mask_image='./qaz.jpeg'
         )
    .set_global_opts(title_opts=opts.TitleOpts(title="红楼梦人物词云",
                                               pos_left='center'))
    .render("./output/names.html")
)

line = (Line(init_opts=opts.InitOpts(width='1600px',
                                     height='800px',
                                     page_title="主要人物各章节出现次数"))
        .add_xaxis(["第%d回" % (i+1) for i in range(len(new_novel))]))
for ch in main_character:
    line.add_yaxis(ch,is_symbol_show=False,is_selected=(ch=='贾宝玉' or ch=='林黛玉' or ch=='薛宝钗'),
                   y_axis=[main_character_cnt[i][ch] for i in range(len(new_novel))],
                   is_smooth=True, label_opts=opts.LabelOpts(is_show=False),)
line.set_global_opts(title_opts=opts.TitleOpts(title="主要人物各章节出现次数",
                                               pos_left='center', pos_top='10%'),
                     tooltip_opts=opts.TooltipOpts(trigger="axis"),
                     datazoom_opts=opts.DataZoomOpts(range_start=0,
                                                     range_end=20),
                     )

line.render("./output/line1.html")

tl = Timeline(init_opts=opts.InitOpts(width='900px',
                                      height='600px',
                                      page_title="每回合人物词频"))
for i in range(len(new_novel)):
    pie = (
        Pie().add("",
                  data_pair=sorted_new_name_cnt[i][:10],
                  rosetype="radius",
                  radius=["30%", "55%"],
                  )
        .set_global_opts(title_opts=opts.TitleOpts("第{}回前10人物词频".format(i+1),
                         pos_left='center', pos_top='10%'))
    )
    tl.add(pie, "第{}回".format(i))
tl.render("./output/timeline_pie.html")

