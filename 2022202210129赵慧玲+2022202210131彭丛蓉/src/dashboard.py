import streamlit as st
from matplotlib import pyplot as plt

import config, dataset, main

# Matplotlib params
plt.style.use("seaborn")
plt.rcParams["figure.dpi"] = 300

# 标题
st.set_page_config(
    page_title="3D Bin Packing",
)
st.header("3D Bin Packing")

# 数据集部分
st.header("数据集")
select_dataset = st.selectbox(
    "选择你想测试的数据集",
    ("E1-1", "E1-2", "E1-3", "E1-4", "E1-5",
     "E2-1", "E2-2", "E2-3", "E2-4", "E2-5",
     "E3-1", "E3-2", "E3-3", "E3-4", "E3-5",
     "E4-1", "E4-2", "E4-3", "E4-4", "E4-5",
     "E5-1", "E5-2", "E5-3", "E5-4", "E5-5",),
    index=1,
)

product_dataset = dataset.ProductDataset(
    "../data/" + select_dataset + ".pkl",
    config.NUM_PRODUCTS,
    config.MIN_PRODUCT_WIDTH,
    config.MAX_PRODUCT_WIDTH,
    config.MIN_PRODUCT_DEPTH,
    config.MAX_PRODUCT_DEPTH,
    config.MIN_PRODUCT_HEIGHT,
    config.MAX_PRODUCT_HEIGHT,
    config.MIN_PRODUCT_WEIGHT,
    config.MAX_PRODUCT_WEIGHT,
    force_overload=False,
)

# 随机排序模块
st.header("随机打乱")
order = product_dataset.get_order()

# 用表格展示随机排序后的货物
st.dataframe(order)

# 解决方案模块
st.header("解决方案")

# 选择参数
st.subheader("选择参数")
solution_type = st.selectbox(
    "选择你想测试的算法",
    ("Maxrects", "Column generation"),
    index=1,
)
tlim = st.slider("时间约束", 0, 100, value=10, step=5)
max_iters = st.slider("最大重复次数", 0, 5, value=1, step=1)

# 计算
if solution_type == "Maxrects":
    bin_pool = main.main(
        order,
        procedure="mr",
        max_iters=max_iters,
        tlim=tlim,
        superitems_horizontal=False,
    )
elif solution_type == "Column generation":
    superitems_horizontal = st.radio(
        "加入超级货物", ("是", "否"), index=1
    )
    cg_use_height_groups = st.radio(
        "按高度组调用", ("是", "否"), index=1
    )
    cg_mr_warm_start = st.radio(
        "使用Maxrects作为热启动", ("是", "否"), index=1
    )
    cg_max_iters = st.slider("最大迭代次数", 0, 100, value=20, step=5)
    cg_max_stag_iters = 3
    cg_sp_mr = st.radio(
        "对定价子问题使用maxrects", ("是", "否"), index=1
    )
    cg_sp_np_type = st.selectbox(
        "无放置策略",
        ("MIP", "CP"),
        index=0,
    )
    cg_sp_p_type = st.selectbox(
        "放置策略",
        ("Maxrects", "MIP", "CP"),
        index=0,
    )
    bin_pool = main.main(
        order,
        procedure="cg",
        max_iters=max_iters,
        tlim=tlim,
        superitems_horizontal=True if superitems_horizontal == "Yes" else False,
        cg_use_height_groups=True if cg_use_height_groups == "Yes" else False,
        cg_mr_warm_start=True if cg_mr_warm_start == "Yes" else False,
        cg_max_iters=cg_max_iters,
        cg_max_stag_iters=cg_max_stag_iters,
        cg_sp_mr=True if cg_sp_mr == "Yes" else False,
        cg_sp_np_type=cg_sp_np_type.lower(),
        cg_sp_p_type="mr" if cg_sp_p_type == "Maxrects" else cg_sp_p_type.lower(),
    )

# 展示压缩前的层
st.subheader("货物在层中的位置")
st.dataframe(bin_pool.get_original_layer_pool().to_dataframe())

# 展示装载率最大的集装箱
st.subheader("装载率最大的集装箱")
original_bin_pool = bin_pool.get_original_bin_pool()
max_density = 0
max_i = 0
for i, bin in enumerate(original_bin_pool):
    if bin.get_density() >= max_density:
        max_i = i
        max_density = bin.get_density()

max_bin = original_bin_pool[max_i]

df = max_bin.layer_pool.describe()
df["layer"] = df["layer"].apply(str)
st.dataframe(df)

# st.dataframe(max_bin.layer_pool.describe())

ax = max_bin.plot()
st.pyplot(plt.gcf())
st.write("最大装载率：")
st.write(max_bin.get_density())

# Success message
st.success("装箱程序已成功运行！")
