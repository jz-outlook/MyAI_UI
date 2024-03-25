import xlrd as xlrd



class OperationExcel:
    def __init__(self, file_name=None, service_sheet=None):
        self.file_name = file_name
        if service_sheet:
            self.sheet_id = int(service_sheet)
        else:
            self.sheet_id = 0
        self.data = self.get_data()

    # 获取sheets的对象
    def get_data(self):
        data = xlrd.open_workbook(self.file_name)
        tables = data.sheets()[int(self.sheet_id)]
        return tables

    # 获取单元格的行数
    def get_lines(self):
        tables = self.data
        return tables.nrows

    # 根据行号，找到该行的数据
    def get_row_values(self, row):
        tables = self.data
        row_data = tables.row_values(row)
        return row_data

    # 读取excel文件内容
    def read_excel(self):
        rows_length = self.get_lines()
        # 定义两个空列表，存放每行的数据
        all_rows = []
        rows_dict_list = []
        for i in range(rows_length):
            if i == 0:
                continue
            all_rows.append(self.get_row_values(i))
        for row in all_rows:
            lis = dict(zip(self.get_row_values(0), row))
            rows_dict_list.append(lis)
        return rows_dict_list



# service_case_path = "/Users/Wework/data.xls"
# api_data = OperationExcel(service_case_path).read_excel()
# print(api_data)