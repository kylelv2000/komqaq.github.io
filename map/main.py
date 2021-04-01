from pyecharts.globals import SymbolType
from pyecharts.charts import WordCloud, Line, Pie, Timeline, Geo, Map
from pyecharts import options as opts

# 2020年全国人口数据
data = {
    "广东": 108.98,
    "山东": 102.33,
    "河南": 102.05,
    "四川": 103.13,
    "江苏": 101.52,
    "河北": 102.84,
    "湖南": 105.80,
    "安徽": 103.39,
    "湖北": 105.55,
    "浙江": 105.69,
    "广西": 108.26,
    "云南": 107.90,
    "江西": 106.67,
    "辽宁": 102.54,
    "福建": 105.96,
    "陕西": 106.92,
    "黑龙江": 102.85,
    "山西": 105.56,
    "贵州": 106.31,
    "重庆": 102.61,
    "吉林": 102.67,
    "甘肃": 104.42,
    "内蒙古": 108.17,
    "新疆": 106.87,
    "上海": 106.19,
    "北京": 106.75,
    "天津": 114.52,
    "海南": 112.58,
    "宁夏": 104.99,
    "青海": 107.40,
    "西藏": 105.70
}


map_data = list(data.items())

c = (
    Map(init_opts=opts.InitOpts(width='1200px',
        height='800px',
        page_title="第6次人口普查男女比例统计（不计港澳台）"))
    .add("第6次人口普查男女比例统计（不计港澳台）",
         data_pair=map_data,
         maptype="china",
         is_map_symbol_show=False,  # 不描点
         )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="第6次人口普查男女比例统计（不计港澳台）",pos_left='center', pos_top='10%'),
        visualmap_opts=opts.VisualMapOpts(
            min_=100, max_=115, is_piecewise=True),
    )
)

c.render('./map/output/maps.html')
