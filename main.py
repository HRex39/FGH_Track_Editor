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
map_load_path = 'map/map.txt'
load_map_yaml = 'map/acceleration.yaml'

# 文件导出路径
txt_output_path = 'MAP_OUTPUT/output.txt'
yaml_output_path = 'MAP_OUTPUT/output.yaml'
sdf_output_path = 'MAP_OUTPUT/output.sdf'

# 检查重复的点
def check(self, position_1, position_2):
    for i in range(len(self.data1)):
        if ((position_1 - self.data1[i])**2 + (position_2 - self.data2[i])**2 <= 0.0):
            print("Pay attention, there are extremely close points. \nDelete one automatically.")
            print(str(position_1)+' '+str(position_2))
            print(str(self.data1[i])+' '+str(self.data2[i]))
            print()
            return False

    return True


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
        self.root.title('FGH_TRACK_EDITOR')
        self.root.geometry("+900+100")
        self.label = Label(self.root)
        self.label['text'] = '\nFGH_TRACK_EDITOR'
        #####
        self.Add_yaml = Button(self.root, text=' 从yaml导入地图 ', command=self.Add_yaml)
        ####
        self.CheckButtonVar = IntVar()
        self.radio1 = Checkbutton(self.root, text="显示次序", variable=self.CheckButtonVar)
        ###
        self.Check = Button(self.root, text='查看锥桶位置', command=self.Matlab_Check)
        self.Txt = Text(self.root, height=4, width=40)
        #####
        self.Add_blue = Button(self.root, text='  鼠标添加blue  ', command=self.Matlab_Add_Blue)
        #####
        self.Add_red = Button(self.root, text='  鼠标添加red   ', command=self.Matlab_Add_Red)
        #####
        self.Input_x_label = Label(self.root, text='锥桶X坐标: ')
        self.Input_y_label = Label(self.root, text='锥桶Y坐标: ')
        self.Input_type_label = Label(self.root, text='锥桶颜色(red or blue): ')
        self.Input_index_label = Label(self.root, text='锥桶下标(int): ')
        self.Input_x = Entry(self.root)
        self.Input_y = Entry(self.root)
        self.Input_type = Entry(self.root)
        self.Input_index = Entry(self.root)
        self.Add = Button(self.root, text='  坐标添加  ', command=self.Matlab_Add)
        #####
        self.Add_mix = Button(self.root, text='   添加杂点   ', command=self.Mix_cone)
        #####
        self.Delete = Button(self.root, text='  删除锥桶  ', command=self.Matlab_Delete)
        #####
        self.Refresh = Button(self.root, text='    刷新    ', command=self.Refresh)
        #####
        self.Out = Button(self.root, text=' 导出为txt文件 ', command=self.Out_Data)
        #####
        self.Test = Button(self.root, text='导出为yaml和sdf文件', command=self.test)
        #####
        self.b = Button(self.root, text='退出', command=self.All_Close)
        #####
        self.Help = Label(self.root)
        self.Help['text'] += '1.程序默认加载txt文件地图\n'
        self.Help['text'] += '2.若出现卡死，请刷新或重启程序\n'
        self.Help['text'] += 'Designed by FGH'
        #####
        self.label.grid(row=0, column=0)
        self.Add_yaml.grid(row=1, column=0)
        self.Check.grid(row=2, column=0)
        self.radio1.grid(row=2, sticky=W)
        self.Txt.grid(row=3, column=0)
        self.Add_red.grid(row=4, sticky=W)
        self.Add_blue.grid(row=4, sticky=E)
        self.Input_x_label.grid(row=5, sticky=W)
        self.Input_x.grid(row=5, sticky=E+S+N)
        self.Input_y_label.grid(row=6, sticky=W)
        self.Input_y.grid(row=6, sticky=E+S+N)
        self.Input_type_label.grid(row=7, sticky=W)
        self.Input_type.grid(row=7,sticky=E+S+N)
        self.Input_index_label.grid(row=8, sticky=W)
        self.Input_index.grid(row=8, sticky=E+S+N)
        self.Add.grid(row=9, sticky=W+E+S+N)
        self.Delete.grid(row=10, sticky=W)
        self.Refresh.grid(row=10)
        self.Add_mix.grid(row=10,sticky=E)
        self.Out.grid(row=11, sticky=W)
        self.Test.grid(row=11, sticky=E)
        self.b.grid(row=12, sticky=W+E+S+N)
        self.Help.grid(row=13, sticky=W+E+S+N)
    
        

    # 导入txt
    def Load_Data(self):
        data = np.loadtxt(map_load_path)  # 将文件中数据加载到data数组里
        for tmp_data in data:
            if(check(self, tmp_data[0], tmp_data[1])):
                self.data1.append(tmp_data[0])
                self.data2.append(tmp_data[1])
                self.data3.append(int(tmp_data[2]))
            
    # 导入yaml
    def Add_yaml(self):
        self.data1.clear()
        self.data2.clear()
        self.data3.clear()

        with open(load_map_yaml, 'r') as f:
            test = f.readlines()
            sum = len(test)
            i = 0
            flag = 0 # 1为left 2为right
            while (i < sum):
                # print(i)
                if test[i][0] == 'c':
                    if test[i][:10] == 'cones_left':
                        flag = 1
                        i += 1
                        continue
                        
                    elif test[i][:10] == 'cones_right':
                        i += 1
                        flag = 2
                        continue
                    else:
                        flag = 0
                        i += 1
                        continue
        
                if test[i][0] != '-' and test[i][0] != ' ':
                    i += 1
                    flag = 0
                    continue

                if flag == 1:
                    #add_left(i)
                    #print(float(test[i][3:]))
                    if(check(self, float(test[i][3:]), float(test[i+1][3:]))):
                        self.data1.append(float(test[i][3:]))
                        self.data2.append(float(test[i+1][3:]))
                        self.data3.append(1)
                        i += 2
                        continue

                elif flag == 2:
                    #add_right(i)
                    if(check(self, float(test[i][3:]), float(test[i+1][3:]))):
                        self.data1.append(float(test[i][3:]))
                        self.data2.append(float(test[i+1][3:]))
                        self.data3.append(2)
                        i += 2
                        continue
                elif flag == 0:
                    i += 1

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
        if (self.CheckButtonVar.get() == 1):
            plt.plot(self.data1,self.data2)
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
            min_distance_1 = 999
            min_index_1 = -1
            min_distance_2 = 999
            min_index_2 = -2
            distance_1_2 = -1
            cosine_C = 1

            for i in range(len(self.data1)): # find the blue closest
                if(self.data3[i] == 1 and (m - self.data1[i])**2 + (n - self.data2[i])**2 <= min_distance_1):
                    min_distance_1 = (m - self.data1[i])**2 + (n - self.data2[i])**2
                    min_index_1 = i

            for i in range(len(self.data1)): # find the blue second closest, law of cosines to garantee one point left and another right
                if(self.data3[i] == 1 and i != min_index_1 and (m - self.data1[i])**2 + (n - self.data2[i])**2 <= min_distance_2):
                    distance_1_2 = (m - self.data1[min_index_1])**2 + (n - self.data2[min_index_1])**2
                    cosine_C = (min_distance_1 + (m - self.data1[i])**2 + (n - self.data2[i])**2 - distance_1_2) / (2 * cmath.sqrt(min_distance_1 * ((m - self.data1[i])**2 + (n - self.data2[i])**2)))
                    if(cosine_C <= 0.5):
                        min_distance_2 = (m - self.data1[i])**2 + (n - self.data2[i])**2
                        min_index_2 = i
            
            # judge cross lap, this will not work if the index in map.txt is not in order (the first cone is not [0], for example.)
            index_larger = max(min_index_1,min_index_2)
            index_smaller = min(min_index_1,min_index_2)
            if(index_smaller == 0 and index_larger > 10): # believed to have passed the starting point
                index_larger = 0
            self.data1.insert(index_larger,m)
            self.data2.insert(index_larger,n)
            self.data3.insert(index_larger,1)
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
            min_distance_1 = 999
            min_index_1 = -1
            min_distance_2 = 999
            min_index_2 = -2

            for i in range(len(self.data1)): # find the red closest
                if(self.data3[i] == 2 and (m - self.data1[i])**2 + (n - self.data2[i])**2 <= min_distance_1):
                    min_distance_1 = (m - self.data1[i])**2 + (n - self.data2[i])**2
                    min_index_1 = i

            for i in range(len(self.data1)): # find the red second closest
                if(self.data3[i] == 2 and i != min_index_1 and (m - self.data1[i])**2 + (n - self.data2[i])**2 <= min_distance_2):
                    min_distance_2 = (m - self.data1[i])**2 + (n - self.data2[i])**2
                    min_index_2 = i
            
            # judge cross lap, this will not work if the index in map.txt is not in order (the first cone is not [0], for example.)
            index_larger = max(min_index_1,min_index_2)
            index_smaller = min(min_index_1,min_index_2)
            if(index_smaller == 0 and index_larger > 10): # believed to have passed the starting point
                index_larger = 0
            self.data1.insert(index_larger,m)
            self.data2.insert(index_larger,n)
            self.data3.insert(index_larger,2)
            plt.clf()

    # 添加自定义坐标锥筒
    def Matlab_Add(self):
        self.Matlab_Drawing()
        try:
            m = float(self.Input_x.get())
            n = float(self.Input_y.get())
            cone_color = self.Input_type.get()
            cone_index = int(self.Input_index.get())
        except ValueError or UnboundLocalError:
            self.root = Tk()
            self.Output_Check = Button(self.root, text='\n格式有误\n', command=self.root.destroy)
            self.Output_Check.pack()
        # 避免重复添加
        for i in range(len(self.data3)):
            if m == self.data1[i] and n == self.data2[i]:
                return

        if cone_color == 'red':
            plt.scatter(m, n, color='red', marker='.')
            self.data1.insert(cone_index,m)
            self.data2.insert(cone_index,n)
            self.data3.insert(cone_index,2)
        else:
            plt.scatter(m, n, color='blue', marker='.')
            self.data1.insert(cone_index,m)
            self.data2.insert(cone_index,n)
            self.data3.insert(cone_index,1)
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
                        'end', '锥桶位置是：' + 'x = ' + str(self.data1[i]) + '\n' + 'y = ' + str(self.data2[i]) + '\n' + 'cone_color = ' + color + '\n' + 'cone_index = ' + str(i) + '\n')
                    break
                else:
                    self.Txt.delete(1.0, 'end')
                    self.Txt.insert('end','此处无锥桶\n' + '你点击的位置是：\n' + str(m) + '\n' + str(n) + '\n')
                    #TODO:在输入框中显示坐标

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
