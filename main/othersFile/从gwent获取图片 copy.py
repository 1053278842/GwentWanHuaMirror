import os
import json
import requests
from lxml import etree

import shutil
import os
import glob

folder_path = r'C:\mycode\vscode\GwentMirror\src\assets\card\art\preview\factor\ico'
custom_directory = r'C:\mycode\vscode\GwentMirror\src\assets\card\art\preview\tt'
destination_folder = r'C:\mycode\vscode\GwentWanHuaMirror\main\resources\images\GwentImg原图'
# 使用glob匹配源文件夹下的所有文件
files = glob.glob(os.path.join(folder_path, '*'))

# 遍历文件列表并复制文件到目标文件夹
for file in files:
    file_name = os.path.basename(file)[:6]+".jpg"
    destination_file = os.path.join(destination_folder, file_name)
    custom_file = os.path.join(custom_directory, file_name)
    print(custom_file)
    
    if os.path.exists(destination_file):
        print('Creating')
        shutil.copy2(destination_file, custom_file)

print("文件复制完成")
