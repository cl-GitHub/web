# coding:utf-8
def get_float(f_str, n):
    """计算精度
    :param f_str:截取精度的数字
    :param n:精度长度
    """
    f_str = str(f_str)  # f_str = '{}'.format(f_str) 也可以转换为字符串
    a, b, c = f_str.partition('.')
    c = (c + "0" * n)[:n]  # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
    return ".".join([a, c])


def get_amount(amount):
    """去除数量中的千分位"""
    return amount.replace(",", "")
