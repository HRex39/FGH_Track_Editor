# FGH_Track_Editor 
![image](https://img.shields.io/badge/author-F.Y.J.-blue.svg)
![image](https://img.shields.io/badge/author-G.X.Y.-blue.svg)
![image](https://img.shields.io/badge/author-H.C.R.-blue.svg)  

 
## 功能：  
  简单的赛道编辑可视化以及导入导出，要求输入txt格式  
  可导出地图为txt,yaml,sdf格式
  增加杂点功能，点击一次增加一次  
  data1：x坐标  
  data2：y坐标  
  data3：左右锥桶（1代表红；2代表蓝色）</br></br>
## How to use?
  将需要描点的锥桶数据放置在map文件夹中（txt格式）   
    要求格式：  
    第一列：x坐标；第二列：y坐标；第三列：锥桶颜色  
## 数据导出：
  目前数据存放在MAP_OUTPUT中，但是具体可以在main.py中更改文件保存的路径
## Windows：   
    Have Problems Now,But I don't know how to fix!  
## Linux：  
    pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple  
    pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple  
    sudo apt-get install python3-tk
    
## 效果图：
![Image text](https://raw.githubusercontent.com/HRex39/FGH_Track_Editor/master/image/Image_1.png)  
## 关于Tkinter:  
  在命令行中运行 python -m tkinter，应该会弹出一个Tk界面的窗口，  
  表明 tkinter 包已经正确安装，而且告诉你 Tcl/Tk 的版本号，  
  通过这个版本号，你就可以参考对应的 Tcl/Tk 文档了。  
