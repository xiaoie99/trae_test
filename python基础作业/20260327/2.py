port_list = ['eth 1/101/1/42','eth 1/101/1/26','eth 1/101/1/23','eth 1/101/1/7','eth 1/101/2/46','eth 1/101/1/34','eth 1/101/1/18','eth 1/101/1/13','eth 1/101/1/32','eth 1/101/1/25','eth 1/101/1/45','eth 1/101/2/8']

print(sorted(port_list, key=lambda x: [int(i) for i in x.split()[1].split('/')]))

# 第二种方法，使用正则表达式提取数字，但不是一句话
# import re
# print(sorted(port_list, key=lambda x: [int(i) for i in re.findall(r'\d+', x)]))