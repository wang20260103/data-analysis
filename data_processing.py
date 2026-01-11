import streamlit as st
import pandas as pd

# 数据处理功能（合并数据清洗和填充空值）
def data_processing():
    """实现数据处理功能，包括数据清洗和填充空值"""
    st.markdown('<h2 class="section-header">🔧 数据处理</h2>', unsafe_allow_html=True)
    
    if st.session_state.raw_data is None:
        st.warning("请先导入数据")
    else:
        # 数据清洗部分
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
            
            # 使用HTML生成居中对齐的表格
            html_table = f"""
            <table style="width: 100%; border-collapse: collapse; text-align: center;">
                <thead>
                    <tr style="background-color: #f0f2f6;">
                        {''.join([f'<th style="padding: 8px; border: 1px solid #ddd;">{col}</th>' for col in missing_df.columns])}
                    </tr>
                </thead>
                <tbody>
                    {''.join([
                        '<tr>' + ''.join([f'<td style="padding: 8px; border: 1px solid #ddd;">{val}</td>' for val in row]) + '</tr>'
                        for _, row in missing_df.iterrows()
                    ])}
                </tbody>
            </table>
            """
            st.markdown(html_table, unsafe_allow_html=True)
        
        # 数据清洗选项
        st.markdown('<div class="subsection-header-with-icon">🧹 数据清洗选项</div>', unsafe_allow_html=True)
        
        remove_duplicates = st.checkbox("删除重复行", value=True)
        
        if st.button("开始清洗数据", type="primary", key="clean_data_button"):
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
            preview_data = cleaned_df.head(10)
            
            # 使用HTML生成居中对齐的表格
            html_table = f"""
            <table style="width: 100%; border-collapse: collapse; text-align: center;">
                <thead>
                    <tr style="background-color: #f0f2f6;">
                        {''.join([f'<th style="padding: 8px; border: 1px solid #ddd;">{col}</th>' for col in preview_data.columns])}
                    </tr>
                </thead>
                <tbody>
                    {''.join([
                        '<tr>' + ''.join([f'<td style="padding: 8px; border: 1px solid #ddd;">{val}</td>' for val in row]) + '</tr>'
                        for _, row in preview_data.iterrows()
                    ])}
                </tbody>
            </table>
            """
            st.markdown(html_table, unsafe_allow_html=True)
            
            # 清洗前后对比
            col1, col2 = st.columns(2)
            with col1:
                st.metric("原始数据行数", len(df))
            with col2:
                st.metric("清洗后数据行数", len(cleaned_df))
        
        # 分隔线
        st.markdown("---")
        
        
        # 使用原始数据或清洗后的数据
        if st.session_state.cleaned_data is not None:
            use_cleaned = st.checkbox("使用清洗后的数据", value=True, key="use_cleaned_checkbox")
            df_fill = st.session_state.cleaned_data if use_cleaned else st.session_state.raw_data
        else:
            df_fill = st.session_state.raw_data
            use_cleaned = False
        
        # 显示有缺失值的列
        missing_cols = df_fill.columns[df_fill.isnull().any()].tolist()
        
        if not missing_cols:
            st.success("数据中没有缺失值！")
        else:
            st.markdown(f'<div class="subsection-header-with-icon">⚠️ 发现 {len(missing_cols)} 列有缺失值</div>', unsafe_allow_html=True)
            st.info("将使用0填充所有缺失值")
            
            # 执行填充
            if st.button("执行填充", type="primary", key="fill_data_button"):
                filled_df = df_fill.copy()
                filled_df = filled_df.fillna(0)
                
                # 保存填充后的数据
                st.session_state.filled_data = filled_df
                st.success("空值填充完成！")
                
                # 显示填充后的数据
                st.markdown('<div class="subsection-header-with-icon">💧 填充后的数据预览</div>', unsafe_allow_html=True)
                preview_data = filled_df.head(10)
                
                # 使用HTML生成居中对齐的表格
                html_table = f"""
                <table style="width: 100%; border-collapse: collapse; text-align: center;">
                    <thead>
                        <tr style="background-color: #f0f2f6;">
                            {''.join([f'<th style="padding: 8px; border: 1px solid #ddd;">{col}</th>' for col in preview_data.columns])}
                        </tr>
                    </thead>
                    <tbody>
                        {''.join([
                            '<tr>' + ''.join([f'<td style="padding: 8px; border: 1px solid #ddd;">{val}</td>' for val in row]) + '</tr>'
                            for _, row in preview_data.iterrows()
                        ])}
                    </tbody>
                </table>
                """
                st.markdown(html_table, unsafe_allow_html=True)
                
                # 填充前后对比
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("填充前缺失值", df_fill.isnull().sum().sum())
                with col2:
                    st.metric("填充后缺失值", filled_df.isnull().sum().sum())
