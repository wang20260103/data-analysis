import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import base64
import warnings
warnings.filterwarnings('ignore')

# 读取并编码背景图片
@st.cache_resource
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# 获取侧边栏背景图片的base64编码
bg_sidebar_path = ".streamlit/static/bg1.jpg"
if os.path.exists(bg_sidebar_path):
    bg_sidebar_base64 = get_base64_image(bg_sidebar_path)
    print(f"侧边栏背景图片Base64编码前100字符: {bg_sidebar_base64[:100]}...")
else:
    bg_sidebar_base64 = ""
    print("侧边栏背景图片文件不存在")

# 获取标题区域背景图片的base64编码
bg_title_path = ".streamlit/static/bg2.jpg"
if os.path.exists(bg_title_path):
    bg_title_base64 = get_base64_image(bg_title_path)
    print(f"标题背景图片Base64编码前100字符: {bg_title_base64[:100]}...")
else:
    bg_title_base64 = ""
    print("标题背景图片文件不存在")

# 生成改进建议的函数
def generate_improvement_suggestions(deductions):
    suggestions = []
    
    # 根据扣分项生成针对性建议
    if '手机管理' in deductions:
        suggestions.append("加强手机管理教育，制定明确的手机使用规定，严格执行课堂手机收纳制度")
    
    if '发型发饰' in deductions:
        suggestions.append("加强学生仪容仪表教育，明确发型发饰规范要求，定期检查")
    
    if '校服衣着' in deductions:
        suggestions.append("强化校服穿着规范，建立每日检查制度，对不符合要求的学生及时纠正")
    
    if '两操' in deductions:
        suggestions.append("提高早操和课间操质量，安排专人负责监督，定期开展评比活动")
    
    if '违规违纪' in deductions:
        suggestions.append("加强纪律教育，明确校规校纪，建立违纪行为记录和改进跟踪机制")
    
    if '男生寝室卫生' in deductions:
        suggestions.append("加强男生寝室卫生管理，制定卫生标准，定期检查评比，建立奖惩机制")
    
    if '女生寝室卫生' in deductions:
        suggestions.append("加强女生寝室卫生管理，制定卫生标准，定期检查评比，建立奖惩机制")
    
    if '教室卫生' in deductions:
        suggestions.append("建立教室卫生责任制，安排值日表，定期检查，保持教室环境整洁")
    
    if '教室规范' in deductions:
        suggestions.append("加强教室规范管理，包括桌椅摆放、墙面装饰、学习氛围等，创造良好学习环境")
    
    if '班主任考勤' in deductions:
        suggestions.append("班主任应加强考勤管理，确保按时到岗，做好班级日常管理工作")
    
    # 通用建议
    if len(deductions) > 3:
        suggestions.append("建议召开班级专题会议，全面分析问题，制定整体改进计划")
    
    suggestions.append("建立班级内部激励机制，鼓励学生自觉遵守各项规定")
    suggestions.append("加强与家长的沟通合作，共同促进学生全面发展")
    
    return suggestions

# 设置页面配置
st.set_page_config(
    page_title="班级考核数据智能分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置主题颜色
st.markdown(
    f"""
    <style>
        :root {{
            --primary-color: #1f77b4;
            --secondary-background: #f0f2f6;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# 自定义CSS样式
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-top: -4rem !important;
        margin-bottom: 1.5rem !important;
        padding-top: 0 !important;
    }}
    /* 增加选择器特异性，确保样式优先应用 */
    h2.section-header, div.section-header {{
        font-size: 1.6rem !important;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }}
    .metric-card {{
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    /* 表格基本样式 - 除特定列外，其他列居中对齐 */
    /* 重置所有表格样式 */
    table {{
        width: 100% !important;
        border-collapse: collapse !important;
    }}
    
    /* 确保所有表头居中对齐 */
    th {{
        text-align: center !important;
        padding: 8px !important;
    }}
    
    /* 确保所有单元格默认居中对齐 */
    td {{
        text-align: center !important;
        padding: 8px !important;
    }}
    
    /* 针对Streamlit生成的表格，增强选择器优先级 */
    .stDataFrame, .st-table {{
        width: 100% !important;
    }}
    
    /* Streamlit表格表头 */
    .stDataFrame th, .st-table th {{
        text-align: center !important;
        padding: 8px !important;
        background-color: #f0f2f6 !important;
    }}
    
    /* Streamlit表格单元格 */
    .stDataFrame td, .st-table td {{
        text-align: center !important;
        padding: 8px !important;
    }}
    
    /* 针对特定列的样式 - 第2列（实际班级总分）和第3列（名次）靠左对齐 */
    /* 使用更通用的选择器确保样式生效 */
    .stDataFrame table tbody tr td:nth-child(2),
    .st-table table tbody tr td:nth-child(2),
    .streamlit-dataframe table tbody tr td:nth-child(2),
    .dataframe table tbody tr td:nth-child(2),
    .stDataFrame table tbody tr td:nth-child(3),
    .st-table table tbody tr td:nth-child(3),
    .streamlit-dataframe table tbody tr td:nth-child(3),
    .dataframe table tbody tr td:nth-child(3) {{
        text-align: left !important;
        justify-content: flex-start !important;
        align-items: center !important;
    }}
    
    /* 确保所有父容器下的表格都应用样式 */
    .main .stDataFrame table tbody tr td:nth-child(2),
    .main .stDataFrame table tbody tr td:nth-child(3),
    .block-container .stDataFrame table tbody tr td:nth-child(2),
    .block-container .stDataFrame table tbody tr td:nth-child(3),
    .element-container .stDataFrame table tbody tr td:nth-child(2),
    .element-container .stDataFrame table tbody tr td:nth-child(3),
    .main .st-table table tbody tr td:nth-child(2),
    .main .st-table table tbody tr td:nth-child(3),
    .block-container .st-table table tbody tr td:nth-child(2),
    .block-container .st-table table tbody tr td:nth-child(3),
    .element-container .st-table table tbody tr td:nth-child(2),
    .element-container .st-table table tbody tr td:nth-child(3) {{
        text-align: left !important;
        justify-content: flex-start !important;
        align-items: center !important;
    }}
    
    /* 确保所有表头无论在哪个容器下都保持居中 */
    .stDataFrame thead tr th,
    .st-table thead tr th,
    .main .stDataFrame thead tr th,
    .block-container .stDataFrame thead tr th,
    .element-container .stDataFrame thead tr th {{
        text-align: center !important;
        justify-content: center !important;
        align-items: center !important;
    }}
    
    /* 强制覆盖Streamlit的默认样式 */
    [data-testid="stDataFrame"] th {{
        text-align: center !important;
    }}
    
    [data-testid="stDataFrame"] td {{
        text-align: center !important;
    }}
    
    [data-testid="stDataFrame"] tbody tr td:nth-child(2),
    [data-testid="stDataFrame"] tbody tr td:nth-child(3) {{
        text-align: left !important;
    }}
    
    /* 确保数据表格内容容器的样式 */
    .dataframe-container {{
        width: 100% !important;
    }}
    
    /* 确保单元格内的内容也应用对齐样式 */
    .dataframe td {{
        box-sizing: border-box !important;
    }}
    
    /* 自定义导航栏样式 */

    /* 确保primary按钮始终显示为蓝色 - 使用更高特异性的选择器 */
    .main .block-container .element-container [data-testid="stButton"] > button[type="primary"] {{
        background-color: #1f77b4 !important;
        color: white !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .main .block-container .element-container [data-testid="stButton"] > button[type="primary"]:hover {{
        background-color: #1a689e !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
    }}

    .main .block-container .element-container [data-testid="stButton"] > button[type="primary"]:active {{
        background-color: #155a8a !important;
    }}

    /* 同时添加对常规stButton类的支持 */
    .main .block-container .element-container .stButton > button[type="primary"] {{
        background-color: #1f77b4 !important;
        color: white !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .main .block-container .element-container .stButton > button[type="primary"]:hover {{
        background-color: #1a689e !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
    }}

    .main .block-container .element-container .stButton > button[type="primary"]:active {{
        background-color: #155a8a !important;
    }}

    /* 隐藏侧边栏中的单选按钮 - 多种选择器确保覆盖所有可能的结构 */
    [data-testid="stSidebar"] .stRadio > div > label > div:first-child {{
        display: none !important;
    }}
    
    [data-testid="stSidebar"] .stRadio > div > label > input {{
        display: none !important;
    }}
    
    [data-testid="stSidebar"] .stRadio label > div:nth-child(1) {{
        display: none !important;
    }}
    
    [data-testid="stSidebar"] .stRadio label > input {{
        display: none !important;
    }}
    
    [data-testid="stSidebar"] .stRadio > div > div > label > div:first-child {{
        display: none !important;
    }}
    
    [data-testid="stSidebar"] .stRadio > div > div > label > input {{
        display: none !important;
    }}
    
    /* 终极通用选择器 - 确保所有单选按钮元素都被隐藏 */
    [data-testid="stSidebar"] input[type="radio"] {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
    }}
    
    [data-testid="stSidebar"] .stRadio > div > div {{
        display: none !important;
    }}
    
    /* 侧边栏背景图片设置 - 终极选择器 */
    /* 直接选择侧边栏的最外层容器 */
    #root > div:nth-child(1) > div > div:nth-child(1) > div > section {{
        background-image: url("data:image/jpeg;base64,{bg_sidebar_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        z-index: 1 !important;
    }}
    
    /* 标题区域背景图片设置 */
    /* 选择主容器中的标题区域 */
    .main-header {{
        background-image: url("data:image/jpeg;base64,{bg_title_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        padding: 2rem 1rem !important;
        border-radius: 0.5rem !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8) !important;
        margin: 0 -1rem 1.5rem -1rem !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }}
    
    /* 移除Streamlit默认的容器边距，让标题紧贴浏览器边缘 */
    .main > div:first-child {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    
    .block-container {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    
    /* 确保根容器也没有默认边距 */
    #root > div:nth-child(1) > div > div:nth-child(2) > div {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    
    /* 确保侧边栏内容区域也应用相同的背景 */
    #root > div:nth-child(1) > div > div:nth-child(1) > div > section > div {{
        background: transparent !important;
    }}
    
    /* 确保侧边栏内所有div都透明，让背景显示出来 */
    [data-testid="stSidebar"] div {{
        background: transparent !important;
    }}
    
    /* 确保侧边栏内容清晰可见 */
    [data-testid="stSidebar"] * {{
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9) !important;
        font-weight: 600 !important;
        z-index: 2 !important;
    }}
    
    /* 确保侧边栏内容清晰可见 */
    [data-testid="stSidebar"] .stTitle,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stRadio label {{
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8) !important;
        font-weight: 600 !important;
    }}

    /* 调整单选按钮标签的样式，增加图标间距 */
    [data-testid="stSidebar"] .stRadio > div > label > div:last-child,
    [data-testid="stSidebar"] .stRadio label > div:last-child,
    [data-testid="stSidebar"] .stRadio > div > div > label > div:last-child {{
        margin-left: 0.5rem;
    }}

    /* 增大导航项目之间的上下间距 */
    [data-testid="stSidebar"] .stRadio > div > label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stRadio > div > div > label {{
        margin-top: 0.75rem !important;
        margin-bottom: 0.75rem !important;
        padding-top: 0.25rem !important;
        padding-bottom: 0.25rem !important;
    }}

    /* 三级标题样式 */
    .subsection-header {{
        background-color: #e8f4f8;
        color: #1f77b4;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: fit-content;
    }}

    /* 带有图标的三级标题 */
    .subsection-header-with-icon {{
        background-color: #e8f4f8;
        color: #1f77b4;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0 0.75rem 0;
        font-size: 1.2rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: fit-content;
    }}

    /* 四级标题样式 */
    .subsubsection-header {{
        background-color: #f0f8ff;
        color: #1f77b4;
        padding: 0.5rem 0.8rem;
        border-radius: 0.4rem;
        margin: 0.8rem 0 0.6rem 0;
        font-size: 1.05rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        width: fit-content;
    }}
    
    /* 减少页脚下方的留白 */
    .block-container {{
        padding-bottom: 1rem !important; /* 减少底部padding */
    }}
    
    /* 确保主容器底部没有过多边距 */
    .main {{
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }}
    
    /* 减少分隔线的上下边距 */
    hr {{ 
        margin: 0.25rem 0 !important;
    }}

    /* 调整页脚本身的边距 */
    [data-testid="stMarkdownContainer"]:has(div[style*="text-align: center"]):last-of-type {{
        margin-bottom: 0 !important;
    }}

    /* 直接针对Streamlit的footer元素设置样式 */
    footer {{
        padding: 0 !important;
        margin: 0 !important;
        height: auto !important;
        min-height: auto !important;
    }}

    /* 确保footer内的所有元素都没有额外边距 */
    footer * {{
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* 针对Streamlit特定的footer容器 */
    [data-testid="stFooter"] {{
        display: none !important;
    }}

    /* 确保页面底部没有额外的留白容器 */
    #root > div:nth-child(1) > div > div:nth-child(2) > div > div > div > div:last-child {{
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }}

    /* 终极覆盖 - 确保整个应用的最底部没有留白 */
    body {{
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
        overflow-x: hidden;
    }}

</style>
""", unsafe_allow_html=True)

# 应用标题
st.markdown('<h1 class="main-header"><br>📊 班级量化考核数据智能分析平台</h1>', unsafe_allow_html=True)

# 侧边栏
st.sidebar.title("功能导航")
page = st.sidebar.radio(
    "选择功能",
    ["📁 数据导入", "🧹 数据清洗", "🔧 填充空值", "🏆 查看前5名", "📉 查看后5名", "📊 班级总分分析", "📋 考核项目分析", "📈 变化趋势和风险预测"]
)

# 初始化session state
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None
if 'current_file' not in st.session_state:
    st.session_state.current_file = None

# 数据导入功能
if page == "📁 数据导入":
    st.markdown('<h2 class="section-header">📁 数据导入</h2>', unsafe_allow_html=True)
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "上传Excel文件",
        type=['xlsx'],
        help="支持.xlsx格式的Excel文件"
    )
    
    # 或者选择本地文件
    st.write("或者选择本地已有的Excel文件:")
    excel_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
    selected_file = st.selectbox("选择文件", excel_files) if excel_files else None
    
    # 读取数据按钮
    if st.button("读取数据", type="primary"):
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.session_state.raw_data = df
                st.session_state.current_file = uploaded_file.name
                st.success(f"成功读取文件: {uploaded_file.name}")
            except Exception as e:
                st.error(f"读取文件失败: {str(e)}")
        elif selected_file:
            try:
                df = pd.read_excel(f"data/{selected_file}")
                st.session_state.raw_data = df
                st.session_state.current_file = selected_file
                st.success(f"成功读取文件: {selected_file}")
            except Exception as e:
                st.error(f"读取文件失败: {str(e)}")
        else:
            st.warning("请先上传文件或选择本地文件")
    
    # 显示原始数据
    if st.session_state.raw_data is not None:
        st.markdown('<div class="subsection-header-with-icon">👀 数据预览</div>', unsafe_allow_html=True)
        st.dataframe(st.session_state.raw_data.head(10))
        
        # 数据基本信息
        st.markdown('<div class="subsection-header-with-icon">📊 数据基本信息</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("行数", st.session_state.raw_data.shape[0])
        with col2:
            st.metric("列数", st.session_state.raw_data.shape[1])
        with col3:
            missing_count = st.session_state.raw_data.isnull().sum().sum()
            st.metric("缺失值数量", missing_count)
        
        # 列信息
        st.markdown('<div class="subsection-header-with-icon">📋 列信息</div>', unsafe_allow_html=True)
        col_info = pd.DataFrame({
            '列名': st.session_state.raw_data.columns,
            '数据类型': st.session_state.raw_data.dtypes.values,
            '非空值数量': st.session_state.raw_data.count().values,
            '缺失值数量': st.session_state.raw_data.isnull().sum().values
        })
        st.dataframe(col_info)

# 数据清洗功能
elif page == "🧹 数据清洗":
    st.markdown('<h2 class="section-header">🧹 数据清洗</h2>', unsafe_allow_html=True)
    
    if st.session_state.raw_data is None:
        st.warning("请先导入数据")
    else:
        st.markdown('<div class="subsection-header-with-icon">🔍 数据质量分析</div>', unsafe_allow_html=True)
        
        # 显示数据质量问题
        df = st.session_state.raw_data
        missing_values = df.isnull().sum()
        duplicate_rows = df.duplicated().sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("重复行数", duplicate_rows)
        with col2:
            st.metric("有缺失值的列数", (missing_values > 0).sum())
        
        # 缺失值详情
        if missing_values.sum() > 0:
            st.markdown('<div class="subsection-header-with-icon">⚠️ 缺失值详情</div>', unsafe_allow_html=True)
            missing_df = pd.DataFrame({
                '列名': missing_values[missing_values > 0].index,
                '缺失值数量': missing_values[missing_values > 0].values,
                '缺失比例': (missing_values[missing_values > 0].values / len(df) * 100).round(2)
            })
            st.dataframe(missing_df)
        
        # 数据清洗选项
        st.markdown('<div class="subsection-header-with-icon">🧹 数据清洗选项</div>', unsafe_allow_html=True)
        
        remove_duplicates = st.checkbox("删除重复行", value=True)
        
        if st.button("开始清洗数据", type="primary"):
            cleaned_df = df.copy()
            
            # 删除重复行
            if remove_duplicates:
                before_count = len(cleaned_df)
                cleaned_df = cleaned_df.drop_duplicates()
                after_count = len(cleaned_df)
                removed_count = before_count - after_count
                if removed_count > 0:
                    st.success(f"已删除 {removed_count} 行重复数据")
            
            # 保存清洗后的数据
            st.session_state.cleaned_data = cleaned_df
            st.success("数据清洗完成！")
            
            # 显示清洗后的数据
            st.markdown('<div class="subsection-header-with-icon">✅ 清洗后的数据预览</div>', unsafe_allow_html=True)
            st.dataframe(cleaned_df.head(10))
            
            # 清洗前后对比
            col1, col2 = st.columns(2)
            with col1:
                st.metric("原始数据行数", len(df))
            with col2:
                st.metric("清洗后数据行数", len(cleaned_df))

# 填充空值功能
elif page == "🔧 填充空值":
    st.markdown('<h2 class="section-header">🔧 填充空值</h2>', unsafe_allow_html=True)
    
    if st.session_state.raw_data is None:
        st.warning("请先导入数据")
    else:
        # 使用原始数据或清洗后的数据
        if st.session_state.cleaned_data is not None:
            use_cleaned = st.checkbox("使用清洗后的数据", value=True)
            df = st.session_state.cleaned_data if use_cleaned else st.session_state.raw_data
        else:
            df = st.session_state.raw_data
            use_cleaned = False
        
        # 显示有缺失值的列
        missing_cols = df.columns[df.isnull().any()].tolist()
        
        if not missing_cols:
            st.success("数据中没有缺失值！")
        else:
            st.markdown(f'<div class="subsection-header-with-icon">⚠️ 发现 {len(missing_cols)} 列有缺失值</div>', unsafe_allow_html=True)
            st.info("将使用0填充所有缺失值")
            
            # 执行填充
            if st.button("执行填充", type="primary"):
                filled_df = df.copy()
                filled_df = filled_df.fillna(0)
                
                # 保存填充后的数据
                st.session_state.filled_data = filled_df
                st.success("空值填充完成！")
                
                # 显示填充后的数据
                st.markdown('<div class="subsection-header-with-icon">💧 填充后的数据预览</div>', unsafe_allow_html=True)
                st.dataframe(filled_df.head(10))
                
                # 填充前后对比
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("填充前缺失值", df.isnull().sum().sum())
                with col2:
                    st.metric("填充后缺失值", filled_df.isnull().sum().sum())

# 班级总分分析
elif page == "📊 班级总分分析":
    st.markdown('<h2 class="section-header">📊 班级总分分析</h2>', unsafe_allow_html=True)
    
    # 获取data目录下的Excel文件
    excel_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
    
    if not excel_files:
        st.warning("当前目录下没有找到Excel文件，请先导入数据")
        st.stop()
    
    # 提取月份信息并排序
    month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    months = []
    for file in excel_files:
        month = file.replace('.xlsx', '')
        if month in month_order:
            months.append(month)
    
    if not months:
        st.warning("未从Excel文件名中提取到有效的月份信息，请确保文件名格式为'X月.xlsx'")
        st.stop()
    
    # 按月份顺序排序
    months = sorted(months, key=lambda x: month_order.index(x))
    
    # 自动选择最近的月份
    latest_month = months[-1]
    
    # 选择月份
    selected_month = st.selectbox(
        "选择月份",
        months,
        index=months.index(latest_month)
    )
    
    # 从选中月份的Excel文件中读取数据
    selected_file = f"data/{selected_month}.xlsx"
    df = pd.read_excel(selected_file)
    
    # 检查是否有实际班级总分列或总分列
    total_score_cols = [col for col in df.columns if '实际班级总分' in col or '总分' in col]
    if not total_score_cols:
        st.error("数据中没有找到'实际班级总分'或'总分'列")
        st.stop()
    total_score_col = total_score_cols[0]
    
    # 获取班级和总分数据
    if '班级' in df.columns:
        score_data = df[['班级', total_score_col]].copy()
    else:
        st.warning("数据中没有找到'班级'列，将使用索引作为班级标识")
        score_data = pd.DataFrame({
            '班级': [f"班级{i+1}" for i in range(len(df))],
            total_score_col: df[total_score_col]
        })
    
    # 添加名次列（按总分从高到低排名）
    # 先处理非有限值
    score_data[total_score_col] = score_data[total_score_col].fillna(0)  # 将NA值填充为0
    score_data[total_score_col] = score_data[total_score_col].replace([np.inf, -np.inf], 0)  # 将inf值替换为0
    
    # 然后进行排名并转换为整数
    score_data['名次'] = score_data[total_score_col].rank(ascending=False, method='min').astype(int)
    
    # 计算平均分
    avg_score = score_data[total_score_col].mean()
    
    # 获取班级总数
    total_classes = len(score_data)
    
    # 数据标注函数：根据排名和平均分进行分类标注
    def annotate_performance(row):
        rank = row['名次']
        score = row[total_score_col]
        
        if rank <= 5:
            return "优秀"
        elif rank > total_classes - 5:
            return "待提高"
        elif score >= avg_score:
            return "良好"
        else:
            return "中等"
    
    # 添加数据标注列
    score_data['数据标注'] = score_data.apply(annotate_performance, axis=1)
    
    # 重新排列列顺序，将名次列放在总分后面，数据标注列放在最后
    score_data = score_data[['班级', total_score_col, '名次', '数据标注']]
    
    # 排序选项
    sort_order = st.radio(
        "排序方式",
        ["从高到低", "从低到高", "按原始顺序"]
    )
    
    if sort_order == "从高到低":
        score_data = score_data.sort_values(total_score_col, ascending=False)
    elif sort_order == "从低到高":
        score_data = score_data.sort_values(total_score_col, ascending=True)
    
    # 显示数据表格
    st.markdown('<div class="subsection-header-with-icon">📚 班级总分数据</div>', unsafe_allow_html=True)
    
    # 重置索引并命名为序号，从1开始
    display_df = score_data.copy()
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = "序号"
    
    # 显示表格（通过全局CSS样式实现居中对齐）
    st.dataframe(display_df, use_container_width=True)
    
    # 创建图表
    st.markdown('<div class="subsection-header-with-icon">📈 班级总分分析</div>', unsafe_allow_html=True)
    
    # 图表类型选择
    chart_type = st.selectbox(
        "选择图表类型",
        ["垂直柱状图", "水平柱状图", "折线图", "散点图"],
        index=1  # 默认选择水平柱状图
    )
    
    # 图表选项
    show_values = st.checkbox("在图表上显示数值", value=True)
    color_scheme = st.selectbox(
        "颜色方案",
        ["蓝色", "红色", "绿色", "彩虹"],
        index=3  # 默认选择彩虹颜色方案
    )
    
    # 设置颜色
    if color_scheme == "蓝色":
        bar_color = 'blue'
    elif color_scheme == "红色":
        bar_color = 'red'
    elif color_scheme == "绿色":
        bar_color = 'green'
    elif color_scheme == "彩虹":
        bar_color = px.colors.qualitative.Set3
    
    # 创建不同类型的图表
    if chart_type == "垂直柱状图":
        fig = px.bar(
            score_data,
            x='班级',
            y=total_score_col,
            title=f'各班级{selected_month}总分对比（垂直柱状图）',
            labels={total_score_col: '总分', '班级': '班级名称'},
            color='班级' if color_scheme == "彩虹" else None,
            color_discrete_sequence=bar_color if color_scheme == "彩虹" else ([bar_color] if color_scheme in ["蓝色", "红色", "绿色"] else None)
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,
            showlegend=True if color_scheme == "彩虹" else False
        )
        if show_values:
            fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    elif chart_type == "水平柱状图":
        fig = px.bar(
            score_data,
            y='班级',
            x=total_score_col,
            orientation='h',
            title=f'各班级{selected_month}总分对比（水平柱状图）',
            labels={total_score_col: '总分', '班级': '班级名称'},
            color='班级' if color_scheme == "彩虹" else None,
            color_discrete_sequence=bar_color if color_scheme == "彩虹" else ([bar_color] if color_scheme in ["蓝色", "红色", "绿色"] else None)
        )
        fig.update_layout(
            height=800,
            showlegend=True if color_scheme == "彩虹" else False
        )
        if show_values:
            fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')
    elif chart_type == "折线图":
        fig = px.line(
            score_data,
            x='班级',
            y=total_score_col,
            markers=True,
            title=f'各班级{selected_month}总分对比（折线图）',
            labels={total_score_col: '总分', '班级': '班级名称'},
            color='班级' if color_scheme == "彩虹" else None,
            color_discrete_sequence=bar_color if color_scheme == "彩虹" else ([bar_color] if color_scheme in ["蓝色", "红色", "绿色"] else None)
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,
            showlegend=True if color_scheme == "彩虹" else False
        )
        if show_values:
            fig.update_traces(texttemplate='%{y:.2f}', textposition='top center')
    elif chart_type == "散点图":
        fig = px.scatter(
            score_data,
            x='班级',
            y=total_score_col,
            title=f'各班级{selected_month}总分对比（散点图）',
            labels={total_score_col: '总分', '班级': '班级名称'},
            color='班级' if color_scheme == "彩虹" else None,
            color_discrete_sequence=bar_color if color_scheme == "彩虹" else ([bar_color] if color_scheme in ["蓝色", "红色", "绿色"] else None),
            size=total_score_col,
            size_max=20
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,
            showlegend=True if color_scheme == "彩虹" else False
        )
        if show_values:
            fig.update_traces(texttemplate='%{y:.2f}', textposition='top center')
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 统计信息
    st.markdown('<div class="subsection-header-with-icon">📊 统计信息</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("最高分", score_data[total_score_col].max())
    with col2:
        st.metric("最低分", score_data[total_score_col].min())
    with col3:
        st.metric("平均分", score_data[total_score_col].mean())
    with col4:
        st.metric("标准差", score_data[total_score_col].std())

# 查看前5名
elif page == "🏆 查看前5名":
    st.markdown('<h2 class="section-header">🏆 查看前5名</h2>', unsafe_allow_html=True)
    
    # 选择数据源
    data_source = st.selectbox(
        "选择数据源",
        ["原始数据", "清洗后数据", "填充后数据"]
    )
    
    if data_source == "原始数据" and st.session_state.raw_data is not None:
        df = st.session_state.raw_data
    elif data_source == "清洗后数据" and st.session_state.cleaned_data is not None:
        df = st.session_state.cleaned_data
    elif data_source == "填充后数据" and 'filled_data' in st.session_state and st.session_state.filled_data is not None:
        df = st.session_state.filled_data
    else:
        st.warning("请先导入数据或完成相应的数据处理步骤")
        st.stop()
    
    # 检查是否有实际班级总分列
    if '实际班级总分' not in df.columns:
        st.error("数据中没有找到'实际班级总分'列")
        st.stop()
    
    # 获取前5名
    if '班级' in df.columns:
        top5 = df.nlargest(5, '实际班级总分')[['班级', '实际班级总分']]
    else:
        st.warning("数据中没有找到'班级'列，将使用索引作为班级标识")
        temp_df = df.copy()
        temp_df['班级'] = [f"班级{i+1}" for i in range(len(df))]
        top5 = temp_df.nlargest(5, '实际班级总分')[['班级', '实际班级总分']]
    
    # 显示前5名表格
    st.markdown('<div class="subsection-header-with-icon">🏆 前5名班级</div>', unsafe_allow_html=True)
    
    # 重置索引并命名为序号，从1开始
    display_top5 = top5.copy()
    display_top5.index = range(1, len(display_top5) + 1)
    display_top5.index.name = "序号"
    
    # 显示表格（通过全局CSS样式实现居中对齐）
    st.dataframe(display_top5, use_container_width=True)
    
    # 创建前5名柱状图
    st.markdown('<div class="subsection-header-with-icon">📊 前5名班级总分对比</div>', unsafe_allow_html=True)
    
    fig = px.bar(
        top5,
        x='班级',
        y='实际班级总分',
        #title='前5名班级总分对比',
        labels={'实际班级总分': '实际总分', '班级': '班级名称'},
        color='实际班级总分',
        color_continuous_scale='Viridis'
    )
    
    # 设置图表布局
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=True
    )
    
    # 在柱子上显示数值
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 排行榜样式展示
    st.markdown('<div class="subsection-header-with-icon">📋 排行榜</div>', unsafe_allow_html=True)
    for i, (idx, row) in enumerate(top5.iterrows()):
        rank = i + 1
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"第{rank}名"
        st.markdown(f'<div class="subsection-header">{medal} {row["班级"]}</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("排名", rank)
        with col2:
            st.metric("总分", f"{row['实际班级总分']:.2f}")
        st.write("---")

# 查看后5名
elif page == "📉 查看后5名":
    st.markdown('<h2 class="section-header">📉 查看后5名</h2>', unsafe_allow_html=True)
    
    # 选择数据源
    data_source = st.selectbox(
        "选择数据源",
        ["原始数据", "清洗后数据", "填充后数据"]
    )
    
    if data_source == "原始数据" and st.session_state.raw_data is not None:
        df = st.session_state.raw_data
    elif data_source == "清洗后数据" and st.session_state.cleaned_data is not None:
        df = st.session_state.cleaned_data
    elif data_source == "填充后数据" and 'filled_data' in st.session_state and st.session_state.filled_data is not None:
        df = st.session_state.filled_data
    else:
        st.warning("请先导入数据或完成相应的数据处理步骤")
        st.stop()
    
    # 检查是否有实际班级总分列
    if '实际班级总分' not in df.columns:
        st.error("数据中没有找到'实际班级总分'列")
        st.stop()
    
    # 获取后5名
    if '班级' in df.columns:
        bottom5 = df.nsmallest(5, '实际班级总分')
    else:
        st.warning("数据中没有找到'班级'列，将使用索引作为班级标识")
        temp_df = df.copy()
        temp_df['班级'] = [f"班级{i+1}" for i in range(len(df))]
        bottom5 = temp_df.nsmallest(5, '实际班级总分')
    
    # 显示后5名表格
    st.markdown('<div class="subsection-header-with-icon">📉 后5名班级</div>', unsafe_allow_html=True)
    
    # 重置索引并命名为序号，从1开始
    display_bottom5 = bottom5[['班级', '实际班级总分']].copy()
    display_bottom5.index = range(1, len(display_bottom5) + 1)
    display_bottom5.index.name = "序号"
    
    # 显示表格（通过全局CSS样式实现居中对齐）
    st.dataframe(display_bottom5, use_container_width=True)
    
    # 创建后5名柱状图
    st.markdown('<div class="subsection-header-with-icon">📊 后5名班级总分对比</div>', unsafe_allow_html=True)
    
    fig = px.bar(
        bottom5,
        x='班级',
        y='实际班级总分',
        #title='后5名班级总分对比',
        labels={'实际班级总分': '实际总分', '班级': '班级名称'},
        color='实际班级总分',
        color_continuous_scale='Plasma'  # 使用不同的颜色方案区分前5名
    )
    
    # 设置图表布局
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=True
    )
    
    # 在柱子上显示数值
    fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 分析主要扣分项
    st.markdown('<div class="subsection-header-with-icon">⚠️ 主要扣分项分析</div>', unsafe_allow_html=True)
    
    # 获取评分项目列（排除班级、编号、总分等非评分项）
    scoring_columns = [col for col in df.columns if col not in ['编号', '班级', '班级教室', '初始分数', '实际班级总分']]
    
    # 为每个后5名班级分析扣分项
    for i, (idx, row) in enumerate(bottom5.iterrows()):
        with st.expander(f"📉 {row['班级']} - 扣分项分析"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric("总分", f"{row['实际班级总分']:.2f}")
            
            with col2:
                # 获取扣分项（负值）
                deductions = {}
                for col in scoring_columns:
                    if pd.notna(row[col]) and row[col] < 0:
                        deductions[col] = row[col]
                
                if deductions:
                    # 按扣分从多到少排序
                    sorted_deductions = sorted(deductions.items(), key=lambda x: x[1])
                    st.write("**主要扣分项（从多到少）：**")
                    for item, score in sorted_deductions:
                        st.write(f"- {item}: {score}")
                else:
                    st.write("无明显扣分项")
            
            # 提供改进建议
            st.write("**改进建议：**")
            suggestions = generate_improvement_suggestions(deductions)
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
            
            st.write("---")
    
    # 排行榜样式展示
    st.markdown('<div class="subsection-header-with-icon">📋 排行榜</div>', unsafe_allow_html=True)
    total_classes = len(df)
    for i, (idx, row) in enumerate(bottom5.iterrows()):
        rank = total_classes - i  # 从后往前排名
        st.markdown(f'<div class="subsection-header">第{rank}名 {row["班级"]}</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("排名", rank)
        with col2:
            st.metric("总分", f"{row['实际班级总分']:.2f}")
        st.write("---")

# 考核项目分析
elif page == "📋 考核项目分析":
    st.markdown('<h2 class="section-header">📋 考核项目分析</h2>', unsafe_allow_html=True)
    
    # 获取data目录下的Excel文件
    excel_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
    
    if not excel_files:
        st.warning("当前目录下没有找到Excel文件，请先导入数据")
        st.stop()
    
    # 提取月份信息并排序
    month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    months = []
    for file in excel_files:
        month = file.replace('.xlsx', '')
        if month in month_order:
            months.append(month)
    
    if not months:
        st.warning("未从Excel文件名中提取到有效的月份信息，请确保文件名格式为'X月.xlsx'")
        st.stop()
    
    # 按月份顺序排序
    months = sorted(months, key=lambda x: month_order.index(x))
    
    # 自动选择最近的月份
    latest_month = months[-1]
    
    # 选择月份
    selected_month = st.selectbox(
        "选择月份",
        months,
        index=months.index(latest_month)
    )
    
    # 根据选择的月份加载对应的Excel文件
    selected_file = f"data/{selected_month}.xlsx"
    try:
        df = pd.read_excel(selected_file)
        st.success(f"成功加载 {selected_month} 的数据")
    except Exception as e:
        st.error(f"加载 {selected_month} 数据时出错: {str(e)}")
        st.stop()
    
    # 检查必要的列是否存在
    required_columns = ['编号', '班级', '初始分数', '实际班级总分']
    if not all(col in df.columns for col in required_columns):
        st.error("数据格式不符合要求，请检查数据文件")
        st.stop()
    
    # 获取所有考核项目列（排除非考核项目列）
    scoring_columns = [col for col in df.columns if col not in required_columns]
    
    if not scoring_columns:
        st.error("未找到考核项目列，请检查数据文件")
        st.stop()
    
    # 统计每个考核项目的加减分总量
    st.markdown('<div class="subsection-header-with-icon">📊 考核项目加减分总量统计</div>', unsafe_allow_html=True)
    
    # 创建统计数据
    scoring_stats = []
    for col in scoring_columns:
        # 将考核项目列转换为数值类型，忽略无法转换的值
        df[col] = pd.to_numeric(df[col], errors='coerce')
        total_score = df[col].sum()
        scoring_stats.append({
            '考核项目': col,
            '加减分总量': total_score,
            '加分次数': (df[col] > 0).sum(),
            '扣分次数': (df[col] < 0).sum(),
            '总次数': ((df[col].notna()) & (df[col] != 0)).sum()
        })
    
    scoring_df = pd.DataFrame(scoring_stats)
    
    # 显示统计表格
    display_df = scoring_df.copy()
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = "序号"
    st.dataframe(display_df, use_container_width=True)
    
    # 可视化加减分总量
    st.markdown('<div class="subsection-header-with-icon">📈 考核项目加减分总量对比</div>', unsafe_allow_html=True)
    
    # 创建柱状图
    fig1 = px.bar(
        scoring_df,
        x='考核项目',
        y='加减分总量',
        
        labels={'加减分总量': '总分', '考核项目': '项目名称'},
        color='加减分总量',
        color_continuous_scale='RdYlGn',  # 红黄绿渐变，红色表示扣分，绿色表示加分
        text='加减分总量'  # 在柱子上显示数值
    )
    
    # 设置图表布局
    fig1.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=True,
        margin=dict(t=50, b=100)  # 增加底部边距，防止x轴标签被截断
    )
    
    # 设置数值显示格式
    fig1.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    
    # 显示图表
    st.plotly_chart(fig1, use_container_width=True)
    
    # 分析高频扣分项
    st.markdown('<div class="subsection-header-with-icon">🔍 高频扣分项分析</div>', unsafe_allow_html=True)
    
    # 筛选出有扣分的项目
    deduction_items = scoring_df[scoring_df['扣分次数'] > 0].copy()
    
    if not deduction_items.empty:
        # 按扣分次数排序
        deduction_items = deduction_items.sort_values('扣分次数', ascending=False)
        
        # 显示扣分项统计
        # st.write("**扣分项统计（按扣分次数排序）：**")
        display_deduction = deduction_items[['考核项目', '扣分次数', '加减分总量', '总次数']].copy()
        display_deduction.index = range(1, len(display_deduction) + 1)
        display_deduction.index.name = "序号"
        st.dataframe(display_deduction, use_container_width=True)
        
        # 可视化高频扣分项
        st.markdown('<div class="subsection-header-with-icon">📋 高频扣分项排名</div>', unsafe_allow_html=True)
        
        # 创建扣分项柱状图
        fig2 = px.bar(
            deduction_items,
            x='考核项目',
            y='扣分次数',
            
            labels={'扣分次数': '次数', '考核项目': '项目名称'},
            color='扣分次数',
            color_continuous_scale='Reds',
            text='扣分次数'
        )
        
        # 设置图表布局
        fig2.update_layout(
            xaxis_tickangle=-45,
            height=500,
            showlegend=True,
            margin=dict(t=50, b=100)
        )
        
        # 设置数值显示格式
        fig2.update_traces(texttemplate='%{y}', textposition='outside')
        
        # 显示图表
        st.plotly_chart(fig2, use_container_width=True)
        
        # 分析总结
        st.markdown('<div class="subsection-header-with-icon">📝 分析总结</div>', unsafe_allow_html=True)
        
        # 找出扣分最多的项目
        top_deduction = deduction_items.iloc[0]
        st.markdown(f"**扣分频率最高的项目：** {top_deduction['考核项目']}（共扣分 {top_deduction['扣分次数']} 次）")
        
        # 找出扣分总量最多的项目
        top_total_deduction = scoring_df.sort_values('加减分总量').iloc[0]
        if top_total_deduction['加减分总量'] < 0:
            st.markdown(f"**扣分总量最多的项目：** {top_total_deduction['考核项目']}（共扣 {top_total_deduction['加减分总量']:.2f} 分）")
        
        # 找出加分最多的项目
        top_total_addition = scoring_df.sort_values('加减分总量', ascending=False).iloc[0]
        if top_total_addition['加减分总量'] > 0:
            st.markdown(f"**加分总量最多的项目：** {top_total_addition['考核项目']}（共加 {top_total_addition['加减分总量']:.2f} 分）")
        
        # 提供改进建议
        st.markdown('<div class="subsection-header-with-icon">💡 改进建议</div>', unsafe_allow_html=True)
        
        # 针对扣分最多的项目提供建议
        if top_deduction['考核项目'] in ['手机管理', '发型发饰', '校服衣着', '两操', '违规违纪', '男生寝室卫生', '女生寝室卫生', '教室卫生', '教室规范', '班主任考勤']:
            suggestions = generate_improvement_suggestions([top_deduction['考核项目']])
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        
        # 通用建议
        st.write("- 针对高频扣分项，建议加强相关规章制度的宣传和执行力度")
        st.write("- 定期通报各班级的考核情况，激励先进，督促后进")
        st.write("- 对考核成绩较差的班级，建议进行个别辅导和帮助")
        
    else:
        st.info("没有发现扣分项，所有考核项目均为加分或无记录")

# 变化趋势和风险预测功能
elif page == "📈 变化趋势和风险预测":
    st.markdown('<h2 class="section-header">📈 变化趋势和风险预测</h2>', unsafe_allow_html=True)

    
    # 获取data目录下的Excel文件
    excel_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
    
    if not excel_files:
        st.warning("当前目录下没有找到Excel文件，请先导入数据")
        st.stop()
    
    # 定义月份顺序
    month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    
    # 提取月份信息并按顺序排序文件
    def get_month(file_name):
        return file_name.replace('.xlsx', '')
    
    # 过滤有效的月份文件
    valid_files = [f for f in excel_files if get_month(f) in month_order]
    
    # 按月份顺序排序文件
    sorted_files = sorted(valid_files, key=lambda x: month_order.index(get_month(x)))
    
    # 选择最近的3个月（默认）
    default_files = sorted_files[-3:] if len(sorted_files) >= 3 else sorted_files
    
    # 如果没有足够的有效月份文件，使用原始文件列表
    if not default_files:
        default_files = excel_files[:min(3, len(excel_files))]
    
    # 选择要对比的月份文件
    selected_files = st.multiselect(
        "选择要对比的月份文件",
        excel_files,
        default=default_files
    )
    
    if len(selected_files) < 2:
        st.warning("请至少选择2个月份文件进行对比")
        st.stop()
    
    # 读取并合并数据
    st.markdown('<div class="subsection-header-with-icon">📥 数据加载与合并</div>', unsafe_allow_html=True)
    
    all_data = []
    for file in selected_files:
        try:
            df = pd.read_excel(f"data/{file}")
            # 提取月份信息（从文件名中获取，假设文件名格式为"9月.xlsx"）
            month = file.replace('.xlsx', '')
            df['月份'] = month
            all_data.append(df)
            st.success(f"成功加载 {file}")
        except Exception as e:
            st.error(f"加载 {file} 时出错: {str(e)}")
            continue
    
    if not all_data:
        st.error("无法加载任何文件，请检查文件格式")
        st.stop()
    
    # 合并数据
    combined_df = pd.concat(all_data, ignore_index=True)
    st.write(f"合并后数据形状: {combined_df.shape}")
    
    # 数据预览
    st.markdown('<div class="subsection-header-with-icon">👀 合并后数据预览</div>', unsafe_allow_html=True)
    
    # 查找总分列（支持不同名称）
    total_score_col = None
    for col in combined_df.columns:
        if '实际班级总分' in col or '总分' in col:
            total_score_col = col
            break
    
    if total_score_col:
        # 使用透视表横向展示各月份总分
        try:
            # 创建透视表，按班级和月份展示总分
            pivot_df = combined_df.pivot_table(
                index='班级', 
                columns='月份', 
                values=total_score_col, 
                aggfunc='first'  # 假设每个班级每月只有一条记录
            ).reset_index()
            
            # 对月份列进行排序
            # 创建月份映射，用于排序
            month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
            
            # 获取当前的月份列，并按照month_order排序
            current_months = list(pivot_df.columns[1:])  # 排除'班级'列
            sorted_months = sorted(current_months, key=lambda x: month_order.index(x))
            
            # 重排透视表的列
            pivot_df = pivot_df[['班级'] + sorted_months]
            
            # 重命名列，格式为"月份总分"
            pivot_df.columns = ['班级'] + [f'{month}总分' for month in pivot_df.columns[1:]]
            
            # 将索引重命名为"序号"
            pivot_df.index = range(1, len(pivot_df) + 1)
            pivot_df.index.name = "序号"
            
            # 显示前10行数据
            st.dataframe(pivot_df.head(10), use_container_width=True)
        except Exception as e:
            st.error(f"创建横向预览时出错: {str(e)}")
            # 回退到基本预览
            st.markdown('<div class="subsection-header-with-icon">👀 基本数据预览</div>', unsafe_allow_html=True)
            preview_df = combined_df.copy()
            
            # 只显示存在的列
            available_columns = ['班级', '月份']
            if total_score_col in combined_df.columns:
                available_columns.append(total_score_col)
            
            # 过滤掉不存在的列
            final_columns = [col for col in available_columns if col in preview_df.columns]
            display_df = preview_df[final_columns].head(10).copy()
            
            # 将索引重命名为"序号"
            display_df.index = range(1, len(display_df) + 1)
            display_df.index.name = "序号"
            
            st.dataframe(display_df, use_container_width=True)
    else:
        # 没有找到总分列，显示基本预览
        st.markdown('<div class="subsection-header-with-icon">👀 基本数据预览</div>', unsafe_allow_html=True)
        preview_df = combined_df.copy()
        
        # 只显示基本信息
        basic_columns = ['班级', '月份']
        # 过滤掉不存在的列
        final_columns = [col for col in basic_columns if col in preview_df.columns]
        display_df = preview_df[final_columns].head(10).copy()
        
        # 将索引重命名为"序号"
        display_df.index = range(1, len(display_df) + 1)
        display_df.index.name = "序号"
        
        st.dataframe(display_df, use_container_width=True)
    
    # 班级纵向对比
    st.markdown('<div class="subsection-header-with-icon">📈 班级纵向对比</div>', unsafe_allow_html=True)
    
    # 检查是否有班级和实际班级总分列
    if '班级' not in combined_df.columns:
        st.error("数据中没有找到'班级'列")
    elif '实际班级总分' not in combined_df.columns:
        st.error("数据中没有找到'实际班级总分'列")
    else:
        # 选择要对比的班级
        available_classes = combined_df['班级'].unique()
        selected_class = st.selectbox("选择班级", available_classes)
        
        # 筛选该班级的数据
        class_data = combined_df[combined_df['班级'] == selected_class].copy()
        
        # 按月份排序
        # 创建月份映射，用于排序
        month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        class_data['月份排序'] = class_data['月份'].map(lambda x: month_order.index(x))
        class_data = class_data.sort_values('月份排序').drop('月份排序', axis=1)
        
        # 显示班级数据表格
        st.markdown(f'<div class="subsection-header-with-icon">📊 {selected_class} 各月份数据</div>', unsafe_allow_html=True)
        display_class_df = class_data[['月份', '实际班级总分'] + [col for col in combined_df.columns if col not in ['月份', '班级', '实际班级总分'] and '班级' not in col]].copy()
        # 将空值填充为0
        display_class_df = display_class_df.fillna(0)
        display_class_df.index = range(1, len(display_class_df) + 1)
        display_class_df.index.name = "序号"
        st.dataframe(display_class_df, use_container_width=True)
        
        # 创建班级总分趋势图
        st.markdown('<div class="subsection-header-with-icon">📈 班级总分趋势</div>', unsafe_allow_html=True)
        
        # 为趋势图准备数据（填充空值）
        chart_data = class_data.copy()
        chart_data['实际班级总分'] = chart_data['实际班级总分'].fillna(0)
        
        fig_class = px.line(
            chart_data,
            x='月份',
            y='实际班级总分',
            title=f'{selected_class} 实际班级总分月度趋势',
            labels={'实际班级总分': '总分', '月份': '月份'},
            markers=True,
            text='实际班级总分'
        )
        
        fig_class.update_layout(
            height=500,
            showlegend=True
        )
        
        fig_class.update_traces(texttemplate='%{y:.2f}', textposition='top center')
        
        st.plotly_chart(fig_class, use_container_width=True)
    
    # 班级扣分风险预测
    st.markdown('<div class="subsection-header-with-icon">⚠️ 班级扣分风险预测</div>', unsafe_allow_html=True)
    
    # 查找总分列（支持不同名称）
    total_score_col = None
    for col in combined_df.columns:
        if '实际班级总分' in col or '总分' in col:
            total_score_col = col
            break
    
    # 检查必要的列是否存在
    if '班级' not in combined_df.columns:
        st.error("数据中没有找到'班级'列，无法进行风险预测")
    elif total_score_col is None:
        st.error("数据中没有找到总分列，无法进行风险预测")
    elif '月份' not in combined_df.columns:
        st.error("数据中没有找到'月份'列，无法进行风险预测")
    else:
        try:
            # 导入numpy用于计算
            import numpy as np
            
            # 计算每个班级的总分变化趋势
            risk_classes = []
            all_classes = combined_df['班级'].unique()
            
            for cls in all_classes:
                # 获取该班级的数据
                class_data = combined_df[combined_df['班级'] == cls].copy()
                
                # 确保有足够的数据点（至少2个月份）
                if len(class_data) < 2:
                    continue
                
                # 按月份排序
                month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
                try:
                    class_data['月份排序'] = class_data['月份'].map(lambda x: month_order.index(x))
                    class_data = class_data.sort_values('月份排序').drop('月份排序', axis=1)
                except ValueError:
                    # 如果月份不在month_order中，跳过该班级
                    continue
                
                # 使用简单的线性回归计算趋势斜率
                # 月份转换为数值索引（0, 1, 2, ...）
                x = np.array(range(len(class_data)))
                y = np.array(class_data[total_score_col].fillna(0))  # 填充空值以确保计算正确
                
                # 计算斜率
                try:
                    slope = np.polyfit(x, y, 1)[0]
                except np.linalg.LinAlgError:
                    # 如果无法计算斜率，跳过该班级
                    continue
                
                # 如果斜率为负，说明总分呈下降趋势，存在扣分风险
                if slope < 0:
                    # 计算下降幅度（最后一个月与第一个月的差值）
                    score_diff = y[-1] - y[0]
                    
                    risk_classes.append({
                        '班级': cls,
                        '趋势斜率': slope,
                        '总分变化': score_diff,
                        '数据月份数': len(class_data),
                        '最近月份': class_data['月份'].iloc[-1]
                    })
            
            if risk_classes:
                # 转换为DataFrame并排序（按总分下降幅度从大到小）
                risk_df = pd.DataFrame(risk_classes)
                risk_df = risk_df.sort_values('总分变化', ascending=True)
                
                # 显示风险班级表格
               # st.write("###### 存在扣分风险的班级（总分呈下降趋势）")
                display_risk_df = risk_df.copy()
                display_risk_df.index = range(1, len(display_risk_df) + 1)
                display_risk_df.index.name = "序号"
                
                # 格式化显示
                display_risk_df['趋势斜率'] = display_risk_df['趋势斜率'].round(2)
                display_risk_df['总分变化'] = display_risk_df['总分变化'].round(2)
                
                st.dataframe(display_risk_df, use_container_width=True)
                
                # 可视化风险班级
                st.markdown('<div class="subsubsection-header">📉 风险班级总分变化趋势</div>', unsafe_allow_html=True)
                
                # 创建图表
                fig_risk = go.Figure()
                
                # 添加风险班级的趋势线
                for cls in risk_df['班级']:
                    class_data = combined_df[combined_df['班级'] == cls].copy()
                    month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
                    class_data['月份排序'] = class_data['月份'].map(lambda x: month_order.index(x))
                    class_data = class_data.sort_values('月份排序')
                    
                    # 为可视化准备数据（填充空值）
                    vis_data = class_data.copy()
                    vis_data[total_score_col] = vis_data[total_score_col].fillna(0)
                    
                    fig_risk.add_trace(go.Scatter(
                        x=vis_data['月份'],
                        y=vis_data[total_score_col],
                        mode='lines+markers',
                        name=cls
                    ))
                
                # 更新图表布局
                fig_risk.update_layout(
                    height=600,
                    
                    xaxis_title='月份',
                    yaxis_title=total_score_col,
                    legend_title='班级',
                    showlegend=True
                )
                
                st.plotly_chart(fig_risk, use_container_width=True)
                
                # 风险提示
                st.warning("⚠️ 以上班级的总分呈下降趋势，建议重点关注并采取改进措施！")
            else:
                st.success("✅ 所有班级的总分趋势均为上升或稳定，未发现明显扣分风险。")
        
        except Exception as e:
            st.error(f"进行风险预测时出错: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
    
    # 考核项目纵向对比
    st.markdown('<div class="subsection-header-with-icon">📈 考核项目纵向对比</div>', unsafe_allow_html=True)
    
    # 确定考核项目列
    required_columns = ['编号', '班级', '初始分数', '实际班级总分', '月份']
    scoring_columns = [col for col in combined_df.columns if col not in required_columns]
    
    if not scoring_columns:
        st.error("未找到考核项目列")
    else:
        # 选择要对比的考核项目
        selected_project = st.selectbox("选择考核项目", scoring_columns)
        
        # 按月份统计该项目的平均分
        # 确保selected_project列是数值类型
        combined_df[selected_project] = pd.to_numeric(combined_df[selected_project], errors='coerce')
        # 执行聚合操作
        monthly_stats = combined_df.groupby('月份')[selected_project].agg(['mean', 'sum', 'count']).reset_index()
        monthly_stats.columns = ['月份', '平均分', '总分', '班级数']
        
        # 按月份排序
        # 创建月份映射，用于排序
        month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        monthly_stats['月份排序'] = monthly_stats['月份'].map(lambda x: month_order.index(x))
        monthly_stats = monthly_stats.sort_values('月份排序').drop('月份排序', axis=1)
        
        # 显示统计数据表格
        st.markdown(f'<div class="subsection-header-with-icon">📊 {selected_project} 各月份统计</div>', unsafe_allow_html=True)
        display_stats_df = monthly_stats.copy()
        display_stats_df.index = range(1, len(display_stats_df) + 1)
        display_stats_df.index.name = "序号"
        st.dataframe(display_stats_df, use_container_width=True)
        
        # 创建考核项目趋势图
        st.markdown('<div class="subsection-header-with-icon">📈 考核项目趋势</div>', unsafe_allow_html=True)
        
        # 创建子图
        fig_project = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
        
        # 添加平均分折线图
        fig_project.add_trace(
            go.Scatter(
                x=monthly_stats['月份'],
                y=monthly_stats['平均分'],
                name='平均分',
                mode='lines+markers+text',
                text=monthly_stats['平均分'].round(2),
                textposition='top center'
            ),
            row=1, col=1
        )
        
        # 添加总分柱状图
        fig_project.add_trace(
            go.Bar(
                x=monthly_stats['月份'],
                y=monthly_stats['总分'],
                name='总分',
                text=monthly_stats['总分'].round(2),
                textposition='outside'
            ),
            row=2, col=1
        )
        
        # 更新布局
        fig_project.update_layout(
            height=600,
            title_text=f'{selected_project} 月度趋势分析',
            showlegend=True
        )
        
        fig_project.update_yaxes(title_text='平均分', row=1, col=1)
        fig_project.update_yaxes(title_text='总分', row=2, col=1)
        fig_project.update_xaxes(title_text='月份', row=2, col=1)
        
        st.plotly_chart(fig_project, use_container_width=True)

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>班级量化考核数据智能分析平台 © 2025</div>",
    unsafe_allow_html=True
)

# 注入JavaScript来强制按钮样式
st.markdown("""
<script>
// 等待页面加载完成
window.addEventListener('load', function() {
    // 查找所有type="primary"的按钮
    const primaryButtons = document.querySelectorAll('button[type="primary"]');
    
    primaryButtons.forEach(button => {
        // 强制设置按钮颜色为蓝色
        button.style.backgroundColor = '#1f77b4';
        button.style.color = 'white';
        button.style.border = 'none';
        button.style.boxShadow = 'none';
        
        // 设置hover状态
        button.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#1a689e';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '#1f77b4';
        });
        
        // 设置active状态
        button.addEventListener('mousedown', function() {
            this.style.backgroundColor = '#155a8a';
        });
        
        button.addEventListener('mouseup', function() {
            this.style.backgroundColor = '#1a689e';
        });
    });
});
</script>
""", unsafe_allow_html=True)

