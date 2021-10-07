in_data = "5 5\n[3, 1] [2, 2] [4, 4] [0, 1] [2, 4]\n[2, 3] [4, 1] [3, 0] [4, 3] [0, 2]\n[4, 2] [3, 1] [4, 0] [5, 0] [1, 0]\n[1, 4] [1, 3] [5, 3] [1, 1] [-1, -1]\n[2, 1] [3, 3] [2, 0] [1, 2] [3, 4]\n0 0 0 2 2\n0 2 3 0 2\n0 2 3 1 3\n0 2 0 2 0\n2 0 0 1 2"
split_data = in_data.split('\n')

XS, YS = split_data[0].split(' ')
POS = []
ROTATE = []

i = 1
while i != int(YS) + 1:
    POS.append([])
    e = split_data[i].replace(', ', ',').replace('[', '').replace(']', '')
    e2 = e.split(' ')
    for e3 in e2:
        e3 = e3.split(',')
        POS[i-1].append(((int)(e3[0]), (int)(e3[1])))
    i += 1

while i != int(YS) * 2 + 1:
    ROTATE.append([])
    e = split_data[i].split(' ')
    e = list(map(lambda x: int(x), e))
    for e2 in e:
        ROTATE[i-int(YS)-1].append(e2)
    i += 1

print(POS)
print(ROTATE)
