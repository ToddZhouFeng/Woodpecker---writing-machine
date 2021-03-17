# 路径决策

本模块要解决如何通过位图来驱动电机，这是本项目的核心模块。我们规定以下对象和接口：

* `bitmap` 位图（二维矩阵，值为0或1，1表示要下笔的地方），大小为 a_max × b_map
* `index2length(index_a, index_b)` 由位图像素的索引计算出长度
* `drop()` 和 `lift()`
* `motor_a` 电机a
  * `motor_a.move(thread_length)` 移动到对应长度
* `motor_b` 电机b
  * `motor_b.move(thread_length)` 移动到对应长度


## 扫描法

顾名思义。优点是简单，缺点是慢。

```python
for k in range(a_max):
    for l in range(b_max):
        if bitmap[l,k]==1:
            drop()
        else:
            lift()
        thread_length_a, thread_length_b = index2length(k,l)
        motor_a.move(thread_length_a)
        motor_b.move(thread_length_b)
```

为了提高效率，我们可以考虑采用跳跃扫描法（实际是缩减分辨率）。如下：

```python
for k in range(0,a_max,2):
    for l in range(0,b_max,2):
        if bitmap[l,k]==1 or bitmap[l+1,k]==1 or \
            bitmap[l,k+1]==1 or bitmap[l+1,k+1]==1:
            drop()
        else:
            lift()
        thread_length_a, thread_length_b = index2length(k,l)
        motor_a.move(thread_length_a)
        motor_b.move(thread_length_b)
```

## 深度搜索法

简单来说就是先扫描，当找到第一个下笔点后，从下笔点开始不断向外搜索，并移动。当找不到时，抬笔，再次向外搜索，然后找到下笔点后，再重复前面的过程。如下：

```python
while True:
    index_next=search(image, index_now)
    if index_next == None:
        break
    if not is_next_to(index_next, index_now):
        if is_drop():
            lift()
        else:
            drop()
    thread_length_a, thread_length_b = index2length(index_next[0],index_next[1])
    motor_a.move(thread_length_a)
    motor_b.move(thread_length_b)
    image[index_now[0], index_now[1]] = 0
```

但这只能达到局部最优，而不能达到全局最优。举个例子，假如说要写一个 T 字，显然，先写一横，再写一竖是最快的，但有可能会先写一个“7”，再补回横的后面，这样的效率就不高。

那这样，我想可以先搜索出所有路径（深度优先或广度优先都行），然后从路径中选择一条最短的路径。这种策略就可以解决上面的问题。

但上面的策略并不完美，比如说要写一个 R 字，从左下开始，如果是选择最短的路径，则会写一个“∧”，然后再写上面的圈。但最快的方式显然是先写一竖 |，再写半圈 ﹚，最后写右下一捺，这样可以一笔写完。（不知道说不说得清……）

于是咱的策略又要改变，我们需要知道最短与最长的路径。如果最长的路径可以覆盖当前的连通区域，那么就选择最长的路径，否则，选择最短的路径。

但这种方法的复杂度很高。为了减少复杂度，我认为在搜索路径时，可以只取某几个方向。比如上一步是向上搜索，那么下一步就只能搜索上面的三个像素。（也就是把一段弯折的线看作不同线段）

算了，太复杂了😫别搜索所有路径了，直接按第一段来吧。