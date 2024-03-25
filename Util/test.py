import os

# 当前文件的绝对路径
abs_path = os.path.abspath(__file__)

# 项目根目录的绝对路径
root_path = os.path.dirname(abs_path)

root_path = os.path.dirname(root_path)

print(abs_path, root_path)