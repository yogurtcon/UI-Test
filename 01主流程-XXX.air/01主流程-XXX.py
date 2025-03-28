# 正确的顺序是：先连接设备（一般在 auto_setup 接口里面连接）--> 再打开应用（一般用 start_app 接口）--> 等应用开启完毕，最后才初始化 poco。

# -*- encoding=utf8 -*-
__author__ = "作者名称"

from airtest.core.api import *
import webbrowser
from airtest.report.report import simple_report
from poco.exceptions import PocoNoSuchNodeException
import logging

# 每次运行前清空log目录
import shutil
import os

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

try:

    # 指定包名
    PKG = "com.XXX.XXX"

    # 先关掉app再重新启动
    stop_app(PKG)
    wake()
    start_app(PKG)
    
    sleep(4)
	
	from poco.drivers.android.uiautomation import AndroidUiautomationPoco
	poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
	
	log("——————用例1——————", snapshot=True)
	try:
		poco("XXX").child("XXX").child()[-1].click()
		touch([1, 1])
		shell("input text 'a'")
		keyevent("ENTER")
		swipe([0.5, 0.5], [0.5, 0.1], duration=1.0)
	except PocoNoSuchNodeException as e:
		log(e, desc="失败")
	
	
	log("——————用例2——————", snapshot=True)
	try:
		if poco("XXX").exists():
			poco("XXX").click()
		else:
			log("未找到元素XXX", snapshot=True)
	except PocoNoSuchNodeException as e:
		log(e, desc="失败")

finally:

	# 报告文件路径
	report_name = '01主流程-XXX'
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


