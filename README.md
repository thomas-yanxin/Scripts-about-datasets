# Scripts-about-datasets
数据集格式处理相关的脚本

## [coco2voc.py](https://github.com/thomas-yanxin/Scripts-about-datasets/blob/master/coco2voc.py) [COCO格式转VOC格式]
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
  
  

## [x2coco.py](https://github.com/thomas-yanxin/Scripts-about-datasets/blob/master/x2coco.py) [数据集转COCO数据集]
(1) labelmes数据转换为COCO格式：
```python
python tools/x2coco.py \
                --dataset_type labelme \
                --json_input_dir ./labelme_annos/ \
                --image_input_dir ./labelme_imgs/ \
                --output_dir ./cocome/ \
                --train_proportion 0.8 \
                --val_proportion 0.2 \
                --test_proportion 0.0
 ```
(2) voc数据转换为COCO格式：
```python
python tools/x2coco.py \
        --dataset_type voc \
        --voc_anno_dir path/to/VOCdevkit/VOC2007/Annotations/ \
        --voc_anno_list path/to/VOCdevkit/VOC2007/ImageSets/Main/trainval.txt \
        --voc_label_list dataset/voc/label_list.txt \
        --voc_out_name voc_train.json
 ```
  

## [VOC格式检测脚本](https://github.com/thomas-yanxin/Scripts-about-datasets/blob/master/x2coco.py) [用于VOC格式数据集中检测图片]
将check.py放入数据集目录中，执行如下命令：
```python
%cd dataset/VOC/
!cat train_list.txt | python check.py
!cat test_list.txt | python check.py
!cat val_list.txt | python check.py
 ```
## [数据集划分]
```python
# 安装依赖
!pip install paddlex
!pip install paddle2onnx
```

```python
!paddlex --split_dataset --format VOC --dataset_dir D:\MyDataset --val_value 0.2 --test_value 0.1
```
