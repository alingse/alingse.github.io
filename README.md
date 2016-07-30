# 快写下来！

这是alingse 的github page

**有想的就赶快写下来！**
##  网站架构

- `/article`  存放文章的html 连接类似 `/article/100001.html` 
- `/math`    以下分别是四大类目，用文章`meta`中的`cat`聚合
- `/code`
- `/learn`
- `/fun` 
- `/tag`、`/tag/xxx` 存放聚好相同tag 的文章，用文章`meta`中的`tags`聚合
- `/date`、`/tag/xxxx/xx` 存放聚好相同时间周期的文章，用文章`meta`中的`cdate`聚合

##  写作流程

### 编写

1. 原始的 markdown文件 在 `_source`文件夹下编写。需要提交

   文件名要求格式 `N.xxx.md`其中 `N` 是按顺序的编号，目前排到**`100001`**

2. 原始markdown文档中插入 yaml 信息
    参考如下文件头编写：
    
	```
	<YAML-META-INFO-START/>
		
	<!--
	id: 100001
	tags:
	  - tongji|统计
	  - translate|翻译
	cat: math
	cdate: "2016.07.30"
	mdate: "2016.07.30"
	title: "Stata Data Analysis Examples: Zero-inflated Poisson Regression"
	keyword: 
		- Zero-inflated Poisson
		- Regression
		- Stata Data Analysis
	-->
	<YAML-META-INFO-END/>
	```
	其中 tag 部分是因为想确保链接是英文而网页上显示 中文的tag，用`|`连接即可
	
   编写完成需要导出为html 同样保存到`_source`文件夹下
   
###  构建

1. 加载正确的文章meta信息 （**完成**）
		
2. 按照各个聚合方案聚合meat信息 (**TOADD**)
	
3. 移动文章到 article 目录 (**完成**)
	
4. 使用模版渲染歌模块的文章列表页（**TODO**）
    
   包括各大类 `tag` 以及`date`等。目前还没有模版


### 自动化提交／自动发布

#### TODO
