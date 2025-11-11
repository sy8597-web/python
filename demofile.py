# demofile.py

# 쓰기
# f = open('demofile.txt', 'wt', encoding='utf-8')
# f.write('첫번째\n두번째\n세번째\n')
# f.close()

# # 읽기
# f = open('demofile.txt', 'rt', encoding='utf-8')        
# content = f.read()
# print(content)  
# f.close()

# 문자열 데이터 처리메서드
data = '  spam and ham'
result = data.strip()
print(data)
print(result)
result2 = result.replace('ham', 'ham egg')
print(result2)
list = result2.split()
print(list)
print(':)'.join(list))

print(len('abcd'))
print('hello'.upper())
print('HELLO'.lower())  
print('2580'.isdecimal())
print('hello world'.find('world'))      

# 정규표현식
import re

# 선택한 주석을 주석 처리 : ctrl + 
result = re.match('[0-9]*th', '35th')
print(result)
print(result.group())

result = re.search('[0-9]*th', '35th')
print(result)
print(result.group())
                  

# 단어 검색
result = re.search('apple', 'this is apple')
print(result.group())

result = re.search('\d{4}', ' 올해는 2025년입니다.')
print(result.group())

result = re.search('\d{5}', ' 우리동네는 51000입니다.')
print(result.group())