# 地图编辑器.py
# 使用Tab来缩进（坏习惯。。。）
import time
import sys
import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import random
import cmath

# 设置杂点倍数
multiple = 0.1

# 文件导入路径
map_load_path = 'map\map.txt'

# 文件导出路径
txt_output_path = 'MAP_OUTPUT\output.txt'
yaml_output_path = 'MAP_OUTPUT\output.yaml'
sdf_output_path = 'MAP_OUTPUT\output.sdf'


class TrackEditor:
    def __init__(self):
        # 按键锁
        self.in_loop = 0  # 开始是0 判断，防止连点两个功能卡死
        self.data1 = []
        self.data2 = []
        self.data3 = []
        #####
        self.Load_Data()
        self.root = Tk()
        self.root.title('赛道编辑器')
        self.root.geometry("+900+100")
        self.label = Label(self.root)
        self.label['text'] = '\n赛道编辑器\n\n'
        self.label.pack()
        #####
        self.Check = Button(self.root, text='查看锥桶位置', command=self.Matlab_Check)
        self.Txt = Text(self.root, height=3, width=20)
        self.Check.pack()
        self.Txt.pack()
        #####
        self.Add_blue = Button(self.root, text='  鼠标添加blue  ', command=self.Matlab_Add_Blue)
        self.Add_blue.pack()
        #####
        self.Add_red = Button(self.root, text='  鼠标添加red   ', command=self.Matlab_Add_Red)
        self.Add_red.pack()
        #####
        self.Input_x = Entry(self.root)
        self.Input_y = Entry(self.root)
        self.Input_type = Entry(self.root)
        self.Add = Button(self.root, text='  坐标添加  ', command=self.Matlab_Add)
        self.Input_x.pack()
        self.Input_y.pack()
        self.Input_type.pack()
        self.Add.pack()
        #####
        self.Add_mix = Button(self.root, text='   添加杂点   ', command=self.Mix_cone)
        self.Add_mix.pack()
        #####
        self.Delete = Button(self.root, text='  删除锥桶  ', command=self.Matlab_Delete)
        self.Delete.pack()
        #####
        self.Refresh = Button(self.root, text='    刷新    ', command=self.Refresh)
        self.Refresh.pack()
        #####
        self.Out = Button(self.root, text=' 导出为txt文件 ', command=self.Out_Data)
        self.Out.pack()
        #####
        self.Test = Button(self.root, text='导出为yaml和sdf文件    ', command=self.test)
        self.Test.pack()
        #####
        self.b = Button(self.root, text='    退出    ', command=self.All_Close)
        self.b.pack()
        #####
        self.Help = Label(self.root)
        self.Help['text'] = '1.输入x坐标, y坐标, red或blue 来添加自定义锥筒\n'
        self.Help['text'] += '2.在使用其他功能前请先刷新，以免报错\n'
        self.Help['text'] += '3.当出现卡死的情况，果断关闭plot，一切就又好起来了（确信）\n'
        self.Help['text'] += 'Designed by FGH'
        self.Help.pack()
        #####

    # 导入txt
    def Load_Data(self):
        data = np.loadtxt(map_load_path)  # 将文件中数据加载到data数组里
        for tmp_data in data:
            self.data1.append(tmp_data[0])
            self.data2.append(tmp_data[1])
            self.data3.append(int(tmp_data[2]))

    # 添加杂点
    def Mix_cone(self):
        leftlx = {}
        leftly = {}
        rightrx = {}
        rightry = {}
        sum_left = 0
        sum_right = 0
        for i in range(len(self.data1)):
            if self.data3[i] == 1:
                sum_left = sum_left + 1
                leftlx[sum_left] = self.data1[i]
                leftly[sum_left] = self.data2[i]
            else:
                if self.data3[i] == 2:
                    sum_right = sum_right + 1
                    rightrx[sum_right] = self.data1[i]
                    rightry[sum_right] = self.data2[i]

        sum_mix = int((sum_left+sum_right)/2*multiple)
        tot = sum_mix
        while tot > 0:
            tot = tot-1
            mix_a = random.randint(0, 1000)/10
            mix_b = random.randint(0, 1000)/10
            t = random.randint(0, 4)
            if t == 0:
                mix_a = mix_a*-1
            if t == 1:
                mix_a = mix_a*-1
                mix_b = mix_b*-1
            if t == 2:
                mix_b = mix_b*-1

            # is_ok()
            # 必须与所有锥桶距离大于10，与至少一个锥桶距离小于20
            flag = 0
            flag_f = 0
            for j in range(sum_left):
                if ((leftlx[j+1]-mix_a)*(leftlx[j+1]-mix_a)+(leftly[j+1]-mix_b)*(leftly[j+1]-mix_b))**0.5 <= 10:
                    flag = 1
                if ((leftlx[j+1]-mix_a)*(leftlx[j+1]-mix_a)+(leftly[j+1]-mix_b)*(leftly[j+1]-mix_b))**0.5 <= 20:
                    flag_f = 1
            for j in range(sum_right):
                if ((rightrx[j+1]-mix_a)*(rightrx[j+1]-mix_a)+(rightry[j+1]-mix_b)*(rightry[j+1]-mix_b))**0.5 <= 10:
                    flag = 1
                if ((rightrx[j+1]-mix_a)*(rightrx[j+1]-mix_a)+(rightry[j+1]-mix_b)*(rightry[j+1]-mix_b))**0.5 <= 20:
                    flag_f = 1

            if flag == 0 and flag_f == 1:
                if tot % 2 == 1:
                    plt.scatter(mix_a, mix_b, color='blue', marker='.')
                    self.data1.append(mix_a)
                    self.data2.append(mix_b)
                    self.data3.append(1)
                    plt.clf()
                else:
                    plt.scatter(mix_a, mix_b, color='red', marker='.')
                    self.data1.append(mix_a)
                    self.data2.append(mix_b)
                    self.data3.append(2)
                    plt.clf()
            else:
                tot = tot+1

        print(str("Mix cones is "+str(sum_mix)+'\n'))
        self.Refresh_Loop()
        while 1:
            self.Matlab_Drawing()
            try:
                [(m, n)] = plt.ginput(1)
            except ValueError:
                time.sleep(0.1)
                continue
            for i in range(len(self.data3)):
                if abs(self.data1[i] - m) <= 0.5 and abs(self.data2[i] - n) <= 0.5:
                    if self.data3[i] == 1:
                        color = 'blue'
                    else:
                        color = 'red'
                    self.Txt.delete(1.0, 'end')
                    self.Txt.insert(
                        'end', 'x=' + str(self.data1[i]) + '\n' + 'y=' + str(self.data2[i]) + '\n' + color)
                    break
            plt.clf()
        '''plt.scatter(m, n, color='blue', marker='.')
        self.data1.append(m)
        self.data2.append(n)
        self.data3.append(1)
        plt.clf()'''

    # 导出为yaml和sdf文件
    def test(self):
        # yaml:
        with open(yaml_output_path, 'w') as f:
            leftlx = {}
            leftly = {}
            rightrx = {}
            rightry = {}
            sum_left = 0
            sum_right = 0
            for i in range(len(self.data1)):
                if self.data3[i] == 1:
                    sum_left = sum_left + 1
                    leftlx[sum_left] = self.data1[i]
                    leftly[sum_left] = self.data2[i]
                else:
                    sum_right = sum_right + 1
                    rightrx[sum_right] = self.data1[i]
                    rightry[sum_right] = self.data2[i]

            # left_cones
            f.write(str("cones_left:" + '\n'))
            for i in range(sum_left):
                f.write(str("- - " + str(leftlx[i + 1]) + '\n'))
                f.write(str("  - " + str(leftly[i + 1]) + '\n'))

            # right_cones
            f.write(str("cones_right:" + '\n'))
            for i in range(sum_right):
                f.write(str("- - " + str(rightrx[i + 1]) + '\n'))
                f.write(str("  - " + str(rightry[i + 1]) + '\n'))

            f.write(str("starting_pose_front_wing:" + '\n'))
            f.write(str("- 0.0" + '\n'))
            f.write(str("- 0.0" + '\n'))
            f.write(str("- 0.0" + '\n'))
            f.write(str("tk_device:" + '\n'))
            f.write(str("- - 0" + '\n'))
            f.write(str("  - 3" + '\n'))
            f.write(str("- - 0" + '\n'))
            f.write(str("  - -3" + '\n'))
            f.close()

            # sdf文件
        with open(sdf_output_path, 'w') as f:
            f.write(str("<?xml version='1.0' encoding='UTF-8'?>" + '\n'))
            f.write(str("<sdf version=\"1.4\">" + '\n'))
            f.write(str("<model name=\"some track\">" + '\n'))

            # left_cones
            for i in range(sum_left):
                f.write(str("    <include>" + '\n'))
                f.write(str("      <uri>model://fssim_gazebo/models/cone_blue</uri>" + '\n'))
                f.write(str("        <pose> " + str(leftlx[i + 1]) + str(leftly[i + 1]) + " 0 0 0 0 </pose>" + '\n'))
                f.write(str("      <name>cone_left</name>" + '\n'))
                f.write(str("    </include>" + '\n'))

            # right_cones
            for i in range(sum_right):
                f.write(str("    <include>" + '\n'))
                f.write(str("      <uri>model://fssim_gazebo/models/cone_yellow</uri>" + '\n'))
                f.write(str("        <pose> " + str(rightrx[i + 1]) + str(rightry[i + 1]) + " 0 0 0 0 </pose>" + '\n'))
                f.write(str("      <name>cone_right</name>" + '\n'))
                f.write(str("    </include>" + '\n'))

            f.write(str("    <include>" + '\n'))
            f.write(str("      <uri>model://fssim_gazebo/models/time_keeping</uri>" + '\n'))
            f.write(str("        <pose> 0.0 3.0 0 0 0 0 </pose>" + '\n'))
            f.write(str("      <name>tk_device_0</name>" + '\n'))
            f.write(str("    </include>" + '\n'))

            f.write(str("    <include>" + '\n'))
            f.write(str("      <uri>model://fssim_gazebo/models/time_keeping</uri>" + '\n'))
            f.write(str("        <pose> 0.0 -3.0 0 0 0 0 </pose>" + '\n'))
            f.write(str("      <name>tk_device_1</name>" + '\n'))
            f.write(str("    </include>" + '\n'))

            f.write(str("  </model>" + '\n'))
            f.write(str("</sdf>" + '\n'))
            f.close()
            # f.write(str(str(i)+'\n'))
            # f.write(str(sum_left))
            # f.write(str(str(i) + '\n'))
            # f.write(str(self.data1[i]) + ' ' + str(self.data2[i]) + ' ' + str(int(self.data3[i])) + '\n')

        # 给个信
        self.root = Tk()
        self.Test = Button(self.root, text='\n导出成功\n', command=self.root.destroy)
        self.Test.pack()

    # 绘图函数
    def Matlab_Drawing(self):
        for i in range(len(self.data3)):
            if self.data3[i] == 1:
                plt.scatter(self.data1[i], self.data2[i],
                            color='blue', marker='.')
            else:
                plt.scatter(self.data1[i], self.data2[i],
                            color='red', marker='.')

    # 绘图函数的删除功能
    def Matlab_Delete(self):
        self.Refresh_Loop()
        while 1:
            self.Matlab_Drawing()
            try:
                [(m, n)] = plt.ginput(1)
            except ValueError:
                time.sleep(0.01)
                [(m, n)] = plt.ginput(1)
            for i in range(len(self.data3)):
                if abs(self.data1[i] - m) <= 0.5 and abs(self.data2[i] - n) <= 0.5:
                    del self.data1[i]
                    del self.data2[i]
                    del self.data3[i]
                    break
            plt.clf()

    # 绘图函数的增加功能, 蓝色锥桶增加函数
    def Matlab_Add_Blue(self):
        self.Refresh_Loop()
        while (1):
            self.Matlab_Drawing()
            try:
                [(m, n)] = plt.ginput(1)
            except ValueError:
                time.sleep(0.01)
                [(m, n)] = plt.ginput(1)
            plt.scatter(m, n, color='blue', marker='.')
            self.data1.append(m)
            self.data2.append(n)
            self.data3.append(1)
            plt.clf()

    # 绘图函数的增加功能, 红色锥桶增加函数
    def Matlab_Add_Red(self):
        self.Refresh_Loop()
        while (1):
            self.Matlab_Drawing()
            try:
                [(m, n)] = plt.ginput(1)
            except ValueError:
                time.sleep(0.01)
                [(m, n)] = plt.ginput(1)
            plt.scatter(m, n, color='red', marker='.')
            self.data1.append(m)
            self.data2.append(n)
            self.data3.append(2)
            plt.clf()

    # 添加自定义坐标锥筒
    def Matlab_Add(self):
        self.Matlab_Drawing()
        try:
            m = float(self.Input_x.get())
            n = float(self.Input_y.get())
        except ValueError or UnboundLocalError:
            self.root = Tk()
            self.Output_Check = Button(self.root, text='\n格式有误\n', command=self.root.destroy)
            self.Output_Check.pack()
        # 避免重复添加
        for i in range(len(self.data3)):
            if m == self.data1[i] and n == self.data2[i]:
                return
        if self.Input_type.get() == 'red':
            plt.scatter(m, n, color='red', marker='.')
            self.data1.append(m)
            self.data2.append(n)
            self.data3.append(2)
        else:
            plt.scatter(m, n, color='blue', marker='.')
            self.data1.append(m)
            self.data2.append(n)
            self.data3.append(1)
        plt.clf()
        self.Matlab_Drawing()
        plt.show()

    # 绘图函数的查看功能
    def Matlab_Check(self):
        self.Refresh_Loop()
        while (1):
            self.Matlab_Drawing()
            try:
                [(m, n)] = plt.ginput(1)
            except ValueError:
                time.sleep(0.1)
                continue
            for i in range(len(self.data3)):
                if abs(self.data1[i] - m) <= 0.5 and abs(self.data2[i] - n) <= 0.5:
                    if self.data3[i] == 1:
                        color = 'blue'
                    else:
                        color = 'red'
                    self.Txt.delete(1.0, 'end')
                    self.Txt.insert(
                        'end', 'x=' + str(self.data1[i]) + '\n' + 'y=' + str(self.data2[i]) + '\n' + color)
                    break
            plt.clf()

    # 刷新
    def Refresh_Loop(self):
        plt.close()
        self.in_loop = 0
        self.Matlab_Drawing()

    def Refresh(self):
        plt.close()
        self.in_loop = 0
        self.Matlab_Drawing()
        plt.show()

    # 彻底退出
    def All_Close(self):
        plt.close()
        while (1):
            self.root.quit()
            self.root.destroy()

    # 导出
    def Out_Data(self):
        with open(txt_output_path, 'w') as f:
            for i in range(len(self.data1)):
                f.write(str(self.data1[i]) + ' ' + str(self.data2[i]) + ' ' + str(int(self.data3[i])) + '\n')
            f.close()
        # 给个信
        self.root = Tk()
        self.Output_Check = Button(self.root, text='\n导出成功\n', command=self.root.destroy)
        self.Output_Check.pack()


# 主函数
def main():
    a = TrackEditor()
    a.root.mainloop()


# 执行机构
if __name__ == "__main__":
    main()
