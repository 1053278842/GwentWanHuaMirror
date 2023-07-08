from PIL import Image
import os
import json

# 设置输入图片文件夹路径和输出雪碧图文件夹路径
input_folder = "downloaded_images/low雪碧图用"
output_folder = "downloaded_images/spritesheets"

# 设置每个卡片的宽度、高度
card_width = 150
card_height = 215

# 设置行数和每行的卡片数量
num_rows = 10
cards_per_row = 10

# 存储所有图片文件路径
image_files = []

# 遍历输入文件夹中的图片文件，并将路径添加到列表中
for filename in os.listdir(input_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        filepath = os.path.join(input_folder, filename)
        image_files.append(filepath)

# 创建空白雪碧图
spritesheet_width = card_width * cards_per_row
spritesheet_height = card_height * num_rows
spritesheet = Image.new("RGB", (spritesheet_width, spritesheet_height), (0, 0, 0, 0))
current_x = 0
current_y = 0
spritesheet_count = 1

def create_new_spritesheet():
    global spritesheet, current_x, current_y, spritesheet_count
    spritesheet_width = card_width * cards_per_row
    spritesheet_height = card_height * num_rows
    spritesheet = Image.new("RGB", (spritesheet_width, spritesheet_height), (0, 0, 0, 0))
    current_x = 0
    current_y = 0
    spritesheet_count += 1

# 初始化映射表
sprite_map = {}

# 遍历图片文件列表
for filepath in image_files:
    # 打开图片文件
    image = Image.open(filepath)

    # 缩放图片
    image = image.resize((card_width, card_height))

    # 获取文件名
    filename = os.path.basename(filepath)[:6]

    # 将当前卡片添加到雪碧图的对应位置
    spritesheet.paste(image, (current_x, current_y))

    # 将文件名添加到映射表中，并记录该卡片在雪碧图中的位置
    sprite_map[filename] = {"x": current_x, "y": current_y, "spriteName": f"spritesheet_{spritesheet_count}"}

    # 更新当前卡片的位置
    current_x += card_width
    if current_x >= spritesheet_width:
        current_x = 0
        current_y += card_height

    # 判断是否需要创建新的雪碧图
    if len(sprite_map) % (cards_per_row * num_rows) == 0:
        output_image = f"{output_folder}/spritesheet_{spritesheet_count}.jpg"
        spritesheet.save(output_image)

        create_new_spritesheet()

# 保存最后一个雪碧图
output_image = f"{output_folder}/spritesheet_{spritesheet_count}.jpg"
spritesheet.save(output_image)

# 输出映射表为 JSON 文件
sprite_map_path = "sprite_map.json"
with open(sprite_map_path, "w") as file:
    json.dump(sprite_map, file)
