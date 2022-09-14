a = [3,2,5,4,1,6]
b = [3,1,2,5,4,6]

for i in range(0,len(a)):
    if a[i] != b[i]:
        if i+1 < len(a):
            if a[i+1] == b[i]:
                print(a[i],"moved forward")
                break
            else:
                print(b[i],"moved backward")
                break

print("移动到新数列的位置：",b.index(1))
        