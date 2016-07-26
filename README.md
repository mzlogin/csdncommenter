# CSDN 已下载资源自动批量评论脚本

[![PyPi version](https://img.shields.io/pypi/v/csdncommenter.svg)](https://pypi.python.org/pypi/csdncommenter)

### 功能

自动批量打分评论指定账号内所有下载过待评论的资源。

### 用法

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

### 已实现特性

1. 一次登录，评论所有待评论资源。

2. 适应 CSDN 两个资源评价至少间隔 60S 的规则。

3. 根据现有评星打分，并根据打分选择对应的评语（目前都是一个英文短句），不会对资源的评星产生不良影响。

```
Author : Zhuang Ma
Website: http://mazhuang.org
E-mail : chumpma(at)gmail.com
```
