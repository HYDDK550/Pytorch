file = open('example.txt', 'r')
try:
    content = file.read()
    # 处理文件内容
finally:
    file.close()


with open('example.txt', 'r') as file:
    content = file.read()
    print(content)
# 文件已自动关闭