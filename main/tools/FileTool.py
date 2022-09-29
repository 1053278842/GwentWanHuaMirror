import binascii
import json
import os
from enums.GwentEnum import CardType, Rarity,Location
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
    cardDict = open(r"main/resources/config/card_json.json", "r",encoding="utf-16")
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
    img_file_path = out_path
    if not os.path.exists(img_file_path):
        os.makedirs(img_file_path)

    # 批量裁剪图片
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
    layer_mask = Image.open(r"main/resources/images/deck_preview/deck_preview_mask.png").convert('RGBA')    # mask
    layer_frame = Image.open(r"main/resources/images/deck_preview/deck_preview_golden_frame.png").convert('RGBA')    # frame
    layer_start = Image.open(r"main/resources/images/deck_preview/deck_preview_star.png").convert('RGBA')    # frame

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
        print("为保证安全，该方法已经废弃.如要使用请到函数内接触注释！")
        # composite_deck_preview(in_path + str(img),in_path + str(img))

# 返回拼接详细信息
def composite_deck_info(in_path,info_dict):
    provision =   info_dict["Provision"]
    name      =   info_dict["Name"]
    cardType  =   info_dict["Type"]
    rarity    =   info_dict["Rarity"]
    location  =   info_dict["Location"]
    currPower =   info_dict["CurrPower"]
    # 如果是Leader卡
    if location == hex(Location.LEADER.value):
        return composite_leader_card(provision,name)
    ##############################################################################################################################
   
    layer_core = Image.open(in_path).convert('RGBA')   # 底图背景
    layer_mask = Image.open(r"main/resources/images/deck_preview/deck_preview_mask.png").convert('RGBA')    # mask

    if rarity == Rarity.LEGENDARY.value or rarity == Rarity.EPIC:
        layer_frame = Image.open(r"main/resources/images/deck_preview/deck_preview_golden_frame.png").convert('RGBA')    # frame
    else:
        layer_frame = Image.open(r"main/resources/images/deck_preview/deck_preview_bronze_frame1.png").convert('RGBA')    # frame
    if cardType ==CardType.STRATAGEM.value:
        # 重设Leader-frame 的高度
        default_frame_y = Image.open(r"main/resources/images/deck_preview/deck_preview_bronze_frame1.png").size[1]
        layer_frame = Image.open(r"main/resources/images/deck_preview/leader-frame.png").convert('RGBA')
        layer_frame = layer_frame.resize((layer_frame.size[0],default_frame_y), Image.Resampling.LANCZOS)

    ## 前缀
    # 特殊卡使用银/金【星】前缀
    layer_start = Image.new('RGBA', (23,25), (0, 0, 0, 0))
    if ( rarity == Rarity.LEGENDARY.value or rarity == Rarity.EPIC ) and cardType == CardType.SPECIAL.value:
        layer_start = Image.open(r"main/resources/images/deck_preview/deck_preview_star.png").convert('RGBA')    # start
    elif cardType == CardType.SPECIAL.value:
        layer_start = Image.open(r"main/resources/images/deck_preview/deck_preview_start_bronze.png").convert('RGBA')    # start
    # 单位卡使用银/金【Power】前缀
    # 因为是drawText，固在后段实现
    # 神器卡使用固定前缀
    if ( rarity == Rarity.LEGENDARY.value or rarity == Rarity.EPIC ) and cardType == CardType.ARTIFACT.value:
        layer_start = Image.open(r"main/resources/images/deck_preview/type_artifact_gold.png").convert('RGBA')    # start
        layer_start = layer_start.resize((27,30), Image.Resampling.LANCZOS)
    elif cardType == CardType.ARTIFACT.value:
        layer_start = Image.open(r"main/resources/images/deck_preview/type_artifact.png").convert('RGBA')    # start
        layer_start = layer_start.resize((27,30), Image.Resampling.LANCZOS)
    # 战略卡固定前缀
    if cardType ==CardType.STRATAGEM.value:
        layer_start = Image.open(r"main/resources/images/deck_preview/stratagem-gold-icon.png").convert('RGBA')    # start
        layer_start = layer_start.resize((27,30), Image.Resampling.LANCZOS)
   
    
    final = Image.new("RGBA", layer_frame.size)             # 合成的image
    final.paste(layer_core, (0,2) , layer_core)
    final.paste(layer_mask, (0,0) , layer_mask)
    final.paste(layer_frame,(0,0) ,layer_frame)
    final.paste(layer_start,(15,14) ,layer_start)
    
    layer_bg = final.convert('RGBA')
    ####################################################################################################################################
    # layer_bg = Image.open(in_path).convert('RGBA')   # 底图
    draw = ImageDraw.Draw(layer_bg)
    # Provision
    font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",26)
    draw.text((55,35),str(provision),(226,167,61),font=font,anchor="mm",align="center")
    # Name
    font = ImageFont.truetype(r"main/resources/fonts/JZJDCYJF.ttf",20)
    draw.text((70,34),str(name),(213,215,213),font=font,anchor="ls",align="left")
    # Power
    # 单位卡使用银/金【Power】前缀
    if ( rarity == Rarity.LEGENDARY.value or rarity == Rarity.EPIC ) and cardType == CardType.UNIT.value:
        # layer_start = Image.open(r"main/resources/images/deck_preview/deck_preview_star.png").convert('RGBA')    # start
        font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",26)
        draw.text((25,35),str(currPower),(216,157,51),font=font,anchor="mm",align="center")
    elif cardType == CardType.UNIT.value:
        # layer_start = Image.open(r"main/resources/images/deck_preview/deck_preview_start_bronze.png").convert('RGBA')    # start
        font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",26)
        draw.text((25,35),str(currPower),(213,215,213),font=font,anchor="mm",align="center")


    layer_bg = layer_bg.convert('RGB')
    # layer_bg.save("2.jpg")
    return layer_bg

def composite_leader_card(provision,name):
    # 框架
    layer_frame = Image.open(r"main/resources/images/deck_preview/leader-frame.png").convert('RGBA')
    # 遮罩
    layer_mask = Image.open(r"main/resources/images/deck_preview/deck_preview_mask.png").convert('RGBA')    # mask
    scale_factor = layer_frame.size[1]/layer_mask.size[1]
    xOffset = -int(layer_frame.size[0]*0.2)
    layer_mask = layer_mask.resize((layer_frame.size[0]+xOffset,layer_frame.size[1]), Image.Resampling.LANCZOS)
    # 技能标志
    layer_start = Image.open(r"main/resources/images/deck_preview/pmbm.png").convert('RGBA')
    scale_factor = layer_frame.size[0]/layer_start.size[0]*0.27
    layer_start = layer_start.resize((int(layer_start.size[0]*scale_factor), int(layer_start.size[1]*scale_factor)), Image.Resampling.LANCZOS)

    # 技能能量
    layer_prov = Image.open(r"main/resources/images/deck_preview/mulligan.png").convert('RGBA')
    scale_factor = layer_frame.size[0]/layer_prov.size[0]*0.25
    layer_prov = layer_prov.resize((int(layer_prov.size[0]*scale_factor), int(layer_prov.size[1]*scale_factor)), Image.Resampling.LANCZOS)
    # 填充背景
    layer_core = Image.open(r"main/resources/images/deck_preview/NR_full.png").convert('RGBA')
    scale_factor = layer_frame.size[1]/layer_core.size[1]
    layer_core = layer_core.resize((int(layer_core.size[0]*scale_factor), int(layer_core.size[1]*scale_factor)), Image.Resampling.LANCZOS)
    # layer_core = Image.new('RGBA', layer_frame.size, (0, 0, 0, 0))
    # 合成
    final = Image.new("RGBA", (layer_frame.size[0],layer_prov.size[1]))
    yOffset = int(abs(layer_prov.size[1] - layer_frame.size[1])/2)
    prov_xOffset = int(layer_frame.size[0]*0.02)
    final.paste(layer_core, (0,2+yOffset) , layer_core)
    final.paste(layer_mask, (0,0+yOffset) , layer_mask)
    final.paste(layer_frame,(0,0+yOffset) ,layer_frame)
    final.paste(layer_start,(0,0) ,layer_start)
    final.paste(layer_prov,(layer_frame.size[0]-layer_prov.size[0]-prov_xOffset,0) ,layer_prov)
    layer_bg = final.convert('RGBA')
    ####################################################################################################################################
    # layer_bg = Image.open(in_path).convert('RGBA')   # 底图
    draw = ImageDraw.Draw(layer_bg)
    # Provision
    font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",46)
    temp_x = layer_frame.size[0]-layer_prov.size[0]/2 - prov_xOffset
    temp_y = layer_prov.size[1]/2 + yOffset
    draw.text((temp_x,temp_y),str(provision),(0,0,0),font=font,anchor="mm")
    # Name
    font = ImageFont.truetype(r"main/resources/fonts/YSHaoShenTi-2.ttf",36)
    temp_x = layer_start.size[0]
    temp_y = layer_prov.size[1]/2 + yOffset
    draw.multiline_text((temp_x,temp_y),str(name),(240,240,240),font=font,anchor="ls",spacing=108)
    
    layer_bg = layer_bg.convert('RGB')
    # layer_bg.save("2.jpg")
    return layer_bg

# 返回一个数组图片  
def get_num_img(size,color,name):

    layer_bg = Image.new('RGBA', (size[0], size[1]), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer_bg)
    font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",26)
    draw.text((size[0]/2,size[1]),str(name),(40,40,40,50),font=font,anchor="mb",align="center")
    font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",25)
    draw.text((size[0]/2,size[1]),str(name),(20,20,20),font=font,anchor="mb",align="center")
    font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",24)
    draw.text((size[0]/2,size[1]),str(name),color,font=font,anchor="mb",align="center")

    layer_bg = layer_bg.convert('RGB')
    return layer_bg

def get_text_img(size,color,name):
    layer_bg = Image.new('RGBA', (size[0], size[1]), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer_bg)
    # font = ImageFont.truetype(r"main/resources/fonts/JZJDCYJF.ttf",26)
    # draw.text((size[0]/2,size[1]/2),str(name),(40,40,40,50),font=font,anchor="ma",align="center")
    # font = ImageFont.truetype(r"main/resources/fonts/JZJDCYJF.ttf",25)
    # draw.text((size[0]/2,size[1]/2),str(name),(20,20,20),font=font,anchor="ma",align="center")
    font = ImageFont.truetype(r"main/resources/fonts/JZJDCYJF.ttf",12)
    draw.text((size[0]/2,size[1]/2),str(name),color,font=font,anchor="ma",align="center")

    layer_bg = layer_bg.convert('RGB')
    return layer_bg

# 根据卡牌参数返回deck预览缩略图，并调整大小
def get_deck_preview_img(info_dict,scale_factor):
    id        =   info_dict["Id"]
    imgPath = 'main/resources/images/GwentImg_preview/'+str(id)+".jpg"
    img = composite_deck_info(imgPath,info_dict)
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

# 生成ImageTk，自定义xy,以及旋转角度
def get_imgTk_scaleXY_rotate(path,x,y,rotate):
    x,y = int(x),int(y)
    img = Image.open(path)
    img = img.resize((x,y)) 
    out = img.rotate(rotate)
    return ImageTk.PhotoImage(out)

# 生成ImageTk自定义x,y轴缩放倍数
def get_imgTk_xy(path,x,y):
    x,y = int(x),int(y)
    img = Image.open(path)
    out = img.resize((x,y)) 
    return ImageTk.PhotoImage(out)

# 生成ImageTk自定义x,y轴缩放倍数
def get_imgTk_xy_scale(path,x,y):
    x,y = int(x),int(y)
    img = Image.open(path)
    imgX,imgY = img.size
    out = img.resize((x,y),Image.Resampling.LANCZOS) 
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
    # bath_img_crop("Card_Img_Small/","GwentImg_preview/",0.25)     # 需要调整原图裁切高度请看这里！

    # 合成卡组预览图
    # composite_deck_preview("GwentImg_preview/1.jpg","1.jpg")
    # bath_composite_preview("GwentImg_preview/")
    # composite_deck_info("1.jpg",9,"约翰·卡尔维特")
    # # # # # # #  # # # # 
    main()
