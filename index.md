# 快写下来！

这是[`alingse`](https://github.com/alingse)写的github page用来写一些东西

很想说：快写下来！

## 页面目录结构

###  存储

原始markdwon文章统一存储在repo 下`_source`文件夹下，同一文章有md和html(由md文件导出)两种格式的文件

发布文章存放在`article`目录下，文章从[`100000.html`](/article/100000.html)开始编号

列表页的模版存储在`_template`下面


###  主分类
 大分类上大致目前先开这四大类。
 
1. `/learn` [学习](/learn)
2. `/code`[编码](/code)
3. `/math`[数学](/math)
4. `/fun`[段子](/fun)

每个分类下是一个列表页`index.html`，给出文章的列表页(使用 构建工具构建)


### tag



计划每篇文章内加 tag，通过构建，给出tag的列表页

以及相关tag的列表页`index.html`，比如：

[`/tag`](/tag)

`/tag/java` [java]()

`/tag/concurrency` [并发]()
   
`/tag/chengdu` [成都]()

###  date

也使用构建工具，按照日期页构建出 每年、每月各个级别的列表页

`/date/2016/07` 

诸如此类



