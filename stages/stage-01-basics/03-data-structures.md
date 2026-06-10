# 03 - 数据结构：list / tuple / set / dict

## 3.1 速查表

| 类型 | 可变 | 有序 | 可哈希 | 重复元素 | 字面量 |
|---|---|---|---|---|---|
| `list` | ✅ | ✅ | ❌ | ✅ | `[1, 2, 3]` |
| `tuple` | ❌ | ✅ | ✅（若元素都可哈希）| ✅ | `(1, 2, 3)` |
| `set` | ✅ | ❌ | ❌ | ❌ | `{1, 2, 3}` |
| `dict` | ✅ | ✅（3.7+）| ❌（键） | 键唯一 | `{"a": 1}` |

## 3.2 list — 主力序列

```python
xs = [1, 2, 3]
xs.append(4)        # 末尾追加
xs.extend([5, 6])   # 合并
xs.insert(0, 0)     # 在 0 位插入（O(n)，少用）
xs.pop()            # 弹末尾
xs.pop(0)           # 弹首位
xs.remove(2)        # 删第一个值为 2 的元素
xs.index(3)         # 找下标
xs.sort()           # 原地排序
sorted(xs)          # 返回新列表
xs.reverse()
len(xs)
3 in xs             # 成员检查（O(n)）
```

**切片**（list / tuple / str 都支持）：

```python
xs = [0, 1, 2, 3, 4, 5]
xs[1:4]      # [1, 2, 3]
xs[::2]      # [0, 2, 4]    步长 2
xs[::-1]     # 反转 [5, 4, 3, 2, 1, 0]
xs[:3]       # [0, 1, 2]
xs[3:]       # [3, 4, 5]
```

**列表推导式**（最常用）：

```python
squares = [x * x for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]
```

**不要这样**：

```python
result = []
for x in range(10):
    result.append(x * x)    # 累加器模式
```

**而要**：

```python
result = [x * x for x in range(10)]
```

> 经验：累加器能改成推导式就改；不能改（要带副作用）就保留。

## 3.3 tuple — 不可变序列

```python
point = (3, 4)
x, y = point              # 解包
a, b, *rest = (1, 2, 3, 4)  # a=1, b=2, rest=[3, 4]
first, *_, last = (1,2,3,4,5)  # first=1, last=5, _=[2,3,4]
```

**单元素 tuple 注意逗号**：

```python
(1)    # 整数 1
(1,)   # 单元素 tuple
```

**元组为什么重要**：

- 可哈希 → 能当 dict key / set 元素
- 解构方便
- 表达"几个字段的不可变记录"
- 性能略好于 list

**命名元组**（阶段 4 详讲 `dataclass` / `NamedTuple`）：

```python
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p.y
```

## 3.4 set — 无序去重

```python
s = {1, 2, 3}
s.add(4)
s.update([5, 6])
s.discard(7)   # 不存在不报错
s.remove(7)    # 不存在抛 KeyError
```

**集合运算**（O(min(len(a), len(b)))）：

```python
a & b   # 交
a | b   # 并
a - b   # 差
a ^ b   # 对称差
```

**常见用法**：去重、判断成员、O(1) 查找。

```python
names = ["a", "b", "a", "c"]
unique = list(set(names))   # 去重，但顺序丢失

# 保序去重（3.7+ dict 有序）
seen = set()
unique = []
for n in names:
    if n not in seen:
        seen.add(n)
        unique.append(n)
```

## 3.5 dict — 哈希映射

```python
d = {"name": "alice", "age": 30}
d["name"]              # 取
d.get("email", "")     # 取，缺省 ""
d["email"] = "a@b.c"   # 写
del d["age"]           # 删
"name" in d            # 查键

# 遍历
for k in d: ...
for k, v in d.items(): ...
for v in d.values(): ...
```

**字典推导式**：

```python
square = {x: x * x for x in range(5)}
```

**常用模式**：

```python
# 计数
from collections import Counter
cnt = Counter(["a", "b", "a", "c"])  # Counter({'a': 2, 'b': 1, 'c': 1})

# 分组
from collections import defaultdict
groups = defaultdict(list)
for name, group in items:
    groups[group].append(name)
```

## 3.6 集合选型

| 场景 | 选 |
|---|---|
| 顺序重要、要重复 | `list` |
| 不变记录、解构 | `tuple` |
| 成员查找、去重 | `set` |
| 键值映射 | `dict` |

## 3.7 拷贝

```python
a = [1, 2, [3, 4]]
b = a             # 引用，不是拷贝
b.append(5)
print(a)          # [1, 2, [3, 4], 5]    同一个对象

b = a.copy()      # 浅拷贝（一层）
b.append(6)
print(a)          # [1, 2, [3, 4], 5]   外层独立
b[2].append(7)
print(a)          # [1, 2, [3, 4, 7], 5]  内层仍共享

import copy
c = copy.deepcopy(a)  # 深拷贝（递归）
```

> 默认参数陷阱（与拷贝相关，阶段 2 详讲）：

```python
# 错：默认参数只求值一次
def add(item, bucket=[]):
    bucket.append(item)
    return bucket

add(1)  # [1]
add(2)  # [1, 2]  同一个 bucket

# 对
def add(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```
