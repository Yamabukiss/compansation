from easygui import *

def uiDesign():
    msgbox("""
    本刀补轨迹生成软件采取读取文本文件(*.txt)来获取参数的形式
    蓝色为工件轨迹
    绿色为刀补轨迹
    """, "使用事项", "下一步")

    msgbox("""
    直线格式遵循:起点:x y 换行 终点:x y
    圆弧格式遵循:起点:x y 换行 终点:x y c_x c_y radius(直线接圆弧)
    圆弧格式遵循:起点:x y c_x c_y radius 换行 终点:x y(圆弧接直线)
    圆弧格式遵循:起点:x y c_x c_y radius 换行 终点:x y c_x c_y radius(圆弧接圆弧)
    """, "文件格式", "下一步")

    path = enterbox(msg="""
    请指定您的参数文件(*.txt)
    默认情况下认为参数文件与程序同目录，此时您可以直接输入文件名
    若在其他目录请输入绝对路径
    """, title='输入参数文件', default='line1.txt')

    type = ccbox('请选择刀补类型;G41(左刀补) G42(右刀补)',title="刀补类型",choices=['G41', 'G42'])
    offset = int(enterbox("请指定刀具半径", "刀具半径", "8"))
    workpieces = ccbox('请选择您的工件轨迹是否需要封闭',title="轨迹封闭",choices=["是","否"])

    return path, type, offset, workpieces
if __name__ == '__main__':
    uiDesign()