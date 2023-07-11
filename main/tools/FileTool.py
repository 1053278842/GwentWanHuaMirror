import binascii
import json
import os

import pymem
from enums.GamePlatform import EGamePlatform
from enums.GwentEnum import CardType, Location, Rarity
from PIL import Image, ImageDraw, ImageFile, ImageFont, ImageTk


def resetVersionPlatformAddress(EGP):
    data = getVersion() 
    if EGP == EGamePlatform.GOG:
        data['address'] = data['addressGOG']
    elif EGP == EGamePlatform.GY:
        data['address'] = data['addressGY']
    elif EGP == EGamePlatform.STEAM:
        data['address'] = data['address']
    saveVersion(data)

def getGlobalConfig():
    cardDict = open(r"main/resources/config/global_config.json", "r",encoding="utf-8")
    return json.loads(cardDict.read())
def saveGlobalConfig(data):
    fp=open("main/resources/config/global_config.json","w",encoding="utf-8")
    json.dump(data,fp=fp,ensure_ascii=False)

def getVersion():
    cardDict = open(r"main/resources/config/version.json", "r",encoding="utf-16")
    return json.loads(cardDict.read())

def saveVersion(version):
    fp=open("main/resources/config/version.json","w",encoding="utf-16")
    json.dump(version,fp=fp,ensure_ascii=False)

def getCardDataJsonDict():
    cardDict = open(r"main/resources/config/card_json_local.json", "r",encoding="utf-8")
    return json.loads(cardDict.read())

def getCardDataJsonDict16():
    cardDict = open(r"main/resources/config/card_json_local.json", "r",encoding="utf-16")
    return json.loads(cardDict.read())

def getLeaderCardDataJsonDict():
    cardDict = open(r"main/resources/data/LeaderCardData.json", "r",encoding="utf-8")
    return json.loads(cardDict.read())

def getDeckDataJsonDict():
    cardDict = open(r"main/resources/data/decks.json", "r",encoding="utf-16")
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
    currPower =   info_dict["CurrPower"]
    factionId =   info_dict["FactionId"]
    abilityCardTemplateId = info_dict["Id"]
    excess = info_dict["Excess"]
    # 只对color起作用
    if excess:
        highlightType = info_dict["HighlightType"]
    else:
        highlightType = False
    # 如果是Leader卡
    if CardType(cardType) == CardType.LEADER:
        return composite_leader_card(provision,name,factionId,abilityCardTemplateId,excess,highlightType)
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
   
    
    final = Image.new("RGBA", layer_frame.size,(34, 34, 34, 0))             # 合成的image
    xCoords = 0
    if excess:
        xOffsetRate = 0.12
        xCoords = int(layer_frame.size[0] * xOffsetRate)
    final.paste(layer_core, (xCoords,2) , layer_core)
    final.paste(layer_mask, (xCoords,0) , layer_mask)
    final.paste(layer_frame,(xCoords,0) ,layer_frame)
    final.paste(layer_start,(xCoords+15,14) ,layer_start)
    if excess:
        # 前缀图标
        # 高度為54
        if highlightType == 1:
            layer_eye = Image.open(r"main/resources/images/deck_preview/view-eye-1.png").convert('RGBA')    # start
        else:
            layer_eye = Image.open(r"main/resources/images/deck_preview/view-eye-2.png").convert('RGBA')    # start
        layer_eye = layer_eye.resize((50,50), Image.Resampling.LANCZOS)
        final.paste(layer_eye,(0,2) ,layer_eye)
    
    layer_bg = final.convert('RGBA')
    ####################################################################################################################################
    # layer_bg = Image.open(in_path).convert('RGBA')   # 底图
    draw = ImageDraw.Draw(layer_bg)
    # Provision
    font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",26)
    draw.text((xCoords+55,35),str(provision),(226,167,61),font=font,anchor="mm",align="center")
    # Name
    font = ImageFont.truetype(r"main/resources/fonts/JZJDCYJF.ttf",20)
    # 白色
    color = (213,215,213) 
    if excess:
        if highlightType == 1:
            color = (129,218,116)
        else:
            color = (223,92,99)
    draw.text((xCoords+70,34),str(name),color,font=font,anchor="ls",align="left")
    # Power
    # 单位卡使用银/金【Power】前缀
    if ( rarity == Rarity.LEGENDARY.value or rarity == Rarity.EPIC ) and cardType == CardType.UNIT.value:
        # layer_start = Image.open(r"main/resources/images/deck_preview/deck_preview_star.png").convert('RGBA')    # start
        font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",26)
        draw.text((xCoords+25,35),str(currPower),(216,157,51),font=font,anchor="mm",align="center")
    elif cardType == CardType.UNIT.value:
        # layer_start = Image.open(r"main/resources/images/deck_preview/deck_preview_start_bronze.png").convert('RGBA')    # start
        font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",26)
        draw.text((xCoords+25,35),str(currPower),(213,215,213),font=font,anchor="mm",align="center")


    layer_bg = layer_bg.convert('RGB')

    return layer_bg

def composite_leader_card(provision,name,factionId,abilityCardTemplateId,excess,highlightType):
    # 框架
    layer_frame = Image.open(r"main/resources/images/deck_preview/leader-frame.png").convert('RGBA')
    # 遮罩
    layer_mask = Image.open(r"main/resources/images/deck_preview/deck_preview_mask.png").convert('RGBA')    # mask
    scale_factor = layer_frame.size[1]/layer_mask.size[1]
    xOffset = -int(layer_frame.size[0]*0.25)
    layer_mask = layer_mask.resize((layer_frame.size[0]+xOffset,layer_frame.size[1]), Image.Resampling.LANCZOS)
    # 技能标志
    layer_start = Image.open(r"main/resources/images/deck_preview/LeaderAbilityIco/{0}.png".format(abilityCardTemplateId)).convert('RGBA')
    scale_factor = layer_frame.size[0]/layer_start.size[0]*0.27
    layer_start = layer_start.resize((int(layer_start.size[0]*scale_factor), int(layer_start.size[1]*scale_factor)), Image.Resampling.LANCZOS)

    # 技能能量
    layer_prov = Image.open(r"main/resources/images/deck_preview/mulligan.png").convert('RGBA')
    scale_factor = layer_frame.size[0]/layer_prov.size[0]*0.25
    layer_prov = layer_prov.resize((int(layer_prov.size[0]*scale_factor), int(layer_prov.size[1]*scale_factor)), Image.Resampling.LANCZOS)
    # 填充背景
    layer_core = Image.open("main/resources/images/deck_preview/LeaderFactionBg/{0}.png".format(factionId)).convert('RGBA')
    scale_factor = layer_frame.size[1]/layer_core.size[1]
    layer_core = layer_core.resize((int(layer_core.size[0]*scale_factor), int(layer_core.size[1]*scale_factor)), Image.Resampling.LANCZOS)
    # layer_core = Image.new('RGBA', layer_frame.size, (0, 0, 0, 0))
    # 合成
    final = Image.new("RGBA", (layer_frame.size[0],layer_prov.size[1]),(34,34,34))
    xCoords = 0
    if excess:
        xOffsetRate = 0.12
        xCoords = int(layer_frame.size[0] * xOffsetRate)
    yOffset = int(abs(layer_prov.size[1] - layer_frame.size[1])/2)
    prov_xOffset = int(layer_frame.size[0]*0.02)
    final.paste(layer_core, (xCoords,2+yOffset) , layer_core)
    final.paste(layer_mask, (xCoords,0+yOffset) , layer_mask)
    final.paste(layer_frame,(xCoords,0+yOffset) ,layer_frame)
    final.paste(layer_start,(xCoords,0) ,layer_start)
    final.paste(layer_prov,(layer_frame.size[0]-layer_prov.size[0]-prov_xOffset,0) ,layer_prov)
    if excess:
        # 前缀图标
        # 高度為54
        if highlightType == 1:
            layer_eye = Image.open(r"main/resources/images/deck_preview/view-eye-1.png").convert('RGBA')    # start
        else:
            layer_eye = Image.open(r"main/resources/images/deck_preview/view-eye-2.png").convert('RGBA')    # start
        layer_eye = layer_eye.resize((50,50), Image.Resampling.LANCZOS)
        final.paste(layer_eye,(0,25) ,layer_eye)


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
    temp_x = xCoords + layer_start.size[0]
    temp_y = layer_prov.size[1]/2 + yOffset
    color = (240,240,240)
    if excess:
        if highlightType == 1:
            color = (129,218,116)
        else:
            color = (233,92,99)
    draw.multiline_text((temp_x,temp_y),str(name),color,font=font,anchor="ls",spacing=108)
    
    layer_bg = layer_bg.convert('RGB')
    
    return layer_bg

# 返回一个数组图片  
def get_num_img(size,color,name):

    layer_bg = Image.new('RGBA', (size[0], size[1]), (34, 34, 34, 0))
    draw = ImageDraw.Draw(layer_bg)
    font = ImageFont.truetype(r"main/resources/fonts/NEOESPORT-2.ttf",24)
    draw.text((size[0]/2,size[1]),str(name),color,font=font,anchor="mb",align="center")

    layer_bg = layer_bg.convert('RGB')
    return layer_bg

def getTextImg(size,color,name,fontSize):
    fontHeightPx = int(fontSize*1.333333)
    # layer_bg = Image.new('RGBA', (size, fontHeightPx), (180, 140, 120, 0))
    layer_bg = Image.new('RGBA', (size, fontHeightPx), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer_bg)
    font = ImageFont.truetype(r"main/resources/fonts/YSHaoShenTi-2.ttf",fontSize)
    draw.text((0,fontHeightPx),str(name),color,font=font,anchor="ld",align="left")

    layer_bg = layer_bg.convert('RGBA')
    return ImageTk.PhotoImage(layer_bg)

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

def getDarkCardPreviewImgTk(size,color):
    img = Image.new("RGBA", size,color)
    imgTk =ImageTk.PhotoImage(img)
    return imgTk

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
