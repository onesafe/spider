
#version 0.2#
**目的:模块松耦合,优化代码(非架构优化)**


##thread_pool.py##

1. global COUNT:
COUNT 变量的目的是为了记录爬取的图片的数量，这个变量在五个子线程中都有使用和修改,所以之前使用全局变量解决.
改进办法:
标准做法是在thread_pool类中作为实例属性,并且传进五个子线程中.
但是python中的变量为引用调用,所以采用'list'完成此任务..
代码中的注释'#add/#modified'处为相关改动

2. global EVENT:
EVENT 变量是为了实现对队列的互斥访问,但是经过前一段时间的学习得知Queue为线程安全.所以去掉此全局变量

3. global MUTEX:
MUTEX 为子线程资源访问互斥锁..是必要的,没有改动的必要.

# version 0.3 #
**目的: 函数松耦合**

##thread_run.py##

1. 对外部无需调用的函数,使用默认的私用函数命名规则(以下划线开头),对其他模块隐藏调用,只保留外部调用的两个函数(do_image_parse/do_page_parse)

## database_option.py ##
1. 为每一个函数添加了异常处理,防止不按照顺序调用,出现程序抛出异常的情况

经过上述的处理,四个模块之间只有import调用，没有其他非法调用,并且模块内部的耦合已经降到最小..函数之间的已经断耦合(任意调用某个函数都将得到相应的结果，不会抛出异常，同时函数调用没有次序限制)

#version 0.4#

1. 修改代码细节 
 
   (1). 修改程序入口,程序入口为**thread_pool_run.py**
 
   (2). 修改函数注释，添加函数doc string
 
   (3). 修改参数处理函数**deal_argv**的错误提示
 
   (4). 修改部分不规范函数命名,**check_image_count**->**image_fetch_finished**
 
   (5). 修改部分不规范代码
 
   (6). 模块内代码组织规范化


2. 函数断耦合**thread_deal_functions.py**(原*thread_run.py**)

   (1). 封装http request函数(_http_request)
 
   (2). 将_get_image函数拆分成几个功能更加独立的函数(_get_image_path,_store_image,_set_image_info,_http_request)
 
   注:具体请看代码中使用**add for coupling**注释标注的代码


3. 处理MMHtmlParse与ThreadPool两个类的耦合关系

   (1). 通过增强MMHtmlParse的健壮性来断耦合


4. 增强程序整体健壮性

   (1). 通过参数检查,异常处理等方式增强代码的来增强代码的健壮性
  
   注:具体请看代码中使用**add for robustness**标注的代码


