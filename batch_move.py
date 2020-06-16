# 批量移动文件，筛选符合条件的文件，移动到指定文件夹

#1.
#遍历目录中的所有文件
#跳过压缩包
#进入文件
#  遍历文件中的所有文件，查看是否有Output文件
#      如果没有，继续遍历目录
#      如果有，查看output是否为空
#          如果为空，继续遍历目录
#          如果不为空，记录文件名

#测试代码
import re
import os

path = "/root/caozx/zz/mm2"
files = os.listdir(path)	#获取目录下所有文件
os.chdir(path)  	#切换当前工作目录

for line in files:
	if ".gz" in line: 
		continue
    else:
        os.chdir("/root/caozx/zz/mm2/"+line) 
        #os.system("cd /root/caozx/zz/mm2/{0}".format(line))
        cwd = os.getcwd()
        reads = os.listdir(cwd)
        for read in reads:
            if "output.txt" in read: 
                size = os.path.getsize("output.txt")
                if size:
                    try:
                        os.system("mv /root/caozx/zz/mm2/{0} ../../good/".format(line))
                        print("------" + line + " finish------")
                    except:
                        os.system("echo /root/caozx/zz/mm2/{0} >> ../../error.txt".format(line))
                        print("------" + line + " error------")
            else:
                continue


#2.
#筛选包含特征矩阵结果的文件
#遍历目录中的所有文件
#进入文件
#  遍历文件中的所有文件，查看是否有c.txt 和 r.txt
#      如果没有，继续遍历目录
#      如果有，移动文件

#测试代码
import re
import os

path = "/root/caozx/zz/good/"
files = os.listdir(path)	#获取目录下所有文件
os.chdir(path)  	# 切换当前工作目录
total = len(files)
count = 0           # 计数移动文件数
err = 0

for line in files:
    os.chdir(path + line) #进入文件夹
    t1 = os.path.exists("/root/caozx/zz/good/{0}/c.txt".format(line))
    t2 = os.path.exists("/root/caozx/zz/good/{0}/r.txt".format(line))
    if t1 & t2:
        try:
            os.system("mv /root/caozx/zz/good/{0} ../../file/".format(line))
            count += 1
            print("------" + line + " finish------")
            #break
        except:
            os.system("echo {0} >> ../../errfeature.txt".format(line))
            err += 1
    else:
        continue

print("total files: " + str(total))
print("moved files: " + str(count))
print("error files: " + str(err))