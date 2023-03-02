

<!--https://www.miniits.com/logo.html-->

![](./img/MiniLogo.png)


* 简单，快捷的AI模型训练和语料处理小工具集合～





### 一，语料冲突检测工具

1, 什么是语料冲突?

* 在很多情况下，语料来源是多样的。尤其在NLP领域，可能引入***样本内容相同，但是标签却不同***的情况，如果存在这样的冲突语料将会导致模型很难收敛。



2, 工具使用：


* 下载：
	* 必须下载1.4.3版本以上才有语料检测功能！

```shell
pip install pyaitools>=1.4.3
```



* 使用：

```python
from pyaitools import detect
```









