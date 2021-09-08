
把yolo格式的数据集转换成VOC格式
--------
先将.txt文件与图片文件分开，再进行合适转换


```python
#建立文件夹，预备存放图片，txt与xml文件。
!mkdir -p VOCData/Annotations/
!mkdir -p VOCData/images/
!mkdir -p yolo/
```


```python
txtPath='Database1'
xmlPath='VOCData/Annotations'
picPath='Database1'
```


```python
#分离.txt文件到yolo路径下
import os
import shutil
import sys
import glob

file_type = ".txt" #文件后缀
from_path = 'Database1'  #源文件路径
to_path = 'yolo'   #要复制的目标路径



from_path_list = glob.glob(from_path + '/*' + file_type)
total = len(from_path_list) # 要复制的文件总数，视情况改
print('复制文件数：',total)

i = 0
interval = 10 # 打算每隔5%变化一次，视需求改
interval_num = int(total / (100 / interval)) 
# 遍历路径内的文件
for root , dirs, files in os.walk(from_path):
    for name in files:
        if name.endswith(file_type): # 只复制特定类型文件
            # print (os.path.join(root, name))
            source = os.path.join(root, name)
            target = os.path.join(to_path, name)
            try:
                shutil.copy(source, target)
            except:
                print("Copy %s failed!" % name)
            
            # 每隔5%刷新一次屏幕显示的进度百分比
            i += 1
            print(from_path_list)
            if (i % interval_num == 0):
                sys.stdout.write("Copy progress: %d%%   \r" % (i / interval_num * interval))
                sys.stdout.flush()

                

```


```python
#分离图片到VOCData/images路径下
import os
import shutil
import sys
import glob

file_type = ".jpg" #文件后缀
from_path = 'Database1'  #源文件路径
to_path = 'VOCData/images'   #要复制的目标路径



from_path_list = glob.glob(from_path + '/*' + file_type)
total = len(from_path_list) # 要复制的文件总数，视情况改
print('复制文件数：',total)

i = 0
interval = 10 # 打算每隔5%变化一次，视需求改
interval_num = int(total / (100 / interval)) 
# 遍历路径内的文件
for root , dirs, files in os.walk(from_path):
    for name in files:
        if name.endswith(file_type): # 只复制特定类型文件
            # print (os.path.join(root, name))
            source = os.path.join(root, name)
            target = os.path.join(to_path, name)
            try:
                shutil.copy(source, target)
            except:
                print("Copy %s failed!" % name)
            
            # 每隔5%刷新一次屏幕显示的进度百分比
            i += 1
            print(from_path_list)
            if (i % interval_num == 0):
                sys.stdout.write("Copy progress: %d%%   \r" % (i / interval_num * interval))
                sys.stdout.flush()

                

```


```python
#进行格式转换，并把xml文件存到VOCData/Annotations路径下
from xml.dom.minidom import Document
import os
import cv2
import sys


def makexml(txtPath,xmlPath,picPath): #读取txt路径，xml保存路径，数据集图片所在路径
        files_len = get_files_list_len(txtPath)
        print(files_len)

        dict = {'0': "UVI"}#字典对类型进行转换，分的种类越多，这里的字典越多
        files = os.listdir(txtPath)
        x = 0
        for i, name in enumerate(files):


          txtFile=open(txtPath+ '/'+name)
          txtList = txtFile.readlines()
              
          if len(txtList)==0:
              file_name=picPath+ '/'+name[0:-4]+".jpg"
              if os.path.exists(file_name):
                os.remove(file_name)
                print('成功删除文件:', file_name)
              else:
                print('未找到此文件:', file_name)
              continue
          print(len(txtList))
          try:
            img = cv2.imread(picPath+ '/'+name[0:-4]+".jpg")
            print(txtPath+ '/'+name+".jpg")
            Pheight,Pwidth,Pdepth=img.shape
          except:
            continue
          xmlBuilder = Document()
          annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
          xmlBuilder.appendChild(annotation)
          
          for i in txtList:
             oneline = i.strip().split(" ")
             '''print(i)
             if len(i) ==0:
                 continue
             print("end")'''
             folder = xmlBuilder.createElement("folder")#folder标签
             folderContent = xmlBuilder.createTextNode("VOC2007")
             folder.appendChild(folderContent)
             annotation.appendChild(folder)

             filename = xmlBuilder.createElement("filename")#filename标签
             filenameContent = xmlBuilder.createTextNode(name[0:-4]+".jpg")
             filename.appendChild(filenameContent)
             annotation.appendChild(filename)

             size = xmlBuilder.createElement("size")  # size标签
             width = xmlBuilder.createElement("width")  # size子标签width
             widthContent = xmlBuilder.createTextNode(str(Pwidth))
             width.appendChild(widthContent)
             size.appendChild(width)
             height = xmlBuilder.createElement("height")  # size子标签height
             heightContent = xmlBuilder.createTextNode(str(Pheight))
             height.appendChild(heightContent)
             size.appendChild(height)
             depth = xmlBuilder.createElement("depth")  # size子标签depth
             depthContent = xmlBuilder.createTextNode(str(Pdepth))
             depth.appendChild(depthContent)
             size.appendChild(depth)
             annotation.appendChild(size)

             object = xmlBuilder.createElement("object")
             picname = xmlBuilder.createElement("name")
             nameContent = xmlBuilder.createTextNode(dict[oneline[0]])
             picname.appendChild(nameContent)
             object.appendChild(picname)
             pose = xmlBuilder.createElement("pose")
             poseContent = xmlBuilder.createTextNode("Unspecified")
             pose.appendChild(poseContent)
             object.appendChild(pose)
             truncated = xmlBuilder.createElement("truncated")
             truncatedContent = xmlBuilder.createTextNode("0")
             truncated.appendChild(truncatedContent)
             object.appendChild(truncated)
             difficult = xmlBuilder.createElement("difficult")
             difficultContent = xmlBuilder.createTextNode("0")
             difficult.appendChild(difficultContent)
             object.appendChild(difficult)
             bndbox = xmlBuilder.createElement("bndbox")
             xmin = xmlBuilder.createElement("xmin")
             mathData=int(((float(oneline[1]))*Pwidth+1)-(float(oneline[3]))*0.5*Pwidth)
             xminContent = xmlBuilder.createTextNode(str(mathData))
             xmin.appendChild(xminContent)
             bndbox.appendChild(xmin)
             ymin = xmlBuilder.createElement("ymin")
             mathData = int(((float(oneline[2]))*Pheight+1)-(float(oneline[4]))*0.5*Pheight)
             yminContent = xmlBuilder.createTextNode(str(mathData))
             ymin.appendChild(yminContent)
             bndbox.appendChild(ymin)
             xmax = xmlBuilder.createElement("xmax")
             mathData = int(((float(oneline[1]))*Pwidth+1)+(float(oneline[3]))*0.5*Pwidth)
             xmaxContent = xmlBuilder.createTextNode(str(mathData))
             xmax.appendChild(xmaxContent)
             bndbox.appendChild(xmax)
             ymax = xmlBuilder.createElement("ymax")
             mathData = int(((float(oneline[2]))*Pheight+1)+(float(oneline[4]))*0.5*Pheight)
             ymaxContent = xmlBuilder.createTextNode(str(mathData))
             ymax.appendChild(ymaxContent)
             bndbox.appendChild(ymax)
             object.appendChild(bndbox)

             annotation.appendChild(object)

          f = open(xmlPath+ '/'+name[0:-4]+".xml", 'w')
          xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
          f.close()
          show(files_len,x)
          x = x+1


#获取文件总数
def get_files_list_len(txtPath):
    from_path_list = os.listdir(txtPath)
    total = len(from_path_list) # 文件总数
    print('复制文件数：',total)
    return total

#转换为xml时的进度显示
def show(files_len,x):

    interval = 5 # 打算每隔5%变化一次，视需求改
    interval_num = int(files_len / (100 / interval)) 
    if (x % interval_num == 0):
        sys.stdout.write("Copy progress: %d%%   \r" % (x / interval_num * interval))
        sys.stdout.flush()


if __name__ == '__main__':
    #makexml("txt所在文件夹","xml保存地址","图片所在地址")

    makexml("yolo","VOCData/Annotations","VOCData/images")
