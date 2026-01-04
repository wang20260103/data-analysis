# 侧边栏
st.sidebar.title("功能导航")

# 初始化页面状态
if 'page' not in st.session_state:
    st.session_state.page = "数据导入"

# 定义导航项目和对应的图标
nav_items = [
    ("数据导入", "📁"),
    ("数据清洗", "🧹"),
    ("填充空值", "🔧"),
    ("查看前5名", "🏆"),
    ("查看后5名", "📉"),
    ("班级总分分析", "📊"),
    ("考核项目分析", "📋"),
    ("变化趋势和风险预测", "📈")
]

# 创建自定义导航按钮
for nav_item, icon in nav_items:
    is_selected = st.session_state.page == nav_item
    
    # 使用Streamlit的button组件创建导航按钮
    if st.sidebar.button(
        label=f"{icon} {nav_item}",
        key=f"nav_{nav_item}",
        use_container_width=True
    ):
        st.session_state.page = nav_item

# 获取当前页面
page = st.session_state.page