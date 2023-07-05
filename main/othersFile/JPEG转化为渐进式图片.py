from PIL import Image

def convert_to_progressive(image_path, output_path):
    try:
        # 打开图片
        image = Image.open(image_path)

        # 检查图像的格式是否为支持渐进式（JPEG和PNG）
        if image.format not in ('JPEG', 'PNG'):
            print("不支持的图片格式")
            return False

        # 将图片转换为渐进式
        image.save(output_path, format=image.format, progressive=True,quality=1000)
        print("图片已成功转换为渐进式")
        return True

    except IOError as e:
        # 图片打开错误
        print("图片打开错误:", str(e))
        return False

# 示例用法
image_path = '162303.jpg'  # 请替换为你的图片路径
output_path = '11.jpg'  # 输出的渐进式图片路径
convert_to_progressive(image_path, output_path)
