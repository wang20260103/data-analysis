import streamlit as st
import os
import base64

# 读取并编码背景图片
@st.cache_resource
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# 获取背景图片的base64编码
def get_background_images():
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

    return bg_sidebar_base64, bg_title_base64

# 生成CSS样式
def get_custom_css():
    bg_sidebar_base64, bg_title_base64 = get_background_images()

    # 使用f-string，但确保CSS大括号被正确转义
    css = f"""
    <style>
        :root {{
            --primary-color: #1f77b4;
            --secondary-background: #f0f2f6;
        }}

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
        /* 表格基本样式 - 所有内容居中对齐 */
        /* 重置所有表格样式 */
        table {{
            width: 100%% !important;
            border-collapse: collapse !important;
            text-align: center !important;
        }}
        
        /* 确保所有表头居中对齐 */
        th {{
            text-align: center !important;
            padding: 8px !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 确保所有单元格默认居中对齐 - 针对所有类型的数据 */
        td {{
            text-align: center !important;
            padding: 8px !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 针对Streamlit生成的表格，增强选择器优先级 */
        .stDataFrame, .st-table {{
            width: 100%% !important;
        }}
        
        /* Streamlit表格表头 */
        .stDataFrame th, .st-table th {{
            text-align: center !important;
            padding: 8px !important;
            background-color: #f0f2f6 !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* Streamlit表格单元格 - 覆盖所有数据类型的默认对齐 */
        .stDataFrame td, .st-table td {{
            text-align: center !important;
            padding: 8px !important;
            justify-content: center !important;
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
        
        /* 强制覆盖Streamlit的默认样式 - 增强优先级 */
        [data-testid="stDataFrame"] th {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        [data-testid="stDataFrame"] td {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 覆盖Streamlit数据框的内置样式 - 确保所有列都居中 */
        .streamlit-dataframe td,
        .dataframe td,
        .streamlit-dataframe th,
        .dataframe th {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 针对不同容器下的表格 - 增强覆盖 */
        .main .stDataFrame table tbody tr td,
        .block-container .stDataFrame table tbody tr td,
        .element-container .stDataFrame table tbody tr td,
        .main .st-table table tbody tr td,
        .block-container .st-table table tbody tr td,
        .element-container .st-table table tbody tr td {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 针对数据框的内部元素 - 确保所有内容居中 */
        .dataframe-container .dataframe td,
        .dataframe-container .dataframe th {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 终极覆盖 - 确保所有表格相关元素都居中 */
        *[class*="dataframe"] td,
        *[class*="dataframe"] th,
        *[class*="table"] td,
        *[class*="table"] th {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 增强选择器 - 覆盖Streamlit的内置表格样式 */
        #root .main .block-container .element-container .stDataFrame table th,
        #root .main .block-container .element-container .stDataFrame table td,
        #root .main .block-container .element-container .st-table table th,
        #root .main .block-container .element-container .st-table table td {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 针对Streamlit数据框的特定结构 */
        [data-testid="stDataFrame"] > div > div > div > table th,
        [data-testid="stDataFrame"] > div > div > div > table td {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 覆盖数据框单元格的内容对齐 */
        .dataframe td,
        .dataframe th,
        .stDataFrame td,
        .stDataFrame th {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
            display: table-cell !important;
            vertical-align: middle !important;
        }}
        
        /* 确保所有可能的表格结构都被覆盖 */
        table th,
        table td,
        table thead th,
        table tbody td,
        table tfoot td {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 针对Streamlit的特殊表格类 */
        .stDataFrame__table th,
        .stDataFrame__table td,
        .stDataFrame__container th,
        .stDataFrame__container td {{
            text-align: center !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        /* 内联样式覆盖 - 确保所有表格元素都居中 */
        /* 移除了过于宽泛的选择器，改为仅针对表格元素的选择器 */
        
        /* 确保数据表格内容容器的样式 */
        .dataframe-container {{
            width: 100%% !important;
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
        
        /* 减小数据导入页面中按钮列之间的间距 */
        .stColumns {{
            gap: 0.5rem !important;
        }}
        
        /* 调整列内边距，让按钮更靠近 */
        .stColumns > div {{
            padding-right: 0.25rem !important;
            padding-left: 0.25rem !important;
        }}
    </style>
    """
    
    return css

# 应用自定义CSS
def apply_custom_css():
    css = get_custom_css()
    st.markdown(css, unsafe_allow_html=True)