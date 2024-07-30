import re
from datetime import datetime


def reg_search(text, regex_list):
    # 定义一个内部函数来解析日期字符串
    def parse_date(date_str):
        year, month, day = map(int, re.findall(r'(\d+)', date_str))
        return datetime(year, month, day).strftime('%Y-%m-%d')


    patterns = {}
    for key, pattern_str in regex_list.items():
            if key == '标的证券':
                patterns[key] = r'股票代码：(\S+)'
            elif key == '换股期限':
                patterns[key] = r'换股期限自.*?至(.*?)止，即 (.*?) 至 (.*?) 止。'


    results = {key: [] for key in regex_list.keys()}

    # 应用正则表达式并收集结果
    for key, pattern in patterns.items():
        if key == '换股期限':
            matches = re.findall(pattern, text)
            if matches:
                start_dates = [parse_date(match[1]) for match in matches]
                end_dates = [parse_date(match[2]) for match in matches]
                results[key] = [start_dates, end_dates]


        else:
            # 对于其他情况，直接匹配并收集结果
            matches = re.findall(pattern, text)
            results[key] = matches

    if '换股期限' in results:
        results['换股期限'] = [f'{start}-{end}' for start, end in zip(results['换股期限'][0], results['换股期限'][1])]

    return [results]  # 返回列表


# 示例使用
text = '''  
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。  
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2 日至 2027 年 6 月 1 日止。  
'''
regex_list = {
    '标的证券':  '600900.SH',
    '换股期限': ['2023-06-02', '2027-06-01']
}

print(reg_search(text, regex_list))