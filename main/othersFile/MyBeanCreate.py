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

# Cpp2liTransBean(r"C:\Users\Administrator\Desktop\cpp2il_out\types\Assembly-CSharp\BattleSettings_metadata.txt", "GWHM/TestBean/Bs","Bs")
# Cpp2liTransBean(r"C:\Users\Administrator\Desktop\cpp2il_out\types\Assembly-CSharp\PlayerSettings_metadata.txt", "GWHM/TestBean/PS","Ps")
# Cpp2liTransBean(r"C:\Users\Administrator\Desktop\cpp2il_out\types\Assembly-CSharp\PlayerInfo_metadata.txt", "GWHM/TestBean/Pi","Pi")
# Cpp2liTransBean(r"C:\Users\Administrator\Desktop\cpp2il_out\types\Assembly-CSharp\BattleDeck_metadata.txt", "GWHM/TestBean/Bd","Bd")
# Cpp2liTransBean(r"C:\Users\Administrator\Desktop\cpp2il_out\types\Assembly-CSharp\BoardSideSettings_metadata.txt", "GWHM/TestBean/Bss","Bss")
# Cpp2liTransBean(r"C:\Users\Administrator\Desktop\cpp2il_out\types\Assembly-CSharp\CardData_metadata.txt", "GWHM/TestBean/Cd","cd")




