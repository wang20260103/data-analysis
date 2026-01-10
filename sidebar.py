import streamlit as st

# 初始化会话状态
def init_session_state():
    """初始化所有需要的会话状态变量"""
    if 'raw_data' not in st.session_state:
        st.session_state.raw_data = None
    if 'cleaned_data' not in st.session_state:
        st.session_state.cleaned_data = None
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
    if 'filled_data' not in st.session_state:
        st.session_state.filled_data = None

# 渲染侧边栏导航
def render_sidebar():
    """渲染侧边栏并返回用户选择的页面"""
    # 设置侧边栏标题
    st.sidebar.title("功能导航")
    
    # 创建导航选项
    page = st.sidebar.radio(
        "选择功能",
        ["📁 数据导入", "🔧 数据处理", "🏆 查看前5名", "📉 查看后5名", "📊 班级总分分析", "📋 考核项目分析", "📈 变化趋势和风险预测"]
    )
    
    return page