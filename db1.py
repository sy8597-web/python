# db1.py

import sqlite3
# 연결객체
con = sqlite3.connect(r"c:\work\sample.db")

# 커서객체
cur = con.cursor()

# 테이블 생성
cur.execute("CREATE TABLE IF NOT EXISTS PhoneBook(name text, phoneNum text);")

# 데이터 삽입
cur.execute("INSERT INTO PhoneBook VALUES('홍길동', '010-1234-5678');")

# 입력파라메터 처리
name = '김철수'
phoneNum = '010-9876-5432'
cur.execute("INSERT INTO PhoneBook VALUES(?,?);", (name, phoneNum))

# 여러건 입력
datalist = (('이영희', '010-1111-2222'), ('박민수', '010-3333-4444'))
cur.executemany("INSERT INTO PhoneBook VALUES(?,?);", datalist)

# # 검색
# for row in cur.execute("SELECT * FROM PhoneBook;"):
#     print(row)


# 패치메서드 호출
cur.execute("SELECT * FROM PhoneBook;")
print("--- fetchone() ---")
print(cur.fetchone()) #한건

print("--- fetchmany(2) ---")
print(cur.fetchmany(2)) #2건

print("--- fetchall() ---")
print(cur.fetchall()) #나머지 전체

#정상적으로 완료
con.commit()

# 연결 종료
con.close()