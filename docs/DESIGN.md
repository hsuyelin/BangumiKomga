# DESIGN

## 文件序号逻辑

### 运行脚本前

运行脚本前komga中顺序如下：
![image](https://user-images.githubusercontent.com/45256288/217723983-4f1ed932-a587-4740-b1ce-e6cedaa21fa7.png)

_注意：komga并不是按照文件名中的序号进行排序的_

### 运行脚本后

运行脚本后komga中顺序如下：
![image](https://user-images.githubusercontent.com/45256288/217725540-ca447b5c-f8e8-423f-8b32-ca608002b64d.png)

红框中三本书匹配到元数据，并**更新序号**。其余书的**序号未变**

### 逻辑

本脚本目前将书籍系列下所有书均视为单行本/卷

在匹配单行本元数据时，会提取此系列下每本书的最后一组数字，与bangumi上单行本的序号进行比较：
- 如果序号一致，则刷新元数据，更新序号
- 如果序号不一致，~~则跳过此书~~👉则只更新序号

### 数字匹配规则

取文件名中匹配到的最后一组数字，数字匹配规则有：

- 纯数字
- 数字+'.-_'+数字


## 同步阅读进度逻辑

_仅简单逻辑，使用时注意_

获取此书籍系列已读书数量，然后更新Bangumi上卷数

