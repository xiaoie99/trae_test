"""
定义以下变量，使用 format() 打印一份格式整齐的接口状态报告:

intf1 = "Gi0/0", status1 = "up", speed1 = "1G"
intf2 = "Gi0/1", status2 = "down", speed2 = "1G"
intf3 = "Gi0/2", status3 = "up", speed3 = "10G"
打印效果如下:

接口      状态    速率
--------------------
Gi0/0     up      1G
Gi0/1     down    1G
Gi0/2     up      10G
"""
intf1, status1, speed1 = "Gi0/0", "up", "1G"
intf2, status2, speed2 = "Gi0/1", "down", "1G"
intf3, status3, speed3 = "Gi0/2", "up", "10G"

print("{:<7} {:<5} {:<4}".format("接口", "状态", "速率"))
print("-" * 20)
print("{:<9} {:<7} {:<4}".format(intf1, status1, speed1))
print("{:<9} {:<7} {:<4}".format(intf2, status2, speed2))
print("{:<9} {:<7} {:<4}".format(intf3, status3, speed3))