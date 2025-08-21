class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        return x


myclass = MyNumbers()
myiter = iter(myclass)



print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

# !/usr/bin/python3

import sys


def fibonacci(n):           # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a            #函数会返回当前的倒数值，并在下一次调用时从上次暂停的地方继续执行。
        a, b = b, a + b
        counter += 1


f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成

while True:
    try:
        print(next(f), end=" ")
    except StopIteration:
        sys.exit()