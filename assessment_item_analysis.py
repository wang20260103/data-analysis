import streamlit as st
import pandas as pd
import plotly.express as px
import os
from rankings import generate_improvement_suggestions

# 考核项目分析功能
def assessment_item_analysis():
    """实现考核项目分析功能"""
    st.markdown('<h2 class="section-header">📋 考核项目分析</h2>', unsafe_allow_html=True)
    
    # 获取data目录下的Excel文件
    excel_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
    
    if not excel_files:
        st.warning("当前目录下没有找到Excel文件，请先导入数据")
        return
    
    # 提取月份信息并排序
    month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    months = []
    for file in excel_files:
        month = file.replace('.xlsx', '')
        if month in month_order:
            months.append(month)
    
    if not months:
        st.warning("未从Excel文件名中提取到有效的月份信息，请确保文件名格式为'X月.xlsx'")
        return
    
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
        return
    
    # 检查必要的列是否存在
    required_columns = ['编号', '班级', '初始分数', '实际班级总分']
    if not all(col in df.columns for col in required_columns):
        st.error("数据格式不符合要求，请检查数据文件")
        return
    
    # 获取所有考核项目列（排除非考核项目列）
    scoring_columns = [col for col in df.columns if col not in required_columns]
    
    if not scoring_columns:
        st.error("未找到考核项目列，请检查数据文件")
        return
    
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
    
    # 使用HTML生成居中对齐的表格
    html_table = f"""
    <table style="width: 100%; border-collapse: collapse; text-align: center;">
        <thead>
            <tr style="background-color: #f0f2f6;">
                <th style="padding: 8px; border: 1px solid #ddd;">序号</th>
                {''.join([f'<th style="padding: 8px; border: 1px solid #ddd;">{col}</th>' for col in display_df.columns])}
            </tr>
        </thead>
        <tbody>
            {''.join([
                '<tr>' + f'<td style="padding: 8px; border: 1px solid #ddd;">{index}</td>' + ''.join([f'<td style="padding: 8px; border: 1px solid #ddd;">{val}</td>' for val in row]) + '</tr>'
                for index, row in display_df.iterrows()
            ])}
        </tbody>
    </table>
    """
    st.markdown(html_table, unsafe_allow_html=True)
    
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
        display_deduction = deduction_items[['考核项目', '扣分次数', '加减分总量', '总次数']].copy()
        display_deduction.index = range(1, len(display_deduction) + 1)
        display_deduction.index.name = "序号"
        
        # 使用HTML生成居中对齐的表格
        html_table = f"""
        <table style="width: 100%; border-collapse: collapse; text-align: center;">
            <thead>
                <tr style="background-color: #f0f2f6;">
                    <th style="padding: 8px; border: 1px solid #ddd;">序号</th>
                    {''.join([f'<th style="padding: 8px; border: 1px solid #ddd;">{col}</th>' for col in display_deduction.columns])}
                </tr>
            </thead>
            <tbody>
                {''.join([
                    '<tr>' + f'<td style="padding: 8px; border: 1px solid #ddd;">{index}</td>' + ''.join([f'<td style="padding: 8px; border: 1px solid #ddd;">{val}</td>' for val in row]) + '</tr>'
                    for index, row in display_deduction.iterrows()
                ])}
            </tbody>
        </table>
        """
        st.markdown(html_table, unsafe_allow_html=True)
        
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