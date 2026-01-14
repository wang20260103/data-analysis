import streamlit as st
import pandas as pd
import plotly.express as px

# 生成改进建议的函数
def generate_improvement_suggestions(deductions):
    """根据扣分项生成改进建议"""
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

# 查看前5名功能
def view_top5():
    """实现查看前5名班级功能"""
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
        return
    
    # 获取前5名
    top5 = df.nlargest(5, '实际班级总分')[['班级', '实际班级总分']]
   
    # 显示前5名表格
    st.markdown('<div class="subsection-header-with-icon">🏆 前5名班级</div>', unsafe_allow_html=True)
    
    # 重置索引并命名为序号，从1开始
    display_top5 = top5.copy()
    display_top5.index = range(1, len(display_top5) + 1)
    display_top5.index.name = "序号"
    
    # 使用HTML生成居中对齐的表格
    html_table = f"""
    <table style="width: 100%; border-collapse: collapse; text-align: center;">
        <thead>
            <tr style="background-color: #f0f2f6;">
                <th style="padding: 8px; border: 1px solid #ddd;">序号</th>
                {''.join([f'<th style="padding: 8px; border: 1px solid #ddd;">{col}</th>' for col in display_top5.columns])}
            </tr>
        </thead>
        <tbody>
            {''.join([
                '<tr>' + f'<td style="padding: 8px; border: 1px solid #ddd;">{index}</td>' + ''.join([f'<td style="padding: 8px; border: 1px solid #ddd;">{val}</td>' for val in row]) + '</tr>'
                for index, row in display_top5.iterrows()
            ])}
        </tbody>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)
    
    # 创建前5名柱状图
    st.markdown('<div class="subsection-header-with-icon">📊 前5名班级总分对比</div>', unsafe_allow_html=True)
    
    fig = px.bar(
        top5,
        x='班级',
        y='实际班级总分',
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

# 查看后5名功能
def view_bottom5():
    """实现查看后5名班级功能"""
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
        return
    
    # 获取后5名
    bottom5 = df.nsmallest(5, '实际班级总分')
    
    # 显示后5名表格
    st.markdown('<div class="subsection-header-with-icon">📉 后5名班级</div>', unsafe_allow_html=True)
    
    # 重置索引并命名为序号，从1开始
    display_bottom5 = bottom5[['班级', '实际班级总分']].copy()
    display_bottom5.index = range(1, len(display_bottom5) + 1)
    display_bottom5.index.name = "序号"
    
    # 使用HTML生成居中对齐的表格
    html_table = f"""
    <table style="width: 100%; border-collapse: collapse; text-align: center;">
        <thead>
            <tr style="background-color: #f0f2f6;">
                <th style="padding: 8px; border: 1px solid #ddd;">序号</th>
                {''.join([f'<th style="padding: 8px; border: 1px solid #ddd;">{col}</th>' for col in display_bottom5.columns])}
            </tr>
        </thead>
        <tbody>
            {''.join([
                '<tr>' + f'<td style="padding: 8px; border: 1px solid #ddd;">{index}</td>' + ''.join([f'<td style="padding: 8px; border: 1px solid #ddd;">{val}</td>' for val in row]) + '</tr>'
                for index, row in display_bottom5.iterrows()
            ])}
        </tbody>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)
    
    # 创建后5名柱状图
    st.markdown('<div class="subsection-header-with-icon">📊 后5名班级总分对比</div>', unsafe_allow_html=True)
    
    fig = px.bar(
        bottom5,
        x='班级',
        y='实际班级总分',
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
                    st.write("**主要扣分项：**")
                    for item in sorted_deductions[:3]:  # 只显示前3个主要扣分项
                        st.write(f"- {item[0]}: {item[1]:.2f}")
                    
                    # 生成改进建议
                    suggestions = generate_improvement_suggestions(deductions.keys())
                    
                    if suggestions:
                        st.write("\n**改进建议：**")
                        for suggestion in suggestions[:3]:  # 只显示前3个建议
                            st.write(f"- {suggestion}")
                else:
                    st.write("**没有明显扣分项**")