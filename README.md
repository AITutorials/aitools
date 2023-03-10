

<!--https://www.miniits.com/logo.html-->

![](./img/MiniLogo.png)



## 简单，快捷的AI模型训练和语料处理小工具集合～





### 一，语料冲突检测工具

1, 什么是语料冲突?

* 在很多情况下，语料来源是多样的。尤其在NLP领域，可能引入***样本内容相同，但是标签却不同***的情况，如果存在这样的冲突语料将会导致模型很难收敛。



2, 快速使用：


* 下载：
	* 必须下载1.4.6版本以上才有语料检测功能!

```shell
pip install pyaitools==1.4.6
```

或

```shell
pip install pyaitools==1.4.6 -i https://pypi.org/simple/
```




* 使用：

```python
from pyaitools import detect

# 需要进行检测的训练数据路径
sample_path = "./train.csv"

# 检测完后需要写入的新文件路径
deconflict_sample_path = "./new_train.csv"

detect.corpus_conflict_detect(sample_path, deconflict_sample_path)
```


> * 输出：

```text
去重后Y标签数量: 3
去重后N标签数量: 3
去重后冲突样本数量:2
冲突样本已写入路径:./conflict_sample.txt
去冲突+去重复后Y标签数量: 1
去冲突+去重复后N标签数量: 3
```


* 参数：
> * sample_path: 需要检测的训练数据路径，训练数据格式为csv，详细要求看下面介绍，无默认值，必须写
> * deconflict_sample_path: 去除冲突后，新训练数据的路径, 无默认值，必须写
> * sep: 需要检测的csv文件中使用什么作为分隔符, 默认为",", 也可以选择"\t"
> * label_list: 标签列表，该列表只有两个元素，默认为["Y", "N"]，需要按照自己定义的标签进行修改
> * choiceDeleteLabel: 当样本发生冲突时，选择删除哪一类标签后生成新数据，默认为"Y"，需要按照自己定义的标签进行修改
> * csample_path: 冲突数据写入的文件路径，默认为./conflict_sample.txt



* 训练数据格式要求：


> * 训练数据例子：
```csv
sentence1,sentence2,relation
镀锌钢管水冲洗调和漆一道,镀锌钢管室内水dn50,N
镀锌钢管水冲洗调和漆一道,镀锌钢管国标螺纹连接水压试验,Y
镀锌钢管,镀锌钢管室内水dn50,N
镀锌钢管室内水dn50螺纹连接水压试验,镀锌钢管螺纹连接水压试验,N
镀锌钢管,镀锌钢管室内水dn50,Y
镀锌钢管水冲洗调和漆一道,镀锌钢管室内水dn50,Y
```

> * 1，训练数据由内容列+标签列构成，其中内容列可以是任意多列（例子中是两列sent1和sent2）
> * 2，标签列必须是最后一列，而且该检测只针对二分类，标签必须只有两种
> * 3，内容列+标签列的列名随意











