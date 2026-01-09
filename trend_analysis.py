import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# 变化趋势和风险预测功能
def trend_analysis():
    """实现变化趋势和风险预测功能"""
    st.markdown('<h2 class="section-header">📈 变化趋势和风险预测</h2>', unsafe_allow_html=True)
    
    # 获取data目录下的Excel文件
    excel_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
    
    if not excel_files:
        st.warning("当前目录下没有找到Excel文件，请先导入数据")
        return
    
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
        return
    
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
        return
    
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