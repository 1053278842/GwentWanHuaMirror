from PIL import Image

def is_progressive(image_path):
    try:
        # 打开图片
        image = Image.open(image_path)
        
        # 检查图像的格式是否支持渐进式
        if image.format not in ('JPEG', 'PNG'):
            return False
        
        # 检查是否有 "progressive" 属性
        if 'progressive' not in image.info:
            return False
        
        # 获取 "progressive" 属性的值
        progressive = image.info['progressive']
        
        # 判断是否为渐进式
        return bool(progressive)
    
    except IOError:
        # 图片打开错误
        return False

# 示例用法
image_path = '11.jpg'  # 请替换为你的图片路径
if is_progressive(image_path):
    print("这张图片'是'渐进式的")
else:
    print("这张图片'不是'渐进式的")
