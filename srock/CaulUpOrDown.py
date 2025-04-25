import baostock as bs
import pandas as pd
from datetime import datetime, timedelta

code = "sh.605398"

# 登陆系统
lg = bs.login()
print('login respond error_code:' + lg.error_code)
print('login respond error_msg:' + lg.error_msg)

# 计算最近十二个月的起始日期
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

# 获取历史K线数据
rs = bs.query_history_k_data_plus(code,"date,code,close",start_date=start_date, end_date=end_date, frequency="d", adjustflag="3")
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
result['close'] = result['close'].astype(float)  # 转换收盘价为浮点数
result = result.sort_values(by='date')  # 按日期排序

# 计算涨跌
result['变化'] = result['close'] > result['close'].shift(1)  # 比较当天收盘价和前一天收盘价
result['变化'] = result['变化'].map({True: '涨', False: '跌'})  # 标记涨跌

# 按月统计涨跌天数
result['月份'] = result['date'].dt.to_period('M')  # 添加月份列
monthly_summary = result.groupby('月份')['变化'].value_counts().unstack(fill_value=0)


if code == 'sh.600567':
    print("***************山鹰国际（600567）2024-04 至 2025-04 涨跌变化表***************")
else:
    print("***************新炬网络（605398）2024-04 至 2025-04 涨跌变化表***************")

# 输出结果
print(monthly_summary)