import requests
from bs4 import BeautifulSoup
import pandas as pd

# 网页链接
url = 'https://iftp.chinamoney.com.cn/english/bdInfo/'

# 模拟HTTP请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 发送请求
response = requests.get(url, headers=headers)
response.raise_for_status()  # 抛出异常
# 解析HTML
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find("table",{"class":"san-sheet-alternating"})
# 使用pandas的read_html来解析表格
df_list = pd.read_html(str(table))
df = df_list[0] if df_list else pd.DataFrame()  # 如果没有找到表格，则创建空DataFrame

# 筛选Bond Type=Treasury Bond且Issue Year=2023的行
df_filtered = df[(df['Bond Type'] == 'Treasury Bond') & (df['Issue Year'] == 2023)]

# 确保列名正确
required_columns = ['ISIN', 'Bond Code', 'Issuer', 'Bond Type', 'Issue Date', 'Latest Rating']
df_filtered = df_filtered[required_columns]

# 保存到CSV文件
output_file = 'treasury.csv'
df_filtered.to_csv(output_file, index=False)

print(f'Data saved to {output_file}')