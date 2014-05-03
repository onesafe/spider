## 运行环境 ##
* ubuntu 13.04
* mysql
* django-1.6.2
* python 2.7



## 内容: ##
1. 一个爬虫:由**html_ptase.py thread_pool.py,thread_run.py,database_options.py**组成
2. 一个网站:在目录mm_image中.

## 运行方式: ##
1. 创建数据库.(mysql)
    * 使用命令进入数据库:   
```
mysql -u root -p
```
    * 在数据库shell下面 使用 source path建立数据库(path为本目录下面的**mm_image/sql/ceate_database.sql**)运行

2. 创建表:
    * 在mm_image下面运行命令  
    python manage.py syncdb


3. 获取资源:
    * 在根目录下运行:  
    python thread_pool.py
    * 开始抓取图片资源.等待一段时间.此时资源分目录保存在**mm_image/images**下面
    *此时,你可以在数据库中通过命令来查看拉了多少图片  
    select id from app_explore_image_picture;
    *若感觉已经足够:可以关闭运行爬虫的shell.最好通过ctrl+c来停止.(这里没有做优化)

4. 运行网站:
    * 进入**mm_image/**
    * 运行  ```python manage.py runserver```
    * 打开浏览器,输入http://127.0.0.1:8000
    * 首页里面是获取的点赞数最多的图片的大图轮播.
    * 点击左上角的分类,可进入不同的分类
    * 此时是一个粗略版的瀑布流.没有做延迟加载.
    * 点击“赞一个” 增加赞的数量
    * 点击“踩一个” 增加踩的数量
    * 点击图片可查看大图
    * 刷新页面可以按照赞的数量从新排序,赞最多的在前面

5. 若无法运行,请查看我录制的视频.
    * 链接: http://pan.baidu.com/s/1pJoERW3

## 具体实现过程 ##

### 爬虫 ###
1. 爬虫由四个个文件组成.
    * thread_pool.py 是 主要文件.里面有两个类.
        * 一个ThreadPool是一个线程池.负责回收和分发线程.
        * 一个ParseThread是页面处理的线程类.继承自threading.Thread
    * thread_run.py 是 进行页面处理的主要函数集合.
    * html_prase.py 是 一个html解析器的类.继承自HTMLPraser
    * database_option.py 是进行数据库操作的一些函数.

2. 线程池:
    * 线程池管理了一个队列,和若干线程.默认为5
    * 线程池初始化的运行其中的线程.但是全都处于阻塞状态(通过event实现)
    * 队列中最初有一个root url.
    * 线程池检测是否有未检测的url,若有,唤醒线程处理.
    * 队列中存放的是若干二元元组(函数闭包).第二个元素是url,第一个元素是处理不同url的不同函数.(主要存在两种url,一种是图片的url,一种是页面的url)

3. 页面处理线程:
    * 管理了一个独立的解析器,
    * 在初始化的时候从线程池获得队列的引用.
    * 若被唤醒,则自动处理列中的未检测的url.
    * 在run函数中,从队列中get一个函数闭包.然后运行该函数实现解析
    * 完成后阻塞自己

4. 解析器:
    * 每个线程拥有独立的解析器.
    * 当检测到a和img标签的时候,将url和相应的函数put进入队列.
    * 相应的处理函数在thread_run.py中.主要是do_page_parse函数和do_image_parse函数.

5. 解析函数:
    * do_page_parse 是进行页面解析的函数.运行过程为通过传递的url获取html string.调用parser对string进行解析
    * do_image_parse 是进行图片下载.并且将图片信息存入数据库

### 网站 ###
1. 前端采用bootstrap
2. 后台django
3. 首页使用了一个轮播插件,叫wowslider.


## 缺点 ##
1. spider 运行时,cpu 占用不正常.因为主线程的循环.
2. 没有使用浏览器内核解析.所以无法解析javascript和ajax
3. 没有做延迟加载.



    
