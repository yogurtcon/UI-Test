# 正确的顺序是：先连接设备（一般在 auto_setup 接口里面连接）--> 再打开应用（一般用 start_app 接口）--> 等应用开启完毕，最后才初始化 poco。
# -*- encoding=utf8 -*-
__author__ = "作者名称"

import os
from airtest.core.api import auto_setup, connect_device, stop_app, wake, start_app, sleep, touch, log, swipe
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

def get_safe_area(screen_size):
    """获取安全的操作区域"""
    # 定义顶部和底部的安全区域
    top_margin = screen_size[1] * 0.0378378
    bottom_margin = screen_size[1] * 0.939459
    
    return {
        'x_min': 0,
        'x_max': screen_size[0],
        'y_min': int(top_margin),
        'y_max': int(bottom_margin)
    }

def random_swipe(safe_area):
    """执行随机滑动操作"""
    # 在安全区域内随机选择起点和终点
    start_x = random.randint(safe_area['x_min'], safe_area['x_max'])
    start_y = random.randint(safe_area['y_min'], safe_area['y_max'])
    end_x = random.randint(safe_area['x_min'], safe_area['x_max'])
    end_y = random.randint(safe_area['y_min'], safe_area['y_max'])
    
    # 执行滑动
    swipe((start_x, start_y), (end_x, end_y))
    log(f"执行滑动操作: ({start_x}, {start_y}) -> ({end_x}, {end_y})")

def random_touch(safe_area):
    """执行随机点击操作"""
    # 在安全区域内随机选择点击位置
    x = random.randint(safe_area['x_min'], safe_area['x_max'])
    y = random.randint(safe_area['y_min'], safe_area['y_max'])
    touch((x, y))
    log(f"执行点击操作: ({x}, {y})")

try:
    # 获取屏幕分辨率
    screen_size = dev.get_current_resolution()
    log(f"屏幕分辨率: {screen_size}")
    
    # 获取安全操作区域
    safe_area = get_safe_area(screen_size)
    log(f"安全操作区域: {safe_area}")
    
    # 定义操作类型
    operations = ['touch', 'swipe']
    
    # 执行随机操作
    for _ in range(5):  # 执行5次随机操作
        # 随机选择操作类型
        operation = random.choice(operations)
        
        if operation == 'touch':
            random_touch(safe_area)
        elif operation == 'swipe':
            random_swipe(safe_area)
            
        # 随机等待时间
        sleep(random.uniform(0, 1))

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


