aa = [1, 2, 3, 4, 5]
bb = [1,2,3,7,8]
print([i for i in aa if i in bb])
print([i for i in aa if i not in bb])
print([i for i in bb if i not in aa])
# print(lambda bb.items(): x[1]["id"])
# 方法一：
# difference = list(set(bb).difference(set(aa)))  # bb中有而aa中没有的
# print (difference)

# 结果输出 [7, 8]