# demoFunction.py

def setValue(newValue):
    x = newValue
    print('함수내부: ', x)

# 함수를 호출
retValue = setValue(5)
print(retValue)

# 함수를 정의
def swap(x,y):
    return y,x

# 호출
result = swap(3,4)
print(result)



# 디버깅연습 함수
def intersect(prelist, postlist):
    result = []
    for x in prelist:
        if x in postlist and x not in result:
            result.append(x)
    return result

# 호출
print(intersect("ham",'spam'))


# LGB
# 전역변수
x = 5
def func(a):
    return a + x
print(func(1))

def func2(a):
    # 지역변수
    x = 10
    return a+x


print(func2(1))