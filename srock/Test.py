import baostock as bs
import pandas as pd
import matplotlib.pyplot as plt

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 登陆系统
lg = bs.login()
print('login respond error_code:' + lg.error_code)
print('login respond error_msg:' + lg.error_msg)

# 获取历史K线数据
rs = bs.query_history_k_data_plus("sh.605398",
                                   "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                   start_date='2023-04-01', end_date='2024-04-22', frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:' + rs.error_code)
print('query_history_k_data_plus respond error_msg:' + rs.error_msg)

data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
print(result)

# 登出系统
bs.logout()

# 数据处理
result['date'] = pd.to_datetime(result['date'])  # 转换日期格式
result['open'] = result['open'].astype(float)  # 转换开盘价为浮点数
result['close'] = result['close'].astype(float)  # 转换收盘价为浮点数

# 绘制折线图
plt.figure(figsize=(12, 6))  # 设置图形大小
plt.plot(result['date'], result['open'], label='开盘价', marker='o', linestyle='-')  # 绘制开盘价折线图
plt.plot(result['date'], result['close'], label='收盘价', marker='x', linestyle='-')  # 绘制收盘价折线图

# 添加图表标题和图例
plt.title('新炬网络（605398）2024-03-01 至 2024-04-22 开盘价和收盘价波动', fontsize=14)
plt.xlabel('日期', fontsize=12)
plt.ylabel('价格（元）', fontsize=12)
plt.legend(fontsize=10)  # 添加图例
plt.grid(True)  # 添加网格线
plt.xticks(rotation=45)  # 旋转x轴标签，便于显示
plt.tight_layout()  # 自动调整子图参数，使之填充整个图像区域
plt.show()