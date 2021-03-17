# 电机驱动

要驱动电机使线到达指定长度，就必须要知道初始长度以及电机步数。初始长度可以通过手动调整到指定位置，或者手动输入初始长度。电机步数则用一个无符号整型记录即可。另外，最好能知道当前转子的状态，这样的话步就能以拍为单位精确调整。

我们用 `steps_now` 来表示电机当前的步数，`step_length` 表示步长（以拍为单位），一拍的转动长度 `stride_length` 约等于 0.0046mm，则线长 `thread_length=steps_now*step_length*stride_length`。

步进电机我们采用 8 拍的驱动方式，即：


| 转子状态 | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   |
| -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1-红    | VCC | VCC | VCC | VCC | VCC | VCC | VCC | VCC |
| P2-橙    | GND | GND |     |     |     |     |     | GND |
| P3-黄    |     | GND | GND | GND |     |     |     |     |
| P4-粉    |     |     |     | GND | GND | GND |     |     |
| P5-蓝    |     |     |     |     | GND | GND | GND |     |

我们定义当前的转子状态 `motor_state_a` 与步数 `steps_now_a` 、步长 `step_length` 的关系如下：

```python
motor_state = (steps_now_a * step_length) % 8
```

初始化时，用户要调整电机，使得笔恰好对齐某个位置，这个位置的线长是固定的（在组装时设置好），假设是 `init_thread_length`，则初始时的步数为：

```python
steps_now = int(init_thread_length / (step_length * stride_length))
```

但如果我们想要精确到拍的话，上面的初始过程就不够好。所以我们规定，在用户调整电机时，转子始终停在 0 状态，并且初始步数要被 8 整除：

```python
steps_now -= steps_now % 8 
```

之后在写字的过程中，如果要去到 `thread_length` 位置，需要移动的步数为：

```python
int(thread_length/step_length/stride_length)-steps_now
```