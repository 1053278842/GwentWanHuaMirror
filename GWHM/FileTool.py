import binascii
import json
import os
import pymem
from PIL import ImageFont,ImageDraw,ImageFile,Image,ImageTk

# 写入卡片json源文件
def writeCardDataJsonBaseFile():
    base = 0x24713aa8018
    count = 0x42b0c*2
    value = pm.read_bytes(base,count)
    result=""
    for item in value:
        result += str(hex(item))[2:].zfill(2).upper()
    print(result)

    with open('text_utf16.txt', 'r',encoding='utf-16') as fp:
        fp.write(binascii.unhexlify(result))
    return 0

# CardData源文件转化为Json
def CardDataFileToJson():
    data = {}
    with open('CN.txt', 'r', encoding='utf-8') as inFile:
        # 第二种：每行分开读取
        count = 0
        id = ""
        description = ""
        name = ""
        tip = ""
        for line in inFile:
            data_line = line.strip("\n")  # 去除首尾换行符，并按空格划分
            count += 1
            if count == 1:
                id = data_line[0:6]
                description = data_line[14:-1]
            elif count == 2:
                name = data_line[12:]
            elif count == 3:
                count = 0
                tip = data_line[15:]
                data[str(id)] = {'name':name,"description":description,"tip":tip}
                # print(tip)
            # data2.append([int(i) for i in data_line])    
    with open("card_json.json", 'w',encoding='utf16') as write_f:
        write_f.write(json.dumps(data, indent=4, ensure_ascii=False))

def Cpp2liTransBean(path,fileName,ClassName):
    data = {}
    with open(path, 'r', encoding='utf-8') as inFile:
        # 属性标识
        START_FLAG = "Field:"
        # 存放搜索到的属性
        attrList =[]
        # 临时变量
        name = ""
        typeName = ""
        offset = ""
        rows = 0
        counts = 30
        num = 0
        for line in inFile:
            data_line = line.strip("\n").strip()  # 去除首尾换行符，并按空格划分
            head_str = data_line[0:6]
            # print(data_line,head_str)
            if head_str == START_FLAG:
                name = data_line[7:]
                rows = 2
            elif rows == 2:
                typeName = data_line[6:]
                rows = 3
            elif rows == 3:
                offset = data_line[25:]
                rows = 0
                attrList.append({'name':name,'typeName':typeName,'offset':offset})

        # for attr in attrList:
        #     print(attr)
        AutoSetAttrName(attrList)
        WriteBeanByAttrList(fileName,attrList,ClassName)

# 根据传入的列表[字典]中的name,typeName,自动过滤、修改合适的name
def AutoSetAttrName(attrList):
    CHANGE_NAME_FLAG = "k__BackingField"
    index = 0
    for attr in attrList:
        index += 1
        if attr["name"][-15:] == CHANGE_NAME_FLAG:
            temp_name = "{typeName}_{index}".format(typeName=attr["typeName"], index=index)
            temp_name = temp_name.replace(".",'_')
            attr["name"] = temp_name

# attrList 是一个列表，其元素是字典。格式严格要求为：{name:,typeName:,offset:}
def WriteBeanByAttrList(fileName,attrList,className):   
    with open(fileName+".py", 'w') as write_f:
        # print("class {className1}(object):def __init__(self):".format(className1=className))
        code_str = "class {className}(object):\n\n\tdef __init__(self):\r".format(className=className)
        # 输出init变量名和偏移
        for attr in attrList:
            code_str += "\t\tself._{name} = {offset}\n".format(name=attr["name"],offset=attr["offset"])
        # 生成set get函数
        code_str += "\n"
        for attr in attrList:
            code_str += "\t@property\n\tdef {name}(self):\n\t\treturn self._{name}\n".format(name=attr["name"])
            code_str += "\t@{name}.setter\n\tdef set(self,{name}):\n\t\tself._{name}={name}\n".format(name=attr["name"])
            code_str += "\n"
        # 生成toString函数
        code_str += "\tdef toString(self):\n\t\tprint("
        ROW_MAX_ATTR_LEN = 2
        count = 0
        for attr in attrList:
            # 第一个没逗号
            if attrList[0] == attr:
                code_str += '"{name}:",hex(self._{name}),"\\n"'.format(name=attr["name"])
            code_str += ',"{name}:",hex(self._{name}),"\\n"'.format(name=attr["name"])
            count += 1
            if count == ROW_MAX_ATTR_LEN:
                count = 0
                code_str += "\r"
        code_str += ")"
        write_f.write(code_str)

def getCardDataJsonDict():
    cardDict = open("GWHM/card_json.json", "r",encoding="utf-16")
    return json.loads(cardDict.read())

# 图片相关
# 图片爬取在其他文件
############################## ############################### ############################### ############################### #
# 压缩图片文件
def compress_image(outfile, mb=5, quality=85, k=0.9): # 通常你只需要修改mb大小
    """不改变图片尺寸压缩到指定大小
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标,KB
    :param k: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
 
    o_size = os.path.getsize(outfile) // 1024  # 函数返回为字节，除1024转为kb（1kb = 1024 bit）
    print('before_size:{} after_size:{}'.format(o_size, mb))
    if o_size <= mb:
        return outfile
    
    ImageFile.LOAD_TRUNCATED_IMAGES = True  # 防止图像被截断而报错
    
    while o_size > mb:
        im = Image.open(outfile)
        x, y = im.size
        out = im.resize((int(x*k), int(y*k)), Image.ANTIALIAS)  # 最后一个参数设置可以提高图片转换后的质量
        try:
            out.save(outfile, quality=quality)  # quality为保存的质量，从1（最差）到95（最好），此时为85
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024
    return outfile

# 批量压缩图片
def bath_img_compress():
    # 批量压缩图片
    path = r'././GwentImg/' # 待压缩图片文件夹
    for img in os.listdir(path):
        compress_image(path + str(img))

# 裁剪成deck缩略横图
def crop_img_to_deck(path,outPath,height_start_rate):
    img = Image.open(path)
    x,y = img.size
    target_y = y * height_start_rate
    region = img.crop((0,target_y,x,target_y+50))
    region.save(outPath)

# 批量裁剪图片
def bath_img_crop(in_path,out_path,height_start_rate):

    #OS创建文件夹
    img_file_path="././GwentImg_deck_small"
    img_file_path = out_path
    if not os.path.exists(img_file_path):
        os.makedirs(img_file_path)

    # 批量裁剪图片
    path = r'././GwentImg/' # 待压缩图片文件夹
    path = in_path
    for img in os.listdir(path):
        crop_img_to_deck(path + str(img),img_file_path+"/"+img,height_start_rate)

# 按照分辨率压缩图片
def compress_image_by_resize(path,outPath,quality):
    im = Image.open(path)
    (x, y) = im.size  # 读取图片尺寸（像素）
    x_1 = 400  # 定义缩小后的标准宽度
    y_1 = int(y * x_1 / x)  # 计算缩小后的高度
    out = im.resize((x_1, y_1), Image.Resampling.LANCZOS)  # 改变尺寸，保持图片高品质
    out.save(outPath,quality=quality)
    
# 批量压缩图片-分辨率
def bath_img_compress_by_resize(in_path,out_path,quality):
    # 批量压缩图片
    for img in os.listdir(in_path):
        compress_image_by_resize(in_path + str(img),out_path+img.replace(".jpg",".jpg"),quality)

# 拼接卡组预览缩略图
def composite_deck_preview(in_path,out_path):
    layer_core = Image.open(in_path).convert('RGBA')   # 底图背景
    layer_mask = Image.open("Images/deck_preview/deck_preview_mask.png").convert('RGBA')    # mask
    layer_frame = Image.open("Images/deck_preview/deck_preview_golden_frame.png").convert('RGBA')    # frame
    layer_start = Image.open("Images/deck_preview/deck_preview_star.png").convert('RGBA')    # frame

    final = Image.new("RGBA", layer_frame.size)             # 合成的image
    final.paste(layer_core, (0,2) , layer_core)
    final.paste(layer_mask, (0,0) , layer_mask)
    final.paste(layer_frame,(0,0) ,layer_frame)
    final.paste(layer_start,(15,14) ,layer_start)
    
    final = final.convert('RGB')
    final.save(out_path)

# 批量片接卡组预览缩略图
def bath_composite_preview(in_path):
    # 批量压缩图片
    for img in os.listdir(in_path):
        composite_deck_preview(in_path + str(img),in_path + str(img))

# 返回拼接详细信息
def composite_deck_info(in_path,provision,name):

    layer_bg = Image.open(in_path).convert('RGBA')   # 底图
    draw = ImageDraw.Draw(layer_bg)
    # Provision
    font = ImageFont.truetype("FontFile/NEOESPORT-2.ttf",26)
    draw.text((55,35),str(provision),(226,167,61),font=font,anchor="mm",align="center")
    # Name
    font = ImageFont.truetype("FontFile/JZJDCYJF.ttf",20)
    draw.text((70,34),str(name),(213,215,213),font=font,anchor="ls",align="left")

    layer_bg = layer_bg.convert('RGB')
    # layer_bg.save("2.jpg")
    return layer_bg

# 根据卡牌参数返回deck预览缩略图，并调整大小
def get_deck_preview_img(id,provision,name,scale_factor):
    imgPath = 'GwentImg_preview/'+str(id)+".jpg"
    img = composite_deck_info(imgPath,provision,name)
    # 缩放
    x, y = img.size
    out = img.resize((int(x*scale_factor), int(y*scale_factor)), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(out)


# 生成ImageTk调整调整大小
def get_img_resized(path,scale_factor):
    img = Image.open(path)
    x,y = img.size
    out = img.resize((int(x*scale_factor),int(y*scale_factor)),Image.Resampling.LANCZOS) 
    return ImageTk.PhotoImage(out)


# 创建卡组缩略图的临时存放文件，并生成
def create_deck_preview_temp_file(curr_memo_cards,scale_factor):

    path = "deck_preview_temp"
    img_file_path="deck_preview_temp"
    file_has_template_id_list = []
    for fileName in os.listdir(img_file_path):
        file_has_template_id_list.append(int(fileName[0:5]))
    if not os.path.exists(img_file_path):
        os.makedirs(img_file_path)
    for key in curr_memo_cards:
        template_id = int(curr_memo_cards[key]["Id"])
        if template_id not in file_has_template_id_list:
            template_provision =curr_memo_cards[key]["Provision"]
            template_name = curr_memo_cards[key]["Name"]
            scale_factor = scale_factor
            imgTk = get_deck_preview_img(template_id,template_provision,template_name,scale_factor)
            img = ImageTk.getimage(imgTk)
            save_path = path+"/"+str(template_id)+".png"
            img.save(save_path)

# 获取暗淡效果的卡牌缩略图
def get_img_hidden_effect(path,effect_factor = 0.7):
    img = Image.open(path)
    img = img.point(lambda p:p * effect_factor)
    return img
def get_img(path):
    return Image.open(path)
def get_img(path):
    return Image.open(path)

############################## ############################### ############################### ############################### #
# 获取程式模块基址
def get_baseAddress():
    global pm
    global baseAddress
    pm = pymem.Pymem("Gwent.exe")
    baseAddress = pymem.process.module_from_name(
        pm.process_handle,"GameAssembly.dll"
    ).lpBaseOfDll

def main():
    get_baseAddress()

if __name__ =='__main__':
    #################
    # getCardDataJsonDict()
    #################

    # 压缩图片
    # bath_img_compress()

    # 分辨率批量压缩图片
    # bath_img_compress_by_resize(r'GwentImg原图/',r"Card_Img_Small/",50)

    # 裁剪图片
    # crop_img_to_deck()

    # 批量裁剪图片
    # bath_img_crop("Card_Img_Small/","GwentImg_preview/",0.25)

    # 合成卡组预览图
    # composite_deck_preview("GwentImg_preview/1.jpg","1.jpg")
    # bath_composite_preview("GwentImg_preview/")
    # composite_deck_info("1.jpg",9,"约翰·卡尔维特")
    # # # # # # #  # # # # 
    main()
