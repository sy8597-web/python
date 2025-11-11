# demoRandom.py

import random

print(random.random())  # 0.0 ~ 1.0 미만의 임의의 부동 소수점 숫자 생성
print(random.random())  
print(random.uniform(2.0, 5.0))  
print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])
print([random.sample(range(20), 10)])
print([random.sample(range(20), 10)])

# 로또
print(random.sample(range(1,46), 5))

from os.path import *
import os

fileName = "c:\\python310\\python.exe"
print(basename(fileName))
print(abspath(fileName))

if exists(fileName):
    print("파일 크기:", os.path.getsize(fileName))
else:
    print("파일이 존재하지 않습니다.")  
    

