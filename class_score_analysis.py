import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 班级总分分析功能
def class_score_analysis():
    """实现班级总分分析功能"""
    st.markdown('<h2 class="section-header">📊 班级总分分析</h2>', unsafe_allow_html=True)
    
    # 获取data目录下的Excel文件
    excel_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
    
    if not excel_files:
        st.warning("当前目录下没有找到Excel文件，请先导入数据")
        return
    
    # 选择月份
    selected_file = st.selectbox("选择月份", excel_files)
    selected_month = selected_file.replace('.xlsx', '')
    
    # 读取数据
    df = pd.read_excel(f"data/{selected_file}")
    
    # 检查是否有'班级'和'实际班级总分'列
    if '班级' not in df.columns or '实际班级总分' not in df.columns:
        st.error("数据中没有找到'班级'或'实际班级总分'列")
        return
    
    # 数据处理
    df = df.drop_duplicates(subset=['班级'], keep='first')  # 去重
    score_data = df[['班级', '实际班级总分']].copy()
    
    # 排序选项
    sort_order = st.radio("排序方式", ["从高到低", "从低到高"], horizontal=True)
    
    if sort_order == "从高到低":
        score_data = score_data.sort_values('实际班级总分', ascending=False)
    elif sort_order == "从低到高":
        score_data = score_data.sort_values('实际班级总分', ascending=True)
    
    # 显示数据表格
    st.markdown('<div class="subsection-header-with-icon">📚 班级总分数据</div>', unsafe_allow_html=True)
    
    # 重置索引并命名为序号，从1开始
    display_df = score_data.copy()
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = "序号"
    
    # 显示表格（通过全局CSS样式实现居中对齐）
    st.dataframe(display_df, use_container_width=True)
    
    # 创建图表
    st.markdown('<div class="subsection-header-with-icon">📈 班级总分对比</div>', unsafe_allow_html=True)
    
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
            y='实际班级总分',
            title=f'各班级{selected_month}总分对比（垂直柱状图）',
            labels={'实际班级总分': '总分', '班级': '班级名称'},
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
            x='实际班级总分',
            orientation='h',
            title=f'各班级{selected_month}总分对比（水平柱状图）',
            labels={'实际班级总分': '总分', '班级': '班级名称'},
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
        # 确保数据按班级排序，以便折线图正确连接
        line_data = score_data.sort_values('班级')
        
        # 为折线图选择单一颜色
        line_color = 'blue'  # 默认颜色
        if color_scheme == "红色":
            line_color = 'red'
        elif color_scheme == "绿色":
            line_color = 'green'
        elif color_scheme == "蓝色":
            line_color = 'blue'
        # 彩虹颜色方案也使用单一颜色
        
        # 折线图始终使用单一轨迹，不按班级分组，确保能正确显示连线
        fig = px.line(
            line_data,
            x='班级',
            y='实际班级总分',
            markers=True,
            title=f'各班级{selected_month}总分对比（折线图）',
            labels={'实际班级总分': '总分', '班级': '班级名称'},
            color_discrete_sequence=[line_color]
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,
            showlegend=False  # 折线图不需要图例
        )
        if show_values:
            fig.update_traces(texttemplate='%{y:.2f}', textposition='top center')
    elif chart_type == "散点图":
        fig = px.scatter(
            score_data,
            x='班级',
            y='实际班级总分',
            title=f'各班级{selected_month}总分对比（散点图）',
            labels={'实际班级总分': '总分', '班级': '班级名称'},
            color='班级' if color_scheme == "彩虹" else None,
            color_discrete_sequence=bar_color if color_scheme == "彩虹" else ([bar_color] if color_scheme in ["蓝色", "红色", "绿色"] else None),
            size='实际班级总分',
            size_max=10
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
        st.metric("最高分", score_data['实际班级总分'].max())
    with col2:
        st.metric("最低分", score_data['实际班级总分'].min())
    with col3:
        st.metric("平均分", score_data['实际班级总分'].mean())
    with col4:
        st.metric("标准差", score_data['实际班级总分'].std())