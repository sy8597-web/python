# 리스트를연습

colors = ['red', 'blue', 'green']

print(len(colors))
print(type(colors))
colors.append('white')
colors.insert(1,'black')
print(colors)
colors.remove('red')
print(colors)
colors.sort()
print(colors)
colors.reverse()
print(colors)

#세트형식 연습

a = {1,2,3,3}
b = {3,4,4,5}

print(a.union(b))
print(a.intersection(b))
print(a.difference(b))


#튜플형식연습

tp = (10,20,30)
print(type(tp))
print(len(tp))
print(tp[0])

# 함수정의
def calc(a,b):
    return a+b, a*b

# 함수호출
result = calc(3,4)
print(result)

print("id: %s, name: %s" % ('kim', '김유신'))
args = (5,6)
print(calc(*args))

# 형식변환* (Type Casting)

a = set((1,2,3))

print(a)

b = list(a)
b.append(30)
print(b)

# demoDict.py
colors = {'apple':'red', 'banana':'yellow'}

# 검색
print(colors['apple'])
# 입력
colors['cherry'] = 'red'
print(colors)

# 삭제
del colors['apple']
print(colors)

for item in colors.items():
    print(item)