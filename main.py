
import itertools
import pandas as pd


def dynloop_num(lens, rem, pace, cur_y_idx , lst_rst = [], lst_tmp = []):

    max_y_idx = lens -1  # 获取Y 轴最大索引值

    if ((rem == pace) and cur_y_idx == max_y_idx):
        lst_tmp.append(  rem / 100 )
        lst_rst.append([*lst_tmp])
        lst_tmp.pop()
        return lst_rst

    else:
        for i in range(pace, rem, pace):  # 遍历当前位置的所有的成分占比

            lst_tmp.append(i / 100)  # 将当前层所含比例元素追加到lst_tmp 中

            if cur_y_idx == max_y_idx:  # 如果当前层是最底层则将lst_tmp 作为元素追加到lst_rst 中

                lst_tmp[max_y_idx] = rem / 100
                lst_rst.append([*lst_tmp])
                lst_tmp.pop()
                break

            else:  # 如果当前还不是最底层则Y 轴+1 继续往下递归，所以递归最大层数就是Y 轴的最大值
                # lst_rst 和lst_tmp 的地址也传到下次递归中，这样不论在哪一层中修改的都是同一个list 对象
                dynloop_num(lens, rem - i, pace, cur_y_idx + 1, lst_rst, lst_tmp)
            lst_tmp.pop()  # 在本次循环最后，不管是递归回来的，还是最底层循环的，都要将lst_tmp 最后一个元素移除

    return lst_rst


def dynloop_fomula(lens, cur_y_idx , start , lst_rst = [], lst_tmp = [] ):

    max_y_idx = lens - 1  # 获取Y 轴最大索引值

    end = start + textpos[cur_y_idx]

    for i in range(start,end):  # 遍历当前位置的所有的成分占比

        lst_tmp.append(newcomplexdata[i])

        if cur_y_idx == max_y_idx:  # 如果当前层是最底层则将lst_tmp 作为元素追加到lst_rst 中

            a = []
            for j in lst_tmp:
                a = a + j
            lst_rst.append([*a])

        else:  # 如果当前还不是最底层则Y 轴+1 继续往下递归，所以递归最大层数就是Y 轴的最大值
            # lst_rst 和lst_tmp 的地址也传到下次递归中，这样不论在哪一层中修改的都是同一个list 对象
            dynloop_fomula(lens,  cur_y_idx + 1, end,  lst_rst, lst_tmp)
        lst_tmp.pop()  # 在本次循环最后，不管是递归回来的，还是最底层循环的，都要将lst_tmp 最后一个元素移除

    return lst_rst



data = pd.read_csv('testdata.csv',header=0)

i = 0
j = 0
tot = 0
complexdata = []
position = []

while(i < data.shape[1]):#排列组合部分

    if ('position' in data.columns[i]):

        hang = data.values[:,i].tolist()

        z = 0

        while(z < len(hang)):

            if type(hang[z]) == float:

                del hang[z:len(hang)]

                break

            z+=1

        k = itertools.combinations(hang, int(data.loc[j, 'repeat']))

        for l in k:
            complexdata.append(l)

        position.append(len(complexdata)-tot)

        tot = len(complexdata)

        j += 1

    i+=1





plong = len(position)   #化合物多少位置
i = 0
point = 0
newcomplexdata = []
textpos = []
while(i < plong):

    hole = int(data.loc[i, 'hole']) * 100
    pace = int(data.loc[i, 'range']) * 100
    haha = []
    hehe = []
    numarray = complexdata[point]
    if hole == pace:
        back = hole/100
    else:
        back = dynloop_num(len(numarray),hole,pace,0,haha,hehe)

    count = 0

    for j in range(point , point+position[i]):
        if type(back) == float:
            temp = list(complexdata[j])
            temp.append(back)
            newcomplexdata.append(temp)
            count+=1

        else:
            for k in back:
                temp = list(complexdata[j]) + list(k)
                newcomplexdata.append(temp)
                count+=1
    textpos.append(count)

    point += position[i]
    i+=1




haha = []
hehe = []

back = dynloop_fomula(len(textpos), 0, 0,  haha, hehe)

work = pd.DataFrame(back)

dcb = pd.read_csv('Periodic Table of Elements.csv',header=0,index_col=1)

fdcb = []

title = []

for i in range(len(back)):

    tmp = []
    for j in range(len(back[i])):

        if type(back[i][j]) == str:

            if i ==0:

                title.extend(dcb)

            tmp.extend(dcb.loc[back[i][j]])

    fdcb.append(tmp)

a = pd.DataFrame(fdcb)

rst = pd.concat([work,a],axis=1,ignore_index=True)
print(rst)
rst.to_csv('output.csv',index=False,header=False)













'''
layers = [[1,2],[11,12,13],[-1,-2]]
    shape = [len(layer) for layer in layers]
    offsets = [0] * len(shape)
    has_next = True
    while has_next:
        record = [layers[i][off] for i,off in enumerate(offsets)]
        print(record)
        for i in range(len(shape) - 1, -1, -1):
            if offsets[i] + 1 >= shape[i]:
                offsets[i] = 0  # 重置并进位
                if i == 0:
                    has_next = False  # 全部占满，退出
            else:
                offsets[i] += 1
                break
    print('complete')
'''











