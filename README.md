# FGH_Track_Editor 
![image](https://img.shields.io/badge/author-XavierG_Cons-orange.svg)
![image](https://img.shields.io/badge/author-HRex39-orange.svg)
![image](https://img.shields.io/badge/tester-Spencer1909-orange.svg)  
![image](https://img.shields.io/badge/python-3.5.2√-blue.svg)
![image](https://img.shields.io/badge/python-3.6.6√-blue.svg)
![image](https://img.shields.io/badge/python-3.7.4√-blue.svg)
![image](https://img.shields.io/badge/python-3.8.2√-blue.svg)  
![image](https://img.shields.io/badge/anaconda-python×-red.svg)  
## 功能：  
  简单的赛道编辑可视化以及导入导出，要求输入txt格式  
  可导出地图为txt,yaml,sdf格式
  增加杂点功能，点击一次增加一次  
  data1：x坐标  
  data2：y坐标  
  data3：左右锥桶（1代表蓝色；2代表红色）</br></br>
## How to use?
  将需要描点的锥桶数据放置在    map.txt    中  
    要求格式：  
    第一列：x坐标；第二列：y坐标；第三列：锥桶颜色</br></br>
## Windows：   
    Python3就能跑啦   
    pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple  
    pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple  
  
## Linux：  
    除了上面两条指令之外呢，还要附加一条  
    sudo apt-get install python3-tk
    
## 效果图：
![Image text](https://raw.githubusercontent.com/HRex39/FGH_Track_Editor/master/image/Image_1.png)  
## 关于Tkinter:  
  在命令行中运行 python -m tkinter，应该会弹出一个Tk界面的窗口，  
  表明 tkinter 包已经正确安装，而且告诉你 Tcl/Tk 的版本号，  
  通过这个版本号，你就可以参考对应的 Tcl/Tk 文档了。  
