# 导入必要的模块
import subprocess  # 用于执行系统命令
import os  # 用于文件和目录操作

# 设置基础目录为当前目录（.）
base_dir = '.'
# 初始化用例计数器
i = 0

# 使用os.walk遍历所有目录
# root: 当前目录路径
# dirs: 当前目录下的子目录列表
# files: 当前目录下的文件列表
for root, dirs, files in os.walk(base_dir):
    # 遍历所有子目录
    for dir_name in dirs:
        # 查找包含"主流程"且以".air"结尾的目录
        if '主流程' in dir_name and dir_name.endswith('.air'):
            # 构建完整的.air目录路径
            air_dir_path = os.path.join(root, dir_name)
            # 遍历.air目录下的所有文件
            for py_file in os.listdir(air_dir_path):
                # 只处理.py文件
                if py_file.endswith('.py'):
                    # 用例计数加1
                    i = i + 1
                    # 构建完整的Python文件路径
                    py_file_path = os.path.join(air_dir_path, py_file)
                    # 打印当前执行的用例信息
                    print(f"用例{i} {py_file_path}")
                    # 使用subprocess执行Python文件
                    subprocess.run(['python', py_file_path])
