import streamlit as st
import pandas as pd
import os

# 确保data目录存在
if not os.path.exists('data'):
    os.makedirs('data')

# 数据导入功能
def data_import():
    """实现数据导入功能"""
    st.markdown('<h2 class="section-header">📁 数据导入</h2>', unsafe_allow_html=True)
    
    # 使用绝对路径确保能正确读取data文件夹
    current_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    # 确保data目录存在
    os.makedirs(data_dir, exist_ok=True)
    
    # 文件上传 - 文件选择后自动保存到磁盘
    uploaded_file = st.file_uploader(
        "上传数据文件",
        type=['xlsx', 'csv'],
        help="支持.xlsx和.csv格式的文件"
    )
    
    # 文件选择后自动保存到磁盘
    if uploaded_file is not None:
        try:
            # 保存上传的文件到data文件夹
            file_path = os.path.join(data_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 显示成功信息
            st.success(f"✅ 文件已成功上传并保存: {uploaded_file.name}")
            
            # 立即更新文件列表并强制刷新页面
            st.rerun()
        except Exception as e:
            st.error(f"❌ 保存文件失败: {str(e)}")
    
    # 或者选择本地已有的数据文件
    st.write("或者选择本地已有的数据文件:")
    # 每次都重新读取文件列表，确保实时更新
    data_files = [f for f in os.listdir(data_dir) if f.endswith(('.xlsx', '.csv'))]
    
    if not data_files:
        st.info("📂 目前没有数据文件，请先上传文件")
        selected_file = None
    else:
        selected_file = st.selectbox("选择文件", data_files, key="file_selector")
    
    # 按钮布局 - 使用紧凑的水平布局让两个按钮更靠近
    if selected_file:
        col1, col2, col3 = st.columns([0.2, 0.18, 0.62], gap="small")
        
        with col1:
            # 读取数据按钮 - 移除use_container_width=True，使用默认大小
            if st.button("读取数据", type="primary", key="read_data_btn"):
                try:
                    file_path = os.path.join(data_dir, selected_file)
                    # 根据文件扩展名选择正确的读取方法
                    if selected_file.endswith('.xlsx'):
                        # 添加更详细的错误处理和日志
                        try:
                            df = pd.read_excel(file_path, engine='openpyxl')
                        except ImportError:
                            st.error(f"❌ 读取Excel文件失败: 缺少openpyxl库，请运行 'pip install openpyxl' 安装")
                            return
                        except Exception as e:
                            st.error(f"❌ 读取Excel文件失败: {str(e)}")
                            return
                    elif selected_file.endswith('.csv'):
                        # 从第3行开始读取.csv文件（跳过前2行）
                        try:
                            df = pd.read_csv(file_path, skiprows=2)
                        except Exception as e:
                            st.error(f"❌ 读取CSV文件失败: {str(e)}")
                            return
                    else:
                        st.error(f"❌ 不支持的文件格式: {selected_file}")
                        return
                    
                    # 删除所有Unnamed:开头的列（空列）
                    df = df.loc[:, ~df.columns.str.contains('^Unnamed:')]
                    
                    st.session_state.raw_data = df
                    st.session_state.current_file = selected_file
                    st.success(f"✅ 成功读取文件: {selected_file}")
                except Exception as e:
                    st.error(f"❌ 读取文件失败: {str(e)}")
                    st.error(f"❌ 错误类型: {type(e).__name__}")
                    import traceback
                    st.error(f"❌ 详细错误信息: {traceback.format_exc()}")
        
        with col2:
            # 删除文件按钮 - 移除use_container_width=True，使用默认大小
            if st.button("删除文件", type="primary", key="delete_file_btn"):
                try:
                    file_path = os.path.join(data_dir, selected_file)
                    
                    if os.path.exists(file_path):
                        if os.access(file_path, os.W_OK):
                            os.remove(file_path)
                            st.success(f"✅ 成功删除文件: {selected_file}")
                            
                            if hasattr(st.session_state, 'current_file') and st.session_state.current_file == selected_file:
                                st.session_state.current_file = None
                                st.session_state.raw_data = None
                                st.session_state.cleaned_data = None
                                st.session_state.filled_data = None
                            
                            st.rerun()
                        else:
                            st.error(f"❌ 没有权限删除文件: {selected_file}")
                    else:
                        st.error(f"❌ 文件不存在: {selected_file}")
                except Exception as e:
                    st.error(f"❌ 删除文件失败: {str(e)}")
        
        with col3:
            # 空列，用于占据剩余空间
            pass
    else:
        # 只有在选择了文件时才显示删除按钮
        if st.button("读取数据", type="primary", key="read_data_btn_empty"):
            st.warning("⚠️ 请先选择要读取的文件")
    
    # 显示原始数据
    if st.session_state.raw_data is not None:
        st.markdown('<div class="subsection-header-with-icon">👀 数据预览</div>', unsafe_allow_html=True)
        
        # 使用HTML生成居中对齐的表格
        preview_data = st.session_state.raw_data.head(10)
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
        
        # 使用HTML生成居中对齐的列信息表格
        col_html_table = f"""
        <table style="width: 100%; border-collapse: collapse; text-align: center;">
            <thead>
                <tr style="background-color: #f0f2f6;">
                    {''.join([f'<th style="padding: 8px; border: 1px solid #ddd;">{col}</th>' for col in col_info.columns])}
                </tr>
            </thead>
            <tbody>
                {''.join([
                    '<tr>' + ''.join([f'<td style="padding: 8px; border: 1px solid #ddd;">{val}</td>' for val in row]) + '</tr>'
                    for _, row in col_info.iterrows()
                ])}
            </tbody>
        </table>
        """
        st.markdown(col_html_table, unsafe_allow_html=True)
