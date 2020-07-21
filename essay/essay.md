# BigCode 代码能力分析

[toc]

## Contributor

* 程荣鑫 @Sparrow612
* 陈彦泽 @Cpaulyz
* 庄子元 @NIL-zhuang

## Abstract

对于近300同学提交的约1000道题python代码进行分析，剔除其中的C++提交和面向用例提交得分，利用马尔可夫链模型对学生解题能力-题目难度进行迭代计算收敛，最终得到各题目的难度和各学生的编程能力。

**Keywords**：马尔科夫链，编程能力评估

## Introduction

编程OJ（Online Judge）是评估学生对编程语言的掌握能力、逻辑思维能力等的重要方式，目前被普遍用于各类测试、练习和竞赛中。对学生编程能力进行合理高效的计算对衡量学生编程能力，分配训练题目等都有着重要的应用价值。

南京大学2018级软件学院约250名同学在2020春季学期的数据科学基础课上，基于MoocTest平台，分为5组完成了总计近1000道python编程题。通过对数据进行分析、采访部份同学等方式，我们发现在编程OJ中，存在如下一系列影响评估的行为：

1. 碍于编程题目的原创性低，部分同学利用搜索引擎在leetcode, codeforce, geekforgeeks，poj等各大OJ平台上找到类似的原题，并抄袭题解以期提高得分
2. 由于MoocTest平台以编程训练为旨，会给学生错误答案的实时反馈。部分学生利用此特性编制面向测试用例的代码，来绕过代码逻辑，获得评测分数。
3. 题目的选择和分配没有难度区分，不同组别、不同学生之间题目相差较大。难以用初始得分评估学生的编程水平

## Code explanation

### 反面向用例

代码在defender.py文件中，它包含两个方面：

1. 极个别的C++语言提交
    
    这不在我们分析范畴内，所以遇到这类代码直接标记为‘不可用’

2. 面向用例代码

    举个例子，下面这样的代码，测试用例为input: 10, output: 213123123123
    
        if input == 10:
    
            print(213123123123)

    会被我们的程序捕捉到。我们扫描同学们提交的代码，并与测试用例的输入输出作匹配，得出同学们在某道题上的“水分”，也就是以面向用例手段通过的用例占比（如果这题全是这么过的，那么就会被降到0分）。

### 提交代码评估

这部分代码主要在evaluator.py和Calculator.py中

1. evaluator.py

    它接收一个输入————test_data.json中的某个url————输出指定格式的评估结果。

    包含了提交代码的下载、面向用例检查、运行等

    返回值的格式是这样的：

    (bool, double, double, int)

    第一个布尔值表示它是否为正常的python提交（前面说过有个别C++提交），第二个浮点数表示剔除面向用例的真实得分比例，第三个浮点数表示运行时间（单位为ms），最后一个int表示代码的行数。

    值得注意的是，我们利用了subprocess模块来执行提交的.py文件，这个模块的启动可能受到多种因素影响，比如电脑的缓存、端口占用情况等等。所以为了减少个人电脑性能对运行时间造成的影响（在个人电脑上得到的代码运行时间不仅波动剧烈而且数值很大），我们将代码放在服务器上运行，得出来的结果比在自己电脑上跑出来的令人满意。

    运行示例图：

    ![](https://lemonzzy.oss-cn-hangzhou.aliyuncs.com/img/Xnip2020-07-21_13-26-53.png)

2. Calculator.py

    它负责将test_data.json中的学生和题目分组（每组学生做的题目都是一样的，这是我们分组的依据），然后以组为单位评估学生代码，通过调用evaluator.py来完成。我们认为，对某个学生做的特定题目而言，选最后一次提交来分析是比较合理的。

    他的输出信息主要在控制台，以及json文件中。calculate包中的5个group.json文件就是运行的结果。

    至此，Calculator.py的第一个任务完成了。

    ![](https://lemonzzy.oss-cn-hangzhou.aliyuncs.com/img/Xnip2020-07-21_13-28-23.png)

    持久化数据：

    ![](https://lemonzzy.oss-cn-hangzhou.aliyuncs.com/img/Xnip2020-07-21_13-31-35.png)

### 能力计算

这涉及Calculator.py和abilities.py两份代码。

1. Calculator.py

    根据每组先前运算得出的数据成果作进一步处理，算出每组题目的对应题目难度和学生能力值（综合能力）

2. abilities.py

    主要算每个学生在不同类别题目中体现出的能力水平，方便后续的数据分析。产物有四个阶段，从最开始的毛坯raw_abilities.json到最后的final_abilities.json都在abilities包中存放。

    ![](https://lemonzzy.oss-cn-hangzhou.aliyuncs.com/img/66BE2505-050B-4CC4-AEB5-6E50B14257C2.png)


### 总结

主要的代码已经解释完毕，剩下一些代码是我们写的一些画图工具，或者帮助数据分析的一些代码，像pca.py负责主成分分析，kmeans.py实现k均值聚类算法，correction.py用于相关性计算等等。

## Approach

## Experimental evaluation

## Conclusion