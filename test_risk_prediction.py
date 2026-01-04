import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 创建测试数据
data = {
    '班级': ['1班', '2班', '3班', '4班', '1班', '2班', '3班', '4班', '1班', '2班', '3班', '4班'],
    '月份': ['9月', '9月', '9月', '9月', '10月', '10月', '10月', '10月', '11月', '11月', '11月', '11月'],
    '实际班级总分': [95, 92, 88, 90, 93, 91, 85, 92, 90, 90, 82, 94],
    '手机管理': [10, 9, 8, 9.5, 9, 8.5, 7.5, 9.5, 8, 8, 7, 9.5],
    '发型发饰': [10, 10, 9, 10, 10, 9.5, 8.5, 10, 10, 9.5, 8, 10],
    '校服衣着': [10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 8.5, 10]
}

# 创建DataFrame
combined_df = pd.DataFrame(data)

# 测试班级扣分风险预测功能
def test_risk_prediction(df):
    print("测试班级扣分风险预测功能...")
    
    # 检查必要的列是否存在
    required_columns = ['班级', '实际班级总分', '月份']
    for col in required_columns:
        if col not in df.columns:
            print(f"❌ 错误：数据中没有找到'{col}'列")
            return False
    
    try:
        # 计算每个班级的总分变化趋势
        risk_classes = []
        all_classes = df['班级'].unique()
        
        print(f"\n共有 {len(all_classes)} 个班级：{list(all_classes)}")
        
        for cls in all_classes:
            # 获取该班级的数据
            class_data = df[df['班级'] == cls].copy()
            
            print(f"\n处理班级：{cls}")
            print(f"数据行数：{len(class_data)}")
            print(f"原始数据：\n{class_data[['月份', '实际班级总分']]}")
            
            # 确保有足够的数据点（至少2个月份）
            if len(class_data) < 2:
                print(f"⚠️ 班级 {cls} 数据不足2个月份，跳过")
                continue
            
            # 按月份排序
            month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
            try:
                class_data['月份排序'] = class_data['月份'].map(lambda x: month_order.index(x))
                class_data = class_data.sort_values('月份排序').drop('月份排序', axis=1)
                print(f"排序后数据：\n{class_data[['月份', '实际班级总分']]}")
            except ValueError as e:
                print(f"⚠️ 班级 {cls} 月份排序错误：{e}，跳过")
                continue
            
            # 使用简单的线性回归计算趋势斜率
            # 月份转换为数值索引（0, 1, 2, ...）
            x = np.array(range(len(class_data)))
            y = np.array(class_data['实际班级总分'])
            
            print(f"x值：{x}")
            print(f"y值：{y}")
            
            # 计算斜率
            try:
                slope = np.polyfit(x, y, 1)[0]
                print(f"趋势斜率：{slope:.4f}")
            except np.linalg.LinAlgError as e:
                print(f"⚠️ 班级 {cls} 无法计算斜率：{e}，跳过")
                continue
            
            # 如果斜率为负，说明总分呈下降趋势，存在扣分风险
            if slope < 0:
                # 计算下降幅度（最后一个月与第一个月的差值）
                score_diff = y[-1] - y[0]
                
                print(f"⚠️ 班级 {cls} 存在扣分风险：斜率={slope:.4f}，总分变化={score_diff:.2f}")
                
                risk_classes.append({
                    '班级': cls,
                    '趋势斜率': slope,
                    '总分变化': score_diff,
                    '数据月份数': len(class_data),
                    '最近月份': class_data['月份'].iloc[-1]
                })
            else:
                print(f"✅ 班级 {cls} 总分趋势稳定或上升：斜率={slope:.4f}")
        
        if risk_classes:
            # 转换为DataFrame并排序（按总分下降幅度从大到小）
            risk_df = pd.DataFrame(risk_classes)
            risk_df = risk_df.sort_values('总分变化', ascending=True)
            
            print("\n📊 存在扣分风险的班级：")
            print(risk_df)
            
            # 可视化风险班级
            print("\n📈 风险班级总分变化趋势：")
            plt.figure(figsize=(10, 6))
            
            for cls in risk_df['班级']:
                class_data = df[df['班级'] == cls].copy()
                month_order = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
                class_data['月份排序'] = class_data['月份'].map(lambda x: month_order.index(x))
                class_data = class_data.sort_values('月份排序')
                
                plt.plot(class_data['月份'], class_data['实际班级总分'], marker='o', label=cls)
            
            plt.title('风险班级总分变化趋势')
            plt.xlabel('月份')
            plt.ylabel('实际班级总分')
            plt.legend()
            plt.grid(True)
            plt.savefig('risk_trend_test.png')
            print("风险趋势图已保存为 risk_trend_test.png")
            
            return True
        else:
            print("\n✅ 所有班级的总分趋势均为上升或稳定，未发现明显扣分风险。")
            return True
    
    except Exception as e:
        print(f"\n❌ 进行风险预测时出错：{str(e)}")
        import traceback
        traceback.print_exc()
        return False

# 运行测试
if __name__ == "__main__":
    success = test_risk_prediction(combined_df)
    if success:
        print("\n🎉 测试成功！班级扣分风险预测功能正常工作。")
    else:
        print("\n❌ 测试失败！班级扣分风险预测功能存在问题。")