import os


class GetPath:

    def __init__(self):
        abs_path = os.path.abspath(__file__)
        root_path = os.path.dirname(abs_path)
        # 项目根目录的绝对路径
        self.path = os.path.dirname(root_path)

    def get_parent_directory(self):
        """获取当前工作目录的上级目录"""
        return os.path.dirname(os.getcwd())

    def get_mp3_path(self):
        path = self.path + '/data/mp3/temp.mp3'
        return str(path)

    def get_login_case_path(self):
        path = self.path + '/data/login/login.xls'
        return str(path)

    def get_data_case_path(self):
        path = self.path + '/data/data.xls'
        return str(path)



# 使用示例
mp3_directory = GetPath().get_mp3_path()
print(f"当前工作目录是: {mp3_directory}")
