CSDN已下载资源自动批量评论脚本
=======================

[![PyPi version](https://img.shields.io/pypi/v/csdncommenter.svg)](https://pypi.python.org/pypi/csdncommenter)

###功能
自动批量打分评论指定账号内所有下载过待评论的资源。

###用法

1. 使用 PyPi

	```
	pip install csdncommenter
	csdncommenter
	```

2. 使用 Git

	将本工程克隆到本地，到 csdncommenter 子目录里运行

	```python
	python csdncommenter.py
	```

###已实现特性

1. 一次登录，评论所有待评论资源。
2. 适应CSDN两个资源评价至少间隔60S的规则。
3. 随机打分一到五星，并选择对应的评语（目前都是一个英文短句）。

```
Author : Zhuang Ma
Website: http://www.mazhuang.org
E-mail : ChumpMa(at)gmail.com
```
