from pyecharts.globals import SymbolType
from pyecharts.charts import Bar, Line, Pie, Timeline, Geo, Page, Map
from pyecharts import options as opts

data = [
    ["北京", 2.63, 2.66, 3.76, 4.12, 3.01, 4.83, 4.41, 4.74, 4.02],
    ["天津", 1.43, 1.25, 2.60, 1.83, 0.23, 2.14, 2.28, 2.63, 2.50],
    ["河北", 4.71, 4.88, 6.60, 6.06, 5.56, 6.95, 6.17, 6.47, 6.50],
    ["山西", 3.27, 4.31, 5.61, 4.77, 4.42, 4.99, 5.24, 4.87, 4.86],
    ["内蒙古", 2.57, 2.40, 3.73, 3.34, 2.40, 3.56, 3.36, 3.65, 3.51],
    ["辽宁", -0.80, -1.00, -0.44, -0.18, -0.42, 0.26, -0.03, -0.39, -0.34],
    ["吉林", -0.85, 0.36, 0.26, -0.05, 0.34, 0.40, 0.32, 0.36, 1.02],
    ["黑龙江", -1.01, -0.69, -0.41, -0.49, -0.60, 0.91, 0.78, 1.27, 1.07],
    ["上海", 1.50, 1.80, 2.80, 4.00, 2.45, 3.14, 2.94, 4.20, 1.87],
    ["江苏", 2.08, 2.29, 2.68, 2.73, 2.02, 2.43, 2.43, 2.45, 2.61],
    ["浙江", 4.99, 5.44, 6.36, 5.70, 5.02, 5.00, 4.56, 4.60, 4.07],
    ["安徽", 5.99, 6.45, 8.17, 7.06, 6.98, 6.97, 6.82, 6.86, 6.32],
    ["福建", 6.80, 7.00, 8.80, 8.30, 7.80, 7.50, 6.19, 7.01, 6.21],
    ["江西", 6.56, 7.37, 7.71, 7.29, 6.96, 6.98, 6.91, 7.32, 7.50],
    ["山东", 4.27, 6.08, 10.14, 10.84, 5.88, 7.39, 5.01, 4.95, 5.10],
    ["河南", 4.18, 4.92, 5.98, 6.15, 5.65, 5.78, 5.51, 5.16, 4.94],
    ["湖北", 4.27, 4.54, 5.59, 5.07, 4.91, 4.90, 4.93, 4.88, 4.38],
    ["湖南", 3.11, 5.11, 6.19, 6.56, 6.72, 6.63, 6.54, 6.57, 6.55],
    ["广东", 8.08, 8.24, 9.16, 7.44, 6.80, 6.10, 6.02, 6.95, 6.10],
    ["广西", 7.17, 8.16, 8.92, 7.87, 7.90, 7.86, 7.93, 7.89, 7.67],
    ["海南", 6.76, 8.47, 8.72, 8.57, 8.57, 8.61, 8.69, 8.85, 8.97],
    ["重庆", 2.91, 3.48, 3.91, 4.53, 3.86, 3.62, 3.60, 4.00, 3.17],
    ["四川", 3.61, 4.04, 4.23, 3.49, 3.36, 3.20, 3.00, 2.97, 2.98],
    ["贵州", 6.70, 7.05, 7.10, 6.50, 5.80, 5.80, 5.90, 6.31, 6.38],
    ["云南", 6.43, 6.87, 6.85, 6.61, 6.40, 6.20, 6.17, 6.22, 6.35],
    ["西藏", 10.14, 10.64, 11.05, 10.68, 10.65, 10.55, 10.38, 10.27, 10.26],
    ["陕西", 4.27, 4.43, 4.87, 4.41, 3.82, 3.87, 3.86, 3.88, 3.69],
    ["甘肃", 3.85, 4.42, 6.02, 6.00, 6.21, 6.10, 6.08, 6.06, 6.05],
    ["青海", 7.58, 8.06, 8.25, 8.52, 8.55, 8.49, 8.03, 8.24, 8.31],
    ["宁夏", 8.03, 7.78, 8.69, 8.97, 8.04, 8.57, 8.62, 8.93, 8.97],
    ["新疆", 3.69, 6.13, 11.40, 11.08, 11.08, 11.47, 10.92, 10.84, 10.57]
]

tl = Timeline(init_opts=opts.InitOpts(width='1200px',
                                      height='800px',
                                      page_title="近十年各省人口自然增长率"))

for i in range(9):
    mp = (
        Map().add("增长率",
                  data_pair=[(dt[0], dt[i+1]) for dt in data],
                  maptype="china",
                  is_map_symbol_show=False,
                  is_roam=False
                  )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="{}年各省人口自然增长率".format(2019-i),
                                      pos_left='center', pos_top='10%'),
            visualmap_opts=opts.VisualMapOpts(
                min_=-2, max_=12, is_piecewise=True),
        )
    )
    tl.add(mp, "{}年".format(2019-i))

# tl.render('./charts/output/pages.html')


china_data = [3.34, 3.81, 5.32, 5.86, 4.96, 5.21, 4.92, 4.95, 4.79]

line = (Line(init_opts=opts.InitOpts(width='1200px',
                                     height='700px',
                                     page_title="近十年人口自然增长率"))
        .add_xaxis(["{}年".format(2019-i) for i in range(9)])
        .add_yaxis("",
                   y_axis=china_data,
                   is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="近十年人口自然增长率",
                                                   pos_left='center', pos_top='5%')
                         )
        )


t2 = Timeline(init_opts=opts.InitOpts(width='1200px',
                                      height='800px',
                                      page_title="近十年各省人口自然增长率"))


def takeSecond(elem):
    return elem[1]


for i in range(9):
    tmp = [(dt[0], dt[i+1]) for dt in data]
    tmp.sort(key=takeSecond, reverse=True)
    bar = (
        Bar()
        .add_xaxis([x[0] for x in tmp])
        .add_yaxis("",
                   [x[1] for x in tmp],
                   )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="{}年各省人口自然增长率".format(2019-i),
                                      pos_left='center', pos_top='10%'),
            visualmap_opts=opts.VisualMapOpts(
                min_=-2, max_=12, is_piecewise=True),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts={"rotate":45}
                #splitline_opts=opts.SplitLineOpts(is_show=True)
            )
        )
    )
    t2.add(bar, "{}年".format(2019-i))


pages = Page(page_title="人口自然增长率", layout=Page.SimplePageLayout)
pages.add(line, tl, t2)
pages.render("./charts/output/pages.html")
