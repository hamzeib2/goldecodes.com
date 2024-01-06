
preferace = {'clothes':0 , 'EGIFT Card': 0,'Book':0 ,'Fashion':0 , 'Electronic':0 , 'Mobiles':0 , 'shoes':0 }
trans =[["['Book'", " 'Mobiles'", " 'clothes']"], ["['Book'", " 'Mobiles'", " 'clothes']"], ["['Book'", " 'Mobiles'", " 'clothes']"], ["['Book'", " 'Mobiles'", " 'clothes']"], ["['Book'", " 'Mobiles'", " 'clothes']"], ["['Fashion'", " 'Mobiles'", " 'clothes']"], ["['Mobiles'", " 'clothes'", " 'EGIFT Card']"], ["['Mobiles'", " 'clothes'", " 'EGIFT Card']"], ["['Electronic'", " 'Mobiles'", " 'clothes']"], ["['Fashion'", " 'Electronic'", " 'Mobiles']"], ["['Book'", " 'Fashion'", " 'Electronic']"]]
t = []
for i in trans:
    listt = [item.strip("[ ]") for item in i]
    l = [item.strip(" '' ") for item in listt]
    t.append(l)
for i in t:
    for j in i:
        preferace[j] +=1

print(preferace)
key = sorted(preferace.keys() , key=lambda x: x , reverse=True)
sorrted_preferance = sorted(preferace.items() , key = lambda x: x[1] , reverse=True)
sd = []
sk = []
for i in sorrted_preferance:
        for j in i:
                #print(j)
            sd.append(j)
#         if j == key:
#             sd.append(j)

for i in sd:
    for j in key:
        if i == j:
            sk.append(i)
#print(sk)
    co = 0
    pre = []
    for i in sk:
        if co>2:
            break
        else:
            pre.append(i)
            co +=1

print(pre)


# pr = ['a','d']

# arr = {'a':0 , 'b':0 , 'c':0 , 'd':0}
# for i in pr:
#     arr[i]+=1
# print(arr)

# sorrted_preferance = sorted(arr.items() , key = lambda x: x[1] , reverse=True)
# print(sorrted_preferance)
# r =  dict(sorrted_preferance)
# print(r['a'])

# # rr = dict(["('a", '1)', "('d", '1)', "('b", '0)', "('c", '0)'])
# # print(rr)
# def append_prefer_in_file(prefer):
   
#     with open( "prjapp/test_file/prefer.text","a") as f:
#         # outfile.writelines(order.date_orderd.strftime("%d/%m/%y")+"-")
#         pre = str(prefer)
#         f.writelines(pre)
#         f.writelines("\n")

# prefer =[('a', 1), ('d', 1), ('b', 0), ('c', 0)]
# append_prefer_in_file(prefer)


# def get_prefer_from_file():
#     transactions=[]
    
#     with open("prjapp/test_file/prefer.text","r") as outfile:
#         for line in outfile:
#             line=outfile.readline().strip()
#             if line == "":
#                 continue
#             line=line.split(',')
#             if ''  in line:
#                 line.remove('')
#             if '[]'  in line:
#                 line.remove('')
#             transactions.append(line)
#     if transactions != []:
#         te = transactions[len(transactions)-1]
#         listt = [item.strip("[ ]") for item in te]
#         l = [item.strip(" '' ") for item in listt]
#         ll = [item.strip(" ( ) ") for item in l]
#         lll = [item.strip(" '' ") for item in ll]
        
#     else:
#         te = []   
#     print("trans")
    
#     print(te)
    
#     return lll


# te = get_prefer_from_file()
# print(te)
# # for i in te:
# #     print(i)

# t = dict(te)
# print(t)
