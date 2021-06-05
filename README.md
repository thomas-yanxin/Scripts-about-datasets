# Scripts-about-datasets
数据集格式处理相关的脚本

## [coco2voc.py](https://github.com/thomas-yanxin/Scripts-about-datasets/blob/master/coco2voc.py)
首先需要安装相关依赖：
```python
!git clone https://gitee.com/yanxin_thomas/cocoapi.git
%cd cocoapi/PythonAPI/
!make
!python setup.py install
!pip install lxml
```

然后根据具体情况作如下修改：
```python
# 转换后的VOC存放地址
CKimg_dir ='/home/aistudio/dataset/VOC/images'
CKanno_dir = '/home/aistudio/dataset/VOC/annotations'
```
```python
def get_CK5(origin_anno_dir,origin_image_dir,verbose=False):
    dataTypes = ['train2017']   #需要根据COCO数据集作具体修改
    for dataType in dataTypes:
        annFile = 'train.json'
        annpath=os.path.join(origin_anno_dir,annFile)
        coco = COCO(annpath)
        classes = catid2name(coco)
        imgIds = coco.getImgIds()
        # imgIds=imgIds[0:1000]#测试用，抽取10张图片，看下存储效果
        for imgId in tqdm(imgIds):
            img = coco.loadImgs(imgId)[0]
            showbycv(coco, dataType, img, classes,origin_image_dir,verbose=False)
```
```python
def main():
    base_dir='/home/aistudio/dataset/VOC'#step1 这里是一个新的文件夹，存放转换后的图片和标注
    image_dir=os.path.join(base_dir,'JPEGImages')#在上述文件夹中生成JPEGImages，Annotations两个子文件夹
    anno_dir=os.path.join(base_dir,'Annotations')
    mkr(image_dir)
    mkr(anno_dir)
    origin_image_dir='/home/aistudio/dataset/train/images'#step 2原始的coco的图像存放位置
    origin_anno_dir='/home/aistudio/dataset/train/annotations'#step 3 原始的coco的标注存放位置
    verbose=True #是否需要看下标记是否正确的开关标记，若是true,就会把标记展示到图片上
    get_CK5(origin_anno_dir,origin_image_dir,verbose)
```
