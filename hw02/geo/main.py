from pyecharts.globals import SymbolType
from pyecharts.charts import WordCloud, Line, Pie, Timeline, Geo
from pyecharts import options as opts

geo = (
    Geo(init_opts=opts.InitOpts(width='1200px',
                                      height='800px',
                                      page_title="中国迁都历史"))
    .add_schema(maptype="china")
    .add("",
         data_pair=[("登封", 1), ("安阳", 1), ("西安", 3), ("洛阳", 2), ("咸阳", 1),
          ("南京", 1), ("开封", 1), ("银川", 1), ("北京", 5), ("南京", 1)],
         type_="scatter"
         )
    .add("",
        [("登封", "安阳"), ("安阳", "西安"),
         ("西安", "洛阳"), ("洛阳", "咸阳"), ("咸阳", "西安"), ("西安", "洛阳"),
         ("洛阳", "南京"), ("南京", "西安"), ("西安", "开封"), ("开封", "银川"),
         ("银川", "北京")],
         type_="lines",
         effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="white"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
        # curve为正时，曲线是凸的；为负时，曲线是凹的
        color = 'purple',
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="中国迁都历史",pos_left='center'))
    .render("./output/lines.html")
)
