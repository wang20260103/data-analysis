import streamlit as st
import pandas as pd
import os

# 数据导入功能
def data_import():
    """实现数据导入功能"""
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
def data_cleaning():
    """实现数据清洗功能"""
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
def fill_missing_values():
    """实现填充空值功能"""
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