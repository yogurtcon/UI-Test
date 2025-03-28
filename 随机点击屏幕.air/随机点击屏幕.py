# 正确的顺序是：先连接设备（一般在 auto_setup 接口里面连接）--> 再打开应用（一般用 start_app 接口）--> 等应用开启完毕，最后才初始化 poco。
# -*- encoding=utf8 -*-
__author__ = "作者名称"

import os
from airtest.core.api import auto_setup, connect_device, stop_app, wake, start_app, sleep, touch, log
import webbrowser
from airtest.report.report import simple_report
import random
import logging

# 每次运行前清空log目录
import shutil

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(current_dir, 'log')

# 如果log目录存在则删除
if os.path.exists(log_dir):
    shutil.rmtree(log_dir)
# 创建新的log目录    
os.makedirs(log_dir)

# 设置日志级别为INFO，这样DEBUG级别的日志就不会被输出
logging.getLogger('airtest').setLevel(logging.INFO)
auto_setup(__file__, logdir=True, devices=["android:///",])
dev=connect_device("android:///")

try:
    # 使用Airtest的get_current_resolution接口获取当前设备的屏幕分辨率
    screen_size = dev.get_current_resolution()
    log(screen_size)
    
    # 定义顶部和底部的安全区域（这个可以先手动点点看，哪些地方要点，哪些不要，以此来的得到可点击的范围）
    top_margin = screen_size[1] * 0.0378378  # 顶部区域不点击
    bottom_margin = screen_size[1] * 0.939459  # 底部区域不点击
    
    log(f"有效点击区域Y轴范围: {top_margin} - {bottom_margin}")

    for _ in range(5):
        # 进行随机点击，避开顶部和底部区域
        x = random.randint(0, screen_size[0])
        y = random.randint(int(top_margin), int(bottom_margin))
        touch((x, y))
        sleep(0.5)  # 等待一段时间

finally:

    # 报告文件路径
    report_name = '随机点击屏幕'
    # 使用绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(current_dir, report_name + '.html')
    # 确保log目录存在
    log_dir = os.path.join(current_dir, 'log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    simple_report(__file__, logpath=log_dir, output=report_path)

    import re

    # 读取HTML文件
    with open(report_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式查找并替换标题
    new_content = re.sub(r'<title>.*?</title>', f'<title>{report_name}</title>', content, flags=re.I)

    # 将修改后的内容写回文件
    with open(report_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

    # 确保报告文件存在
    if os.path.exists(report_path):
        # 使用webbrowser打开报告文件
        webbrowser.open('file://' + os.path.realpath(report_path))
    else:
        print(f"报告文件{report_path}不存在，请先生成报告。")


