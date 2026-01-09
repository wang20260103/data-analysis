import streamlit as st

# 导入自定义模块
import styles
import sidebar
import data_processing
import rankings
import class_score_analysis
import assessment_item_analysis
import trend_analysis

# 设置页面配置
st.set_page_config(
    page_title="班级考核数据智能分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用自定义CSS
styles.apply_custom_css()

# 应用标题
st.markdown('<h1 class="main-header"><br>📊 班级量化考核数据智能分析平台</h1>', unsafe_allow_html=True)

# 初始化会话状态
sidebar.init_session_state()

# 渲染侧边栏导航
page = sidebar.render_sidebar()

# 根据用户选择的页面调用相应的功能函数
if page == "📁 数据导入":
    data_processing.data_import()
elif page == "🧹 数据清洗":
    data_processing.data_cleaning()
elif page == "🔧 填充空值":
    data_processing.fill_missing_values()
elif page == "🏆 查看前5名":
    rankings.view_top5()
elif page == "📉 查看后5名":
    rankings.view_bottom5()
elif page == "📊 班级总分分析":
    class_score_analysis.class_score_analysis()
elif page == "📋 考核项目分析":
    assessment_item_analysis.assessment_item_analysis()
elif page == "📈 变化趋势和风险预测":
    trend_analysis.trend_analysis()

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>班级量化考核数据智能分析平台 © 2025</div>",
    unsafe_allow_html=True
)

# 注入JavaScript来强制按钮样式
st.markdown("""
<script>
// 等待页面加载完成
window.addEventListener('load', function() {
    // 查找所有type="primary"的按钮
    const primaryButtons = document.querySelectorAll('button[type="primary"]');
    
    primaryButtons.forEach(button => {
        // 强制设置按钮颜色为蓝色
        button.style.backgroundColor = '#1f77b4';
        button.style.color = 'white';
        button.style.border = 'none';
        button.style.boxShadow = 'none';
        
        // 设置hover状态
        button.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#1a689e';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '#1f77b4';
        });
        
        // 设置active状态
        button.addEventListener('mousedown', function() {
            this.style.backgroundColor = '#155a8a';
        });
        
        button.addEventListener('mouseup', function() {
            this.style.backgroundColor = '#1a689e';
        });
    });
});
</script>
""", unsafe_allow_html=True)