# 批量删除指定文件

import os
import re

path = "/root/caozx/zz/good/"

cwd = os.getcwd()   # 返回当前工作目录
files = os.listdir(path)    # 返回指定路径下的文件列表
os.chdir(path)  
total = len(files)
count = 0           # 计数处理文件数

for line in files:
    try:
        print("line文件名为：" + line)
        os.chdir(path + line)
        os.system("pwd")
        cwd = os.getcwd()
        reads = os.listdir(cwd)
        for read in reads:
            if "r.txt" in line:
                os.system("rm -rf /root/caozx/zz/good/{0}/r.txt /root/caozx/zz/good/{1}/c.txt".format(line, line))
                print("======" + line + " finish======")
                count += 1
    except Exception as e:
        print(e)

print("total files: " + str(total))
print("moved files: " + str(count))