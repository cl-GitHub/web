# coding:utf-8
import xlrd


class Excel:
    def __init__(self, excelpath):
        self.test_data_path = excelpath

    def open_excel(self, file):
        u"""读取excel文件"""
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception as e:
            raise e

    def excel_table(self, file, sheetname, isInt):
        u"""装载list"""
        data = self.open_excel(file)
        # 通过工作表名称，获取到一个工作表
        table = data.sheet_by_name(sheetname)
        # 获取行数
        Trows = table.nrows
        # 获取 第一行数据
        Tcolnames = table.row_values(0)
        lister = []
        for rownumber in range(1, Trows):
            row = table.row_values(rownumber)
            if row:
                app = {}
                for i in range(len(Tcolnames)):
                    # 判断python读取的返回类型  0 --empty,1 --string, 2 --number(都是浮点), 3 --date, 4 --boolean, 5 --error
                    ctype = table.cell(rownumber, i).ctype
                    if isInt:
                        if ctype == 2:
                            app[Tcolnames[i]] = str(int(row[i]))
                        else:
                            app[Tcolnames[i]] = row[i]
                    else:
                        app[Tcolnames[i]] = row[i]
                lister.append(app)
        return lister

    def get_list(self, sheetname, isInt=True):
        try:
            data_list = self.excel_table(self.test_data_path, sheetname, isInt)
            assert len(data_list) >= 0, u'excel标签页:' + sheetname + u'为空'
            return data_list
        except Exception as e:
            raise e
