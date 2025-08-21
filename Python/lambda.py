f = lambda: "Hello, world!"
print(f())  # 输出: Hello, world!

x = lambda a : a + 10
print(x(5))

y = lambda a, b : a * b
print(y(5, 6))

from functools import reduce

numbers = [1, 2, 3, 4, 5]

# 使用 reduce() 和 lambda 函数计算乘积
product = reduce(lambda x, y: x * y, numbers)

print(product)  # 输出：120