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

class DataAnalyzer:
    def __init__(self):
        self.data = {}
        self.cleaned_data = {}
        self.combined_data = None
        
    def read_excel_files(self, file_paths):
        """读取Excel文件"""
        print("开始读取Excel文件...")
        
        for file_path in file_paths:
            try:
                file_name = os.path.basename(file_path)
                full_path = f"data/{file_path}"
                print(f"正在读取: {full_path}")
                
                # 读取Excel文件
                df = pd.read_excel(full_path)
                self.data[file_name] = df
                
                print(f"{full_path} 读取成功，数据形状: {df.shape}")
                print(f"列名: {list(df.columns)}")
                print("-" * 50)
                
            except Exception as e:
                print(f"读取文件 {full_path} 时出错: {e}")
        
        return self.data
    
    def analyze_data_quality(self, df, data_name):
        """分析数据质量"""
        print(f"\n=== {data_name} 数据质量分析 ===")
        print(f"数据形状: {df.shape}")
        print(f"数据类型:\n{df.dtypes}")
        print(f"\n缺失值统计:\n{df.isnull().sum()}")
        print(f"\n重复行数: {df.duplicated().sum()}")
        
        # 数值列的描述性统计
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\n数值列描述性统计:\n{df[numeric_cols].describe()}")
        
        return df.isnull().sum(), df.duplicated().sum()
    
    def detect_outliers(self, df, column, method='iqr'):
        """检测异常值"""
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        elif method == 'zscore':
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            outliers = df[z_scores > 3]
        
        return outliers
    
    def clean_data(self, df, data_name):
        """数据清洗"""
        print(f"\n=== 开始清洗 {data_name} ===")
        df_cleaned = df.copy()
        
        # 1. 处理重复行
        initial_rows = len(df_cleaned)
        df_cleaned = df_cleaned.drop_duplicates()
        removed_duplicates = initial_rows - len(df_cleaned)
        print(f"删除重复行: {removed_duplicates} 行")
        
        # 2. 处理缺失值
        missing_values = df_cleaned.isnull().sum()
        print(f"\n缺失值处理:")
        
        for col in df_cleaned.columns:
            if df_cleaned[col].isnull().sum() > 0:
                if df_cleaned[col].dtype in ['object']:
                    # 分类变量：用众数填充
                    mode_value = df_cleaned[col].mode()[0] if not df_cleaned[col].mode().empty else 'Unknown'
                    df_cleaned[col].fillna(mode_value, inplace=True)
                    print(f"列 '{col}': 用众数 '{mode_value}' 填充 {missing_values[col]} 个缺失值")
                else:
                    # 数值变量：用中位数填充
                    median_value = df_cleaned[col].median()
                    df_cleaned[col].fillna(median_value, inplace=True)
                    print(f"列 '{col}': 用中位数 {median_value} 填充 {missing_values[col]} 个缺失值")
        
        # 3. 检测和处理异常值
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        print(f"\n异常值检测:")
        
        for col in numeric_cols:
            outliers = self.detect_outliers(df_cleaned, col)
            if len(outliers) > 0:
                print(f"列 '{col}': 发现 {len(outliers)} 个异常值")
                # 用上下边界值替换异常值
                Q1 = df_cleaned[col].quantile(0.25)
                Q3 = df_cleaned[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                df_cleaned[col] = np.where(df_cleaned[col] < lower_bound, lower_bound, df_cleaned[col])
                df_cleaned[col] = np.where(df_cleaned[col] > upper_bound, upper_bound, df_cleaned[col])
                print(f"已将异常值替换为边界值 [{lower_bound:.2f}, {upper_bound:.2f}]")
        
        print(f"\n{data_name} 清洗完成，最终数据形状: {df_cleaned.shape}")
        return df_cleaned
    
    def perform_statistical_analysis(self, df):
        """执行统计分析"""
        print("\n=== 统计分析结果 ===")
        
        # 基本统计信息
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print("\n数值列统计信息:")
            stats_df = df[numeric_cols].describe()
            print(stats_df)
            
            # 计算变异系数
            print("\n变异系数:")
            for col in numeric_cols:
                cv = df[col].std() / df[col].mean()
                print(f"{col}: {cv:.4f}")
        
        # 分类列统计
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            print("\n分类列统计信息:")
            for col in categorical_cols:
                print(f"\n{col} 的值分布:")
                print(df[col].value_counts())
                print(f"唯一值数量: {df[col].nunique()}")
        
        return df[numeric_cols].describe() if len(numeric_cols) > 0 else None
    
    def create_visualizations(self, df, data_name):
        """创建可视化图表"""
        print(f"\n=== 为 {data_name} 创建可视化图表 ===")
        
        # 创建输出目录
        if not os.path.exists('charts'):
            os.makedirs('charts')
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # 1. 数值列的分布图
        if len(numeric_cols) > 0:
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
                ax = axes[i] if len(numeric_cols) > 1 else axes[0]
                sns.histplot(df[col], kde=True, ax=ax)
                ax.set_title(f'{col} 分布图')
                ax.set_xlabel(col)
                ax.set_ylabel('频数')
            
            # 隐藏多余的子图
            for i in range(len(numeric_cols), len(axes)):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            plt.savefig(f'charts/{data_name}_数值分布.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"已保存数值分布图: charts/{data_name}_数值分布.png")
        
        # 2. 相关性热力图
        if len(numeric_cols) > 1:
            plt.figure(figsize=(10, 8))
            correlation_matrix = df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=0.5)
            plt.title(f'{data_name} 相关性热力图')
            plt.tight_layout()
            plt.savefig(f'charts/{data_name}_相关性热力图.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"已保存相关性热力图: charts/{data_name}_相关性热力图.png")
        
        # 3. 箱线图
        if len(numeric_cols) > 0:
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
                ax = axes[i] if len(numeric_cols) > 1 else axes[0]
                sns.boxplot(y=df[col], ax=ax)
                ax.set_title(f'{col} 箱线图')
                ax.set_ylabel(col)
            
            # 隐藏多余的子图
            for i in range(len(numeric_cols), len(axes)):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            plt.savefig(f'charts/{data_name}_箱线图.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"已保存箱线图: charts/{data_name}_箱线图.png")
        
        # 4. 分类列的条形图
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                if df[col].nunique() <= 20:  # 只显示唯一值不超过20个的分类列
                    plt.figure(figsize=(12, 6))
                    value_counts = df[col].value_counts()
                    sns.barplot(x=value_counts.index, y=value_counts.values)
                    plt.title(f'{col} 分布图')
                    plt.xlabel(col)
                    plt.ylabel('频数')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.savefig(f'charts/{data_name}_{col}_分布.png', dpi=300, bbox_inches='tight')
                    plt.close()
                    print(f"已保存 {col} 分布图: charts/{data_name}_{col}_分布.png")
    
    def combine_monthly_data(self):
        """合并月度数据"""
        print("\n=== 合并月度数据 ===")
        
        if len(self.cleaned_data) == 0:
            print("没有清洗后的数据可以合并")
            return None
        
        # 添加月份标识
        combined_dfs = []
        for file_name, df in self.cleaned_data.items():
            df_copy = df.copy()
            # 从文件名中提取月份
            month = file_name.replace('.xlsx', '')
            df_copy['月份'] = month
            combined_dfs.append(df_copy)
        
        # 合并所有数据
        self.combined_data = pd.concat(combined_dfs, ignore_index=True)
        print(f"合并完成，总数据形状: {self.combined_data.shape}")
        
        return self.combined_data
    
    def analyze_trends(self):
        """分析趋势"""
        if self.combined_data is None:
            print("没有合并的数据可供分析")
            return
        
        print("\n=== 趋势分析 ===")
        
        numeric_cols = self.combined_data.select_dtypes(include=[np.number]).columns
        
        # 创建趋势图
        for col in numeric_cols:
            if col != '月份':  # 跳过月份列
                plt.figure(figsize=(12, 6))
                monthly_stats = self.combined_data.groupby('月份')[col].agg(['mean', 'median', 'std'])
                
                plt.plot(monthly_stats.index, monthly_stats['mean'], marker='o', label='平均值')
                plt.plot(monthly_stats.index, monthly_stats['median'], marker='s', label='中位数')
                
                plt.title(f'{col} 月度趋势')
                plt.xlabel('月份')
                plt.ylabel(col)
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(f'charts/{col}_趋势分析.png', dpi=300, bbox_inches='tight')
                plt.close()
                print(f"已保存 {col} 趋势图: charts/{col}_趋势分析.png")
    
    def generate_report(self):
        """生成分析报告"""
        print("\n=== 生成分析报告 ===")
        
        report = []
        report.append("# 数据分析报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 数据概览
        report.append("## 数据概览")
        for file_name, df in self.data.items():
            report.append(f"- {file_name}: {df.shape[0]} 行, {df.shape[1]} 列")
        report.append("")
        
        # 数据质量
        report.append("## 数据质量")
        for file_name, df in self.data.items():
            missing_count = df.isnull().sum().sum()
            duplicate_count = df.duplicated().sum()
            report.append(f"- {file_name}: 缺失值 {missing_count} 个, 重复行 {duplicate_count} 行")
        report.append("")
        
        # 清洗后数据
        report.append("## 清洗后数据")
        for file_name, df in self.cleaned_data.items():
            report.append(f"- {file_name}: {df.shape[0]} 行, {df.shape[1]} 列")
        report.append("")
        
        # 合并数据
        if self.combined_data is not None:
            report.append("## 合并数据")
            report.append(f"- 总行数: {self.combined_data.shape[0]}")
            report.append(f"- 总列数: {self.combined_data.shape[1]}")
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
        return report_text
    
    def run_complete_analysis(self, file_paths):
        """运行完整分析流程"""
        print("开始完整数据分析流程...")
        
        # 1. 读取数据
        self.read_excel_files(file_paths)
        
        # 2. 分析数据质量
        for file_name, df in self.data.items():
            self.analyze_data_quality(df, file_name)
        
        # 3. 数据清洗
        for file_name, df in self.data.items():
            cleaned_df = self.clean_data(df, file_name)
            self.cleaned_data[file_name] = cleaned_df
        
        # 4. 统计分析
        for file_name, df in self.cleaned_data.items():
            self.perform_statistical_analysis(df)
        
        # 5. 创建可视化
        for file_name, df in self.cleaned_data.items():
            self.create_visualizations(df, file_name.replace('.xlsx', ''))
        
        # 6. 合并数据和趋势分析
        self.combine_monthly_data()
        self.analyze_trends()
        
        # 7. 生成报告
        self.generate_report()
        
        print("\n数据分析完成！")
        print("生成的文件:")
        print("- charts/: 包含所有可视化图表")
        print("- 数据分析报告.md: 详细的分析报告")

# 主程序
if __name__ == "__main__":
    # 创建数据分析器
    analyzer = DataAnalyzer()
    
    # 获取data目录下的Excel文件
    excel_files = []
    for file in os.listdir('data'):
        if file.endswith('.xlsx'):
            excel_files.append(file)
    
    if not excel_files:
        print("当前目录下没有找到Excel文件")
    else:
        print(f"找到Excel文件: {excel_files}")
        
        # 运行完整分析
        analyzer.run_complete_analysis(excel_files)