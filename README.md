# NJU BASIC DATA SCIENCE

## 数据科学基础

"反面向用例+代码评估+能力评价"程序

### 更新记录

- 2020.04.29 程荣鑫：提交了evaluator.py代码，代码逻辑仍需要修改我先提交这么多了。
- 2020.07.01 程荣鑫：重启项目，整顿之前面向用例判断的漏洞。
- 2020.07.01 陈彦泽：提交了工作一半的文件，加入了.gitignore，加入了之前讨论的文档
- 2020.07.02 程荣鑫：修改了evaluator.py和defender.py，添加了driver.py
- 2020.07.02 陈彦泽：修改了evaluator.py中删除文件的方法，见使用说明
- 2020.07.03~2020.07.06 程荣鑫&陈彦泽，用subprocess代替较老的模块os
- 2020.07.09 程荣鑫：添加了abilities包，abilities.py(为方便调用函数放进calculate包中)用于评估每个学生面对不同种类题目的表现
- 2020.07.11 陈彦泽：添加了calculate包，Calculator.py用于处理编程能力评估
- 2020.07.11 陈彦泽：为CaseData类添加了成员变量type，标识题目类型
- 2020.07.19 陈彦泽：给StudentGroup类加上了筛选开关，可以剔除做了不到80题的学生
- 2020.07.19 程荣鑫：添加pca.py和correction.py，用于主成分分析和相关性分析

### 功能阐述

- 反面向用例：我们的程序会尽可能去除那些"疑似作弊"的代码骗来的分数，以便进行后续的评估
- 代码评估：我们的程序会根据代码行数、运行时间等等因素评估提交代码的质量
- 题目难度分析：根据学生整体的做题表现尝试评估每道题目的难度
- 能力评价：在上述三点之外，我们还给出每个学生的能力（数值化）

### 数据说明&代码解释

- evaluator类的getScore方法能返回一个元组，元素如下
    - 第一个返回值分三种情况，异常提交: False，正常提交: True
    - 第二个返回值是剔除面向用例后的真实得分比例
    - 第三个返回值是运行时间
    - 第四个返回值是代码行数
    
- defender类用于防卫异常提交，包含如下两个方面
    - cpp提交，返回值为-1
    - 面向用例，返回单题作弊次数/单题测试用例数
    
- driver类用来自动爬取数据运行评估
  
    - 主要用于测试defender类和evaluator类
    
- DataUtils.py为一些数据处理的工具，比如均值、方差等

- StudentGroup.py将学生分为五组

- distribution.py画了一个题目作答人数的分布图

- abilities包中的数据为每个学生在各个种类题目上的表现，我们用0～100的浮点数来表示

- CaseData类为calculate包中的case封装类

- Calculator.py中

    - score_evaluator_get_score_save(group)用于生成每组的中间数据group{id}.json（已完成，无需再跑）

    - run(group, times=20)用于对某个组进行迭代计算

    - ```python
        get_student_ability(group)
        get_case_difficulty(group)
        get_case_student_map(group)
        get_student_case_map(group)
        ```

        用于获取某个组迭代计算后的数据，**外部文件可直接调用这类接口**
    
- StudentGroup类将`getStudentGroup`和`getQuestionGroup`的中的`isFilte`改为True可以打开筛选

### 使用方法

- 在evaluator类中的main函数启动程序即可（需要注意python的环境变量配置问题）

- 随后在命令行输入url即可自动下载代码到本地（文件下完取完数据会自动删除

- windows和mac下删除文件和运行python的指令不同，需要修改evaluator.py中的以下代码

	```
	def deleteDir(dir):
	    windowsDeleteDir(dir)
	
	def deleteFile(file):
	    windowsDeleteFile(file)
	
	# res = os.system('python3 {}<{}>>{}'.format(file, cls.work_dir + '/test.txt', cls.work_dir + '/test.txt'))
	res = os.system('python {}<{}>>{}'.format(file, cls.work_dir + '/test.txt', cls.work_dir + '/test.txt'))
	```
    经测试，其实这里不改也不影响在MAC系统上的使用，就把这里的内容作为参考吧。

	