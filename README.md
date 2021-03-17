# Woodpecker

> 一个简单、低成本、可DIY的写字机器人
>
> A simple, low price, DIYable writing machine

## 项目介绍

### 为什么我要做这个？

目前大多数写字机器人的成本都很高，淘宝上的最低也要500，而开源的也要2~3百。在我看来，写字只是一件很简单的事，根本不需要这么多钱。因此，我希望能设计出一款低于百元的写字机器人。

我大致看了一下网上的开源方案，比较有代表性的如 github 上的 [peng-zhihui/X-Bot](https://github.com/peng-zhihui/X-Bot) 和 arduino社区的 [写字机器人](https://www.arduino.cn/thread-93897-1-1.html)，使用的基本是 core-XY（XY联动）方案，这种方案的介绍可以看 [peng-zhihui/X-Bot](https://github.com/peng-zhihui/X-Bot)，简单来说就是十字交叉的「同步带+导轨」+两个伺服电机

这种方案基本上可以无缝用于工业了好吧╮(╯-╰)╭，不贵才怪呢！个人使用的无需这么复杂。于是就有了这个项目。下面来说说我的想法。

补充资料：

* [3D打印机设计：关于 CoreXY 与 H-bot 之间的选择](https://blog.libcore.org/?p=291)
* [H-BOT机械手模型](http://bbs.inovance.com/course/67/207)

### 我的想法

作为非机械系学生，我希望结构越简单越好。首先，电机直接控制笔在两个方向上的运动。两者要如何连接呢？自然而然，我想到了线。用线的话，就不能在水平面，而是要在垂直面上控制笔——纸固定在墙上，上面挂两个电机，电机用线吊着笔。显然，这种方案在数学上是可行的，给定两根线长，可以求出笔在纸上的位置。

那么，如何控制笔的起落呢？这个可以借鉴以前的开源方案，用一个小舵机来控制笔的旋转，从而控制笔与纸的接触。

![构思](/assets/images/构思.jpg)

至此，大概雏形就已经出来了。当然，我不是第一个提出的这种方案的人，网上已经有 DIY 教程：[instructables - Polargraph Drawing Machine](https://www.instructables.com/Polargraph-Drawing-Machine/)，这家伙甚至写好了代码！Bravo！

但这只是节省了导轨的成本，并没有节省伺服电机的成本。于是我想，笔这玩意又没多重，应该用步进电机就行了吧，看网上资料说步进电机没有累积误差，那我直接计算转的圈数就能获取当前的绳长。如果有失步，或许可以通过中途再校正来消除。

OK，想法有了，开干！

## 设计过程

### 硬件

需要的硬件有：

* 步进电机28BYJ-48 + 驱动板 2 套 共￥9.6
* 舵机SG90 1 个 ￥3.9
* 细长线 2 条 ￥0（找妈要）
* 杜邦线母对母、公对母 若干条 ￥1
* 5V电源 1 个 ￥2
* 热熔胶 ￥9.3
* 可选：液晶小黑板（省得老是换纸）米家的贵一点（￥48.9），淘宝上有 ￥9.9 包邮的

总共：￥25.8（不考虑液晶小黑板）

另外还需要控制设备。如果使用上位机与下位机分离的方式，电脑作为上位机，下位机可以是 arduino、stm32、esp8266；如果上位机与下位机一体，可以使用树莓派 zero. 控制设备大概要花费 ￥70

因为我有树莓派，所以我直接在树莓派上控制。

#### 3D 打印

需要 3D 打印的部分有：步进电机固定座、轴套、舵机固定座、笔托。这里问题比较大的是舵机固定座和笔托。因为在初次实验中，我发现写字时笔会歪，导致笔不可能垂直于纸。要解决这个问题，我设想了几个方案：

* 如果是液晶小黑板，则将直杆形的笔换成圆盘性的笔，这样就能解决左右歪的问题，至于上下歪，可以通过增加配重来解决。
* 如果是一般的笔，可以直接在舵机固定座两边加上泡沫支撑
* 双绳方案：增加多一条绳（会增加安装难度



### 软件

第一个问题是，如何将 x-y 坐标的图像，转换为双极坐标？

第二个问题是，给定一条曲线，如何控制步进电机？如果要考虑下笔的轻重，那如何控制舵机？

第三个问题是，如何将图像/文字转化成线？

第四个问题是，怎么规划路径？或者说，怎么决定笔画的顺序？


#### 问题一

双极坐标（Bipolar Coordinates）的定义如下：<img src="https://latex.codecogs.com/svg.latex?\inline&space;A,B" title="A,B" /> 是两固定点，距离为 <img src="https://latex.codecogs.com/svg.latex?\inline&space;w" title="w" />，平面上任意一对点都可以用到 <img src="https://latex.codecogs.com/svg.latex?\inline&space;A,B" title="A,B" /> 的距离 <img src="https://latex.codecogs.com/svg.latex?\inline&space;a,b" title="a,b" /> 来表示。详细介绍请去看：[百度百科](https://baike.baidu.com/item/%E5%8F%8C%E6%9E%81%E5%9D%90%E6%A0%87%E7%B3%BB/22803822) 和 [维基百科](https://zh.wikipedia.org/zh-hans/%E9%9B%99%E6%A5%B5%E5%9D%90%E6%A8%99%E7%B3%BB)

<center><img src="/assets/images/bipolar_plot.jpg" title="双极坐标" width="400"></center>


坐标系变换这个应该是在高等数学中学的。我们要实现的就是如下变换：

<center><img src="https://latex.codecogs.com/svg.latex?(x,y)\leftrightarrow(a,b)" title="(x,y)\leftrightarrow(a,b)" /></center>

一般来说，<img src="https://latex.codecogs.com/svg.latex?\inline&space;(x,y)" title="(x,y)" /> 原点在图像的左下角，但对于悬挂式的写字机器人，图像是从左上角开始画的，所以我们规定左上角是为原点。这么一来，就有：

<center><img src="https://latex.codecogs.com/svg.latex?\begin{cases}&space;a=\sqrt{x^2&plus;y^2}\\&space;b=\sqrt{(w-x)^2&plus;y^2}&space;\end{cases}" title="\begin{cases} a=\sqrt{x^2+y^2}\\ b=\sqrt{(w-x)^2+y^2} \end{cases}" /></center><br>

<center><img src="https://latex.codecogs.com/svg.latex?\begin{cases}&space;x=\frac{a^2&plus;w^2-b^2}{2w}\\&space;y=\frac{1}{w}\sqrt{(aw)^2-\left(\frac{w^2+a^2-b^2}{2}\right)^2}&space;\end{cases}" title="\begin{cases} x=\frac{a^2+w^2-b^2}{2w}\\ y=\frac{1}{w}\sqrt{(aw)^2-\left(\frac{w^2+a^2-b^2}{2}\right)^2} \end{cases}" /></center>

图像转换成双极坐标后，我们就可以像在直角坐标下那样思考。后面默认都是双极坐标。

#### 问题二

步进电机的原理很简单，就是通过磁场的旋转，来带动转子转动。磁场又是通过脉冲控制的，那样只要知道初始位置和脉冲数量，就知道笔的位置。

[步进电机28BYJ-48拆机图、原理和51/stm32测试程序](https://blog.csdn.net/wangguchao/article/details/78902212)

#### 问题三

见 ImagePreprocess

这里我参考了 [Samir55/Image2Lines](https://github.com/Samir55/Image2Lines)、[arthurflor23/text-segmentation](https://github.com/arthurflor23/text-segmentation)、[A Statistical approach to line segmentation in handwritten documents](https://cedar.buffalo.edu/~srihari/papers/SPIE-2007-lineSeg.pdf)


#### 问题四

见 PathDecide


