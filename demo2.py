# -*- coding: utf-8 -*-
# @Time : 2022/5/21 21:23
# @Author : 任浩天，吴闽杰
# @File : Demo1_mian.py
import operator
op=['+','-','@','/','=']#"@"是“*”
def is_op(opea):
    if opea in op:
        return True
    else:
        return False
def isalphas(factor):
    if factor.isalpha() or is_op(factor):
        return True
    else:
        return False
#自定义一个栈的结构
class Stack:
    def __init__(self):            #栈的初始化
        self.items = []
    def is_empty(self):            #判断栈是否为空
        return self.items == []
    def size(self):                #获取栈中元素的个数
        return len(self.items)
    def push(self,item):           #入栈
        self.items.append(item)
    def pop(self):                 #出栈并获取栈顶元素
        return self.items.pop()
    def peek(self):                #获取栈顶元素
        if len(self.items):
            return self.items[len(self.items)-1]
        return None
    def print_stack(self):         #打印栈
        pass
#定义符号的优先级
def priority(str):
    dic = {}
    dic[1] = -1
    for i in str:
        if isalphas(i) :
            dic[i] = 0
        elif i == '|':
            dic[i] = 1
        elif i == '·':
            dic[i] = 2
        elif i == '*':
            dic[i] = 3
    return dic
#给正规式添加连接运算的符号
def add_and(str):
    ls = list(str)+['!']
    length = len(ls)
    i = 0
    while ls[i] != '!':
        if isalphas(ls[i]) and isalphas(ls[i+1]):
            ls.insert(i+1, "·")
            i += 1
        if isalphas(ls[i]) and ls[i+1] == "(":
            ls.insert(i+1,"·")
            i += 1
        if ls[i] == ")" and isalphas(ls[i+1]):
            ls.insert(i+1,"·")
            i += 1
        if ls[i] == "*" and isalphas(ls[i+1]):
            ls.insert(i+1,"·")
            i += 1
        if ls[i] == ")" and ls[i+1] == "(":
            ls.insert(i+1,"·")
            i += 1
        if ls[i] == "*" and ls[i+1] == "(":
            ls.insert(i+1,"·")
            i += 1
        i += 1
    del ls[-1]
    newstr = ''.join(ls)
    return newstr
#实现由中缀表达式到逆波兰表达式(后最表达式)
def ie_to_se(str):
    stack_sign = Stack()                #符号栈
    stack_sign.push(1)                  #提前在栈底压入一个最低级的符号
    str_add_sign = add_and(str)         #得到加入链接符号后的str
    dic_priority = priority(str_add_sign)#得到每个元素的优先级
    ls = []                              #记录后缀表达式的列表
    for i in str_add_sign:
        if isalphas(i):
            ls.append(i)
        else:
            if i == '(':
                stack_sign.push(i)
            elif i == ')':
                a = stack_sign.pop()
                while True:
                    if a != '(':   #把符号'('上的全部符号弹出
                        ls.append(a)
                        a = stack_sign.pop()
                    else:
                        break
            else:                 #符号除了')'的其他符号
                while 1:          #如果符号栈中有'('就要把在其之上符号优先级>=此刻符号的符号出栈加入到后缀式
                    if stack_sign.peek() == '(':
                        stack_sign.push(i)
                        break
                    else:
                        if dic_priority[stack_sign.peek()] >= dic_priority[i]:#栈顶元素的优先级大于此时将要进入符号栈的优先级（出栈）
                            b=stack_sign.pop()
                            ls.append(b)
                        else:
                            stack_sign.push(i)
                            break
    c = stack_sign.pop()#把符号栈中所有元素出栈
    while c!=1:
        ls.append(c)
        c = stack_sign.pop()
    return ls
#定义节点状态类
class State:
    def __init__(self, ID, start=None, end=None):
        self.ID = ID
        self.start = start
        self.end = end
#创建NFA的move表:ls_state为move列表（NFA的move表），k为边的左状态ID，values为接受的字符，j为右状态ID
def creat_LS_move(ls_state, k, values, j):
    dict1 = {}      #外围字典
    dict2 = {}     #内围字典
    dict2[values] = j  #定义右端点
    dict1[k] = dict2     #定义左状态
    ls_state.append(dict1)
#只是一个元素
def is_alpha(k, cnt_State, values, ls_state):
    a = State(k)           #构建状态a
    b = State(k + 1)       #构建状态b
    creat_LS_move(ls_state, k, values, k + 1)
    return State(cnt_State, a, b), ls_state
#对两个元素进行或运算
def is_or(k, cnt_State, state1, state2, ls_state):
    a = State(k)
    b = State(k + 1)
    creat_LS_move(ls_state, k, 'ε', state1.start.ID)
    creat_LS_move(ls_state, k, 'ε', state2.start.ID)
    creat_LS_move(ls_state, state1.end.ID, 'ε', b.ID)
    creat_LS_move(ls_state, state2.end.ID, 'ε', b.ID)
    return State(cnt_State, a, b), ls_state
#对两个元素进行连接运算
def is_and(k, cnt_State, valuea,state1, ls_state):
    b = State(k)
    num=state1.end.ID
    creat_LS_move(ls_state, num, valuea, b.ID)
    return State(cnt_State, state1.start, b), ls_state
#对两个元素进行闭包运算
def is_repeat(k, cnt_State, state1, ls_state):
    a = State(k)
    b = State(k + 1)
    creat_LS_move(ls_state, k, 'ε', state1.start.ID)
    creat_LS_move(ls_state, state1.end.ID, 'ε', state1.start.ID)
    creat_LS_move(ls_state, state1.end.ID, 'ε', b.ID)
    creat_LS_move(ls_state, k, 'ε', b.ID)
    return State(cnt_State, a, b), ls_state
#将后缀表达式变为NFA
def se_to_NFA(ls):#ls为后最表达式
    ls=ls+['#']  #添加#作为结束符号
    stack_NFA = Stack()
    begin = 1      #开始状态
    D_num = 0      #默认数字
    ls_state = []
    index=0
    while(index<len(ls)):#遍历后缀表达式
        if ls[index]=='#':
            break
        else:
            if isalphas(ls[index]) and ls[index + 1] != '·':#创建状态边
                state, ls_state = is_alpha(begin, D_num, ls[index], ls_state)
                stack_NFA.push(state)
                begin += 2  #初始态
                index +=1
            elif ls[index]== '*':#闭包一目运算，取出一个个状态边
                state1 = stack_NFA.pop()
                state, ls_state = is_repeat(begin, D_num, state1, ls_state)
                stack_NFA.push(state)
                begin += 2
                index += 1
            elif ls[index] == '|':#二目运算，取出两个状态边
                state1 = stack_NFA.pop()
                state2 = stack_NFA.pop()
                state, ls_state = is_or(begin, D_num, state2, state1, ls_state)
                stack_NFA.push(state)
                begin += 2
                index += 1
            elif (isalphas(ls[index]) and ls[index+1] == '·'):#连接运算
                values=ls[index]  #得到字符
                state1 = stack_NFA.pop()
                state, ls_state = is_and(begin, D_num, values,state1, ls_state)
                stack_NFA.push(state)
                begin += 1
                index += 2
    final_state = stack_NFA.pop()
    return final_state.start.ID, final_state.end.ID, ls_state
'''
    从NFA到DFA
'''
class Nfa:
    def __init__(self, start, end, move):
        self.start = start
        self.accepted = end
        self.move = move

    # 进行闭包运算,ls为状态集，u为ls状态集的闭包
    def make_Closure(self, ls):
        u = []
        stack = Stack()
        for i in ls:  # 先把状态集全部压入栈
            stack.push(i)
            u.append(i)
        while not (stack.is_empty()):
            i = stack.pop()  # 取出栈顶元素
            for d in self.move:  # 遍历状态表，如果存在空符号，则压入栈
                if d.get(i) != None:
                    if 'ε' in d.get(i):
                        a = d.get(i)['ε']
                        if a not in u:
                            stack.push(a)
                            u.append(a)
                    else:
                        pass
        return u

    # make_move方法求子集，ls为初态集，char为转换字符，u为转换后的集合
    def make_move(self, ls, char):
        u = []
        for i in ls:
            for d in self.move:
                if d.get(i) != None:
                    if char in d.get(i):
                        a = d.get(i)[char]
                        if a not in u:
                            u.append(a)
        #                     elif 'ε' in d.get(i):

        return u

    # 获得NFA的开始状态，结束状态，以及move列表
    def get_startendmove(self, ls):
        return se_to_NFA(ls)

    # 获得NFA的字母列表
    def get_alpha(self, ls):
        ls1 = []
        for i in ls:
            if isalphas(i) and i not in ls1:
                ls1.append(i)
        return ls1

class Dfa:
    def __init__(self,N,ls):
        self.Dfa_state_start = N.make_Closure([N.start])   #DFA的初态
        self.Dfa_statelist = [self.Dfa_state_start]        #存DFA的状态表
        self.Dfa_stateflag = {0:0}                         #记录DFA是否别标记过
        self.Dfa_state_accepted = N.accepted               #DFA的终态
        cnt = 0                                            #记录下标
        cnt_state = 0                                      #状态数字
        dt = {}                                            #方便检查
        ls_ans = []                                        #存
        ls_accepted = []
        ls_notaccepted = []
        ls1 = N.get_alpha(ls)                              #获取后缀表达式中的字母
        # 判断终态是在终结态里还是非终态里
        if N.accepted in self.Dfa_state_start:
            ls_accepted = [0]
        else:
            ls_notaccepted = [0]
        while cnt <= cnt_state and self.Dfa_stateflag[cnt] == 0:
            dt[cnt] = tuple(self.Dfa_statelist[cnt])
            for char in ls1:#遍历每个符号
                tup = tuple(N.make_Closure(N.make_move(self.Dfa_statelist[cnt],char)))#经过符号后产生的集合再做闭包运算
                for i in range(len(ls1)):
                    if char == ls1[i]:
                        dic = {}
                        dic1 = {}
                        dic1[char] = tup   #存放在字典里
                        dic[cnt] = dic1
                        ls_ans.append(dic)#存放在列表里
                        break
                if tup not in self.Dfa_statelist and tup != () and self.is_numright(list(tup), self.Dfa_statelist)!=1:#确认新的状态集不在Dfa_statelist中
                    self.Dfa_statelist.append(tup)#加入
                    cnt_state += 1
                    self.Dfa_stateflag[cnt_state] = 0;#添加标记
                    if N.accepted in tup and cnt_state not in ls_accepted: #判断终态与非终态
                        ls_accepted.append(cnt_state)                      #包含nfa终态则将状态数字加入终态数字集
                    elif cnt_state not in ls_notaccepted:
                        ls_notaccepted.append(cnt_state)                   #不包含nfa终态则将状态数字加入非终态数字集
            self.Dfa_stateflag[cnt] = 1
            cnt += 1
        self.dt = dt#状态集合标号数组:
        self.move = self.trans_second(ls_ans,dt)
        self.ls_accepted = ls_accepted
        self.ls_notaccepted = ls_notaccepted
        self.dic1 = dic1
        self.ls1 = ls1#后缀表达式中的字母
    def trans(self,dt):   #dfa转移表
        dic1 = {}
        for i in dt.keys():
            tu = dt[i]
            dic1[tu] = i
        return dic1
    def trans_second(self,ls,dt):
        ls1 = []
        for i in ls:
            for j in i:#开始状态
                dic = i[j]#存放结束状态
                for m in dic:#转移字符
                    for n in dt:#状态数字
                        if dt[n] == dic[m]:#判断是否有组状态集合标号
                            dic[m] = n
        for i in ls:
            for j in i:
                dic = i[j]
                for m in dic:
                    if dic[m] != ():
                        ls1.append(i)
        return ls1
    def is_numright(self,list1,list2):
        for i in list2:
            if set(list1).issubset(set(i)) and set(i).issubset(set(list1)):
                flag = 1
                break
            else:
                flag = 0
        return  flag
'''
    DFA化简
'''
class toMiniDfa:
    flag_mark = 1
    length = 0
    Region = []  # 记录分区（所有划分）
    dic_region = {}
    standard = []
    dic_regionstandard = {}
    dic_regionstandard_accepted = {}
    dic_regionstandard_notaccepted = {}

    def __init__(self, ls_notaccepted, ls_accepted, ls, move, dic1, dic_goal):
        self.accepted = []  #
        self.notaccepted = []  #
        self.length = len(ls_notaccepted) + len(ls_accepted) #记录总状态数
        self.Region.append(ls_notaccepted)  #添加非终态划分
        self.Region.append(ls_accepted)  #添加终态划分
        self.accepted.append(ls_accepted)  #记录非终态划分
        self.notaccepted.append(ls_notaccepted)  #记录终态划分
        self.dic_region[1] = ls_notaccepted  #记录非终态划分
        self.dic_region[2] = ls_accepted  #记录终态划分
        self.flag_notaccepted = 1
        self.cnt = 2
        self.flag = 1
        while self.flag == 1:
            self.dic_regionstandard = {}
            self.dic_regionstandard_accepted = {}
            self.dic_regionstandard_notaccepted = {}
            self.flag = 0
            if self.flag_notaccepted == 1:
                for i in self.less_ls(self.Region, self.accepted):  # 遍历每一个划分
                    dic_tempor = {}
                    for j in i:  # 遍历划分中的每一个状态
                        ls1 = []
                        for index in range(len(ls)):  # ls字母表
                            ls0 = []
                            ls0.append(self.get_goal(ls[index], move, j, dic1, self.dic_region))#获取下一状态所在划分
                            ls1.append(ls0)
                        dic_tempor[j] = ls1  #{0：[2]...}存下一状态所在划分
                        if j == i[0]:
                            for x in self.dic_region:#遍历划分
                                if i == self.dic_region[x]:#
                                    self.dic_regionstandard[x] = ls1
                                    self.dic_regionstandard_notaccepted[x] = ls1#记录非终态集所产生的划分
                    cnt = 0
                    while cnt < len(i):
                        if self.is_equal(dic_tempor[i[cnt]], dic_tempor[i[0]]) == 0:
                            self.flag = 1
                            t = self.is_inotherregion(self.dic_regionstandard_notaccepted, dic_tempor[i[cnt]])
                            if t != None:
                                for n in self.dic_regionstandard:
                                    if n == t:
                                        self.dic_region[n].append(i[cnt])
                                        self.dic_regionstandard[n] = self.add_region(self.dic_regionstandard[n],
                                                                                     dic_tempor[i[cnt]])
                                        self.dic_regionstandard_notaccepted[n] = self.add_region(
                                            self.dic_regionstandard[n], dic_tempor[i[cnt]])
                            else:
                                ls2 = []
                                ls2.append(i[cnt])
                                self.Region.append(ls2)
                                self.notaccepted.append(ls2)
                                self.cnt += 1
                                self.dic_region[self.cnt] = ls2
                                self.dic_regionstandard[self.cnt] = dic_tempor[i[cnt]]
                                self.dic_regionstandard_notaccepted[self.cnt] = dic_tempor[i[cnt]]
                            for m in self.dic_region:
                                if i[cnt] in self.dic_region[m]:
                                    self.dic_region[m].remove(i[cnt])
                                    break
                        else:
                            cnt += 1
            self.flag_notaccepted = 0
            if self.flag_notaccepted == 0:
                ls20 = self.less_ls(self.Region, self.notaccepted)
                for i in ls20:  # 遍历每一个分区
                    dic_tempor = {}
                    for j in i:  # 遍历分区中的每一个状态
                        ls1 = []
                        for index in range(len(ls)):
                            ls0 = []
                            ls0.append(self.get_goal(ls[index], move, j, dic1, self.dic_region))
                            ls1.append(ls0)
                        dic_tempor[j] = ls1
                        if j == i[0]:
                            for x in self.dic_region:
                                if i == self.dic_region[x]:
                                    self.dic_regionstandard[x] = ls1
                                    self.dic_regionstandard_accepted[x] = ls1
                    cnt = 0
                    while cnt < len(i):
                        if self.is_equal(dic_tempor[i[cnt]], dic_tempor[i[0]]) == 0:
                            self.flag = 1
                            t = self.is_inotherregion(self.dic_regionstandard_accepted, dic_tempor[i[cnt]])
                            if t != None:
                                for n in self.dic_regionstandard:
                                    if n == t:
                                        self.dic_region[n].append(i[cnt])
                                        self.dic_regionstandard[n] = self.add_region(self.dic_regionstandard[n],
                                                                                     dic_tempor[i[cnt]])
                                        self.dic_regionstandard_accepted[n] = self.add_region(
                                            self.dic_regionstandard[n], dic_tempor[i[cnt]])

                            else:
                                ls2 = []
                                ls2.append(i[cnt])
                                self.Region.append(ls2)
                                self.accepted.append(ls2)
                                self.cnt += 1
                                self.dic_region[self.cnt] = ls2
                                self.dic_regionstandard[self.cnt] = dic_tempor[i[cnt]]
                                self.dic_regionstandard_accepted[self.cnt] = dic_tempor[i[cnt]]
                            for m in self.dic_region:
                                if i[cnt] in self.dic_region[m]:
                                    self.dic_region[m].remove(i[cnt])
                                    break
                        else:
                            cnt += 1
                self.flag_notaccepted = 1
        self.accepted1, self.notaccepted1 = self.trans_second(self.accepted, self.notaccepted)

        self.move ,self.dic= self.get_move(move, self.dic_region)
    def get_move(self, ls, dt):

        ls1 = []
        dic1 = {}
        dic2 = {}
        cnt=1
        for l in dt:
            if len(dt[l])!=0:
                dic2[cnt] = dt[l]
                cnt+=1
        # for l in list(dt):
        #     if len(dt[l]) == 0:
        #         del dt[l]
        for i in ls:
            for j in i:  # 开始状态
                dic = i[j]  # 存放{'a': 2}
                for m in dic:  # 遍历结束状态
                    for n in dic2:  # 状态数字
                        list1 = dic2[n]
                        if list1 != None:
                            for p in list1:
                                if p == dic[m]:  # 判断是否有组状态集合标号
                                    dic[m] = n
        for i in ls:
            for j in i:
                for n in dic2:  # 状态数字
                    list1 = dic2[n]
                    if list1 != None:
                        for p in list1:
                            if p == j:  # 判断是否有组状态集合标号
                                dic1[n] = i[j]
                                ls1.append(dic1)
                                dic1 = {}
                    else:
                        dic1[i] = j
                        ls1.append(dic1)
                        dic1 = {}
        return ls1,dic2


    #输出划分结果
    def print_ans(self):
        print(self.dic)

    # 去除划分中重复状态
    def less_ls(self, ls1, ls2):
        ls = []
        ls = ls1[:]
        for i in ls2:
            for j in ls:
                if tuple(j) == tuple(i):
                    ls.remove(j)
        return ls

    # dic_goal是状态分表,获取输入状态通过某输入字符可以到达的状态所在划分
    def get_goal(self, char, move, state, dic1, dic_goal):  #字母表，dfa转移表，当前划分状态集，分区中的一个状态，dic1,总的划分
        cnt = 0
        cnt1 = 0
        cnt2 = 0
        for i in move:
            if i.get(state) != None:
                cnt1 += 1
                dic = i.get(state)
                if dic.get(char) != None:
                    for j in dic_goal:
                        if dic.get(char) in dic_goal[j]:
                            return j
                else:
                    cnt2 += 1
            else:
                cnt += 1
        if cnt == len(move):#判断是否无状态可到达
            return -1
        if cnt1 == cnt2:#判断是否不能到达任何一个已有划分中状态
            return -1

    def is_inotherregion(self, dic_regionstandard, ls):  # 分出去的分区是否在已经分好的分区
        dic = self.trans(dic_regionstandard)
        for i in dic:
            ls1 = []
            for j in i:
                ls0 = []
                ls0 = list(j)
                ls1.append(ls0)
            if self.is_equal(ls1, ls) == 1:
                return dic[i]

    def trans(self, dic_regionstandard):#格式转换{0：[2]...}->
        dic = {}
        for i in dic_regionstandard.keys():
            ls1 = []
            for j in dic_regionstandard[i]:
                tup = tuple(j)
                ls1.append(tup)
            tu = tuple(ls1)
            dic[tu] = i
        return dic

    def trans_second(self, accepted, notaccepted):
        accepted1 = []
        notaccepted1 = []
        for t in range(len(accepted)):
            for i in self.dic_region:
                if self.dic_region[i] == accepted[t]:
                    accepted1.append(i)
        for t in range(len(notaccepted)):
            for i in self.dic_region:
                if self.dic_region[i] == notaccepted[t]:
                    notaccepted1.append(i)
        return accepted1, notaccepted1

    def is_equal(self, ls1, ls2):
        flag = 0
        flag1 = 0
        for i in range(len(ls1)):
            if operator.eq(ls2[i], ls1[i]):
                flag1 += 1
            if operator.eq(ls2[i], ls1[i]) and ls2[i] != [-1]:
                for j in range(i):
                    if ls2[j] == [-1]:
                        flag += 1
                for j in range(i + 1, len(ls1)):
                    if ls2[j] == [-1]:
                        flag += 1
                if flag == len(ls1) - 1:
                    return 1
                flag = 0
                for j in range(i):
                    if ls1[j] == [-1]:
                        flag += 1
                for j in range(i + 1, len(ls1)):
                    if ls1[j] == [-1]:
                        flag += 1
                if flag == len(ls1) - 1:
                    return 1
        if flag1 == len(ls1):
            return 1
        else:
            return 0

    def add_region(self, ls1, ls2):
        for i in range(len(ls1)):
            if ls1[i] == [-1]:
                if ls2[i] != -1:
                    ls1[i] = ls2[i]
        return ls1

#将正规式变为NFA|
str='(a|b|x|y|z)*|=|@|+'

str1 = add_and(str)
print("加入乘法点（即连接符号）的表达式：{0}".format(str1))
ls=ie_to_se(str1)
print("转成逆波兰表达式（即后缀表达式）：{0}".format(ls))
start,end,Ls_state = se_to_NFA(ls)#得到初态，终态和转移图
print('初态:',start,'终态',end)
print("转成nfa：")
for i in Ls_state:
    print(i)
# 将NFA变为DFA
N = Nfa(start,end,Ls_state)#初始状态，终态，nfa转移表
D = Dfa(N,ls)              #nfa,后缀表达式
a = D.move
print("状态集合标号数组:")
for i in D.dt.keys():
    print(i,D.dt[i])
print("dfa转移表：")
for i in D.move:
    print(i)
print("终态为：{0}".format(D.ls_accepted))

MD = toMiniDfa(D.ls_notaccepted,D.ls_accepted,D.ls1,D.move,D.dic1,D.dt)#f非终态，终态，字母表，状态转移表，
print("最小化后DFA的终态为：{0}".format(MD.accepted1))
print("最小化后dfa的非终态为：{0}".format(MD.notaccepted1))
print("最小化后dfa的分组为：{0}".format(MD.dic))


'''
驱动器算法
'''
MDFA=MD.move
for i in MDFA:
    print(i)
def get_alphas(ls_dic):#得到转移表的可接受字母有哪些
    ls1=[]
    for i in ls_dic:
        for d in i.values():
           for m in d.keys():
               if m not in ls1:
                   ls1.append(m)
    return ls1
def judge(str,MDFA):#判断是否有词法错误
    ls=get_alphas(MDFA)
    for i in str:
        if i not in ls:
            return False
def move(MDFA,state,char):#state为初始态，char为识别的字符
    #得到以state为出发的状态转移边
    LS=[]
    nextstate=None
    for d in MDFA:#拿出那些以state为起点的状态转移集
       for k in d.keys():
          if state==k:
              LS.append(d)
    if len(LS)==0:#如果state状态不能转移到任何状态就返回False
        return False
    for d in LS:#返回如果state能够经过char得到后的状态
        for v in d.values():
            if char in v.keys():
                nextstate=v.get(char)
                return nextstate
    if  nextstate==None:
        return False
def Driver(MDFA, str):
    LS1 = []#记录变量
    LS2 = []#记录关键符
    str1 = ''
    state = 1
    i=0
    while(i<len(str)):
        if i==len(str)-1:
            if move(MDFA, state, str[i])==False:
                if state==2:
                    LS1.append(str1)
                elif state==3:
                    LS2.append(str1)
                elif move(MDFA, 1 ,str[i])==2:
                    LS1.append(str[i])
                elif move(MDFA, 1 ,str[i])==3:
                    LS2.append(str[i])
                break
            else:
                if  move(MDFA, state, str[i])==2:
                    LS1.append(str+str[i])
                elif move(MDFA, state, str[i])==3:
                    LS2.append(str+str[i])
                break
        else:
            state2 = move(MDFA, state, str[i])
            if state2!= False:
                str1 = str1+str[i]
                state = state2
                i=i+1
            elif state2==False:#不能继续跳转
                if state==2:#达到的状态是变量
                    LS1.append(str1)
                    state = 1
                    str1 = ''
                elif state==3:#达到的状态是关键符
                    LS2.append(str1)
                    state = 1
                    str1 = ''
    return LS1,LS2
# def handle(LS1):
#     LS2=[]
#     op = ['+', '-', '*', '/', '=']
#     for i in range(len(LS1)):
#         if LS1[i]=='@':
#             LS1[i]="*"
#     for i in LS1:
#         if i in op:
#             LS2.append(i)
#             LS1.remove(i)
#     return LS1,LS2
str='abb=abba+y*z'
str=str.replace('*','@')
if judge(str,MDFA)==False:
    print("输入的表达式有误")
else:
    Ls1,Ls2=Driver(MDFA,str)
    print('变量:',Ls1)
    print('关键符号：',Ls2)