import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def analyze_excel_files():
    """分析Excel文件的主函数"""
    print("开始数据分析...")
    
    # 获取data目录下的Excel文件
    excel_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
    print(f"找到Excel文件: {excel_files}")
    
    # 创建输出目录
    if not os.path.exists('charts'):
        os.makedirs('charts')
        print("创建charts目录")
    
    all_data = {}
    cleaned_data = {}
    
    # 1. 读取数据
    for file in excel_files:
        try:
            print(f"\n正在读取: data/{file}")
            df = pd.read_excel(f"data/{file}")
            all_data[file] = df
            print(f"数据形状: {df.shape}")
            print(f"列名: {list(df.columns)}")
        except Exception as e:
            print(f"读取 {file} 时出错: {e}")
            continue
    
    # 2. 数据清洗和分析
    for file_name, df in all_data.items():
        print(f"\n=== 分析 {file_name} ===")
        
        # 数据质量检查
        print(f"缺失值: {df.isnull().sum().sum()}")
        print(f"重复行: {df.duplicated().sum()}")
        
        # 数据清洗
        df_cleaned = df.copy()
        
        # 处理缺失值
        for col in df_cleaned.columns:
            if df_cleaned[col].isnull().sum() > 0:
                if df_cleaned[col].dtype in ['object']:
                    mode_value = df_cleaned[col].mode()[0] if not df_cleaned[col].mode().empty else 'Unknown'
                    df_cleaned[col].fillna(mode_value, inplace=True)
                else:
                    median_value = df_cleaned[col].median()
                    df_cleaned[col].fillna(median_value, inplace=True)
        
        # 处理重复行
        df_cleaned = df_cleaned.drop_duplicates()
        
        cleaned_data[file_name] = df_cleaned
        print(f"清洗后数据形状: {df_cleaned.shape}")
        
        # 3. 创建可视化图表
        month_name = file_name.replace('.xlsx', '')
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            # 数值分布图
            n_cols = min(3, len(numeric_cols))
            n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
            if n_rows == 1 and n_cols == 1:
                axes = [axes]
            elif n_rows == 1:
                axes = axes
            else:
                axes = axes.flatten()
            
            for i, col in enumerate(numeric_cols):
                if i < len(axes):
                    ax = axes[i] if len(numeric_cols) > 1 else axes[0]
                    sns.histplot(df_cleaned[col], kde=True, ax=ax)
                    ax.set_title(f'{col} 分布')
                    ax.set_xlabel(col)
                    ax.set_ylabel('频数')
            
            # 隐藏多余的子图
            for i in range(len(numeric_cols), len(axes)):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            plt.savefig(f'charts/{month_name}_数值分布.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"已保存 {month_name} 数值分布图")
            
            # 箱线图
            for i, col in enumerate(numeric_cols):
                plt.figure(figsize=(8, 6))
                try:
                    sns.boxplot(y=df_cleaned[col])
                    plt.title(f'{col} 箱线图')
                    plt.ylabel(col)
                    plt.tight_layout()
                    plt.savefig(f'charts/{month_name}_{col}_箱线图.png', dpi=300, bbox_inches='tight')
                    plt.close()
                    print(f"已保存 {col} 箱线图")
                except Exception as e:
                    print(f"创建 {col} 箱线图时出错: {e}")
                    plt.close()
            
            # 相关性热力图
            if len(numeric_cols) > 1:
                plt.figure(figsize=(10, 8))
                correlation_matrix = df_cleaned[numeric_cols].corr()
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                           square=True, linewidths=0.5)
                plt.title(f'{month_name} 相关性热力图')
                plt.tight_layout()
                plt.savefig(f'charts/{month_name}_相关性热力图.png', dpi=300, bbox_inches='tight')
                plt.close()
                print(f"已保存 {month_name} 相关性热力图")
    
    # 4. 合并数据并分析趋势
    if len(cleaned_data) > 1:
        print("\n=== 合并数据并分析趋势 ===")
        
        # 添加月份标识并合并
        combined_dfs = []
        for file_name, df in cleaned_data.items():
            df_copy = df.copy()
            month = file_name.replace('.xlsx', '')
            df_copy['月份'] = month
            combined_dfs.append(df_copy)
        
        combined_data = pd.concat(combined_dfs, ignore_index=True)
        print(f"合并后数据形状: {combined_data.shape}")
        
        # 合并后数据预览（横向展示各月份总分）
        print("\n=== 合并后数据预览 ===")
        
        # 查找总分列
        total_score_col = None
        for col in combined_data.columns:
            if '实际班级总分' in col or '总分' in col:
                total_score_col = col
                break
        
        if total_score_col:
            # 创建透视表，按班级和月份展示总分
            pivot_df = combined_data.pivot_table(
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
            
            print(f"预览数据列: {list(pivot_df.columns)}")
            print("\n前10行数据预览:")
            print(pivot_df.head(10))
            print(f"\n总数据行数: {len(pivot_df)}")
        else:
            print("未找到总分列，无法生成横向预览")
            # 回退到原始预览
            preview_df = combined_data.copy()
            
            # 将索引重命名为"序号"
            preview_df.index = range(1, len(preview_df) + 1)
            preview_df.index.name = "序号"
            
            # 显示基本信息
            print(f"合并后数据形状: {combined_data.shape}")
            print(f"列名: {list(combined_data.columns)}")
            print("\n前10行数据预览:")
            print(preview_df.head(10))
        
        # 分析趋势
        numeric_cols = combined_data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col != '月份' and combined_data[col].nunique() > 1:  # 跳过月份列和常数列
                try:
                    plt.figure(figsize=(12, 6))
                    monthly_stats = combined_data.groupby('月份')[col].mean()
                    
                    plt.plot(monthly_stats.index, monthly_stats.values, marker='o')
                    plt.title(f'{col} 月度趋势')
                    plt.xlabel('月份')
                    plt.ylabel(col)
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                    plt.savefig(f'charts/{col}_趋势分析.png', dpi=300, bbox_inches='tight')
                    plt.close()
                    print(f"已保存 {col} 趋势图")
                except Exception as e:
                    print(f"创建 {col} 趋势图时出错: {e}")
    
    # 5. 生成报告
    print("\n=== 生成分析报告 ===")
    
    report = []
    report.append("# 数据分析报告")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # 数据概览
    report.append("## 数据概览")
    for file_name, df in all_data.items():
        report.append(f"- {file_name}: {df.shape[0]} 行, {df.shape[1]} 列")
    report.append("")
    
    # 数据质量
    report.append("## 数据质量")
    for file_name, df in all_data.items():
        missing_count = df.isnull().sum().sum()
        duplicate_count = df.duplicated().sum()
        report.append(f"- {file_name}: 缺失值 {missing_count} 个, 重复行 {duplicate_count} 行")
    report.append("")
    
    # 清洗后数据
    report.append("## 清洗后数据")
    for file_name, df in cleaned_data.items():
        report.append(f"- {file_name}: {df.shape[0]} 行, {df.shape[1]} 列")
    report.append("")
    
    # 图表列表
    report.append("## 生成的图表")
    if os.path.exists('charts'):
        charts = os.listdir('charts')
        for chart in charts:
            report.append(f"- {chart}")
    
    # 保存报告
    report_text = "\n".join(report)
    with open('数据分析报告.md', 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print("分析报告已保存: 数据分析报告.md")
    print("\n数据分析完成！")
    print("生成的文件:")
    print("- charts/: 包含所有可视化图表")
    print("- 数据分析报告.md: 详细的分析报告")

if __name__ == "__main__":
    analyze_excel_files()