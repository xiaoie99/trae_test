"""
从设备采集回来的版本信息字符串经常有多余的空格，需要处理后再使用:

version_raw = "  Cisco IOS XE Software, Version 17.03.04  "
完成以下3步并分别打印结果:

去掉首尾空格（strip）
把字符串转成全大写（upper）
把 "17.03.04" 替换成 "17.06.01"（replace）
打印效果如下:

去掉空格: Cisco IOS XE Software, Version 17.03.04
转大写:   CISCO IOS XE SOFTWARE, VERSION 17.03.04
替换版本: Cisco IOS XE Software, Version 17.06.01
"""
version_raw = "  Cisco IOS XE Software, Version 17.03.04  "
print("去掉空格:", version_raw.strip())
print("转大写:", version_raw.upper())
print("替换版本:", version_raw.strip().replace("17.03.04", "17.06.01"))
