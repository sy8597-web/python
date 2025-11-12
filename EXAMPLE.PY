import sqlite3
import os
import random

class ProductDB:
    """
    SQLite 데이터베이스를 사용하여 전자제품 데이터를 관리하는 클래스.
    """
    def __init__(self, db_name="MyProduct.db"):
        """
        데이터베이스에 연결하고 테이블을 생성합니다.
        :param db_name: 사용할 데이터베이스 파일의 이름
        """
        self.db_name = db_name
        # 데이터베이스에 연결
        self.conn = sqlite3.connect(self.db_name)
        # 커서 생성
        self.cursor = self.conn.cursor()
        # 테이블 생성 메서드 호출
        self.create_table()

    def create_table(self):
        """
        Products 테이블을 생성합니다. 테이블이 이미 존재하면 생성하지 않습니다.
        productID는 자동으로 증가하는 기본 키입니다.
        """
        query = """
        CREATE TABLE IF NOT EXISTS Products (
            productID INTEGER PRIMARY KEY AUTOINCREMENT,
            productName TEXT NOT NULL,
            productPrice INTEGER NOT NULL
        );
        """
        self.cursor.execute(query)
        self.conn.commit()
        print("Products 테이블이 성공적으로 준비되었습니다.")

    def insert_product(self, product_name, product_price):
        """
        하나의 제품 데이터를 테이블에 추가합니다.
        :param product_name: 추가할 제품의 이름
        :param product_price: 추가할 제품의 가격
        """
        query = "INSERT INTO Products (productName, productPrice) VALUES (?, ?);"
        self.cursor.execute(query, (product_name, product_price))
        self.conn.commit()
        print(f"제품 '{product_name}'이(가) 추가되었습니다.")

    def insert_bulk_products(self, products_list):
        """
        여러 개의 제품 데이터를 한 번에 테이블에 추가합니다.
        :param products_list: (이름, 가격) 튜플의 리스트
        """
        query = "INSERT INTO Products (productName, productPrice) VALUES (?, ?);"
        self.cursor.executemany(query, products_list)
        self.conn.commit()
        print(f"{len(products_list)}개의 제품이 대량으로 추가되었습니다.")

    def select_all_products(self, limit=10):
        """
        테이블의 모든 제품 데이터를 조회합니다.
        :param limit: 조회할 데이터의 수
        :return: 제품 데이터의 리스트
        """
        query = f"SELECT * FROM Products LIMIT {limit};"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_product_by_id(self, product_id):
        """
        특정 ID를 가진 제품을 조회합니다.
        :param product_id: 조회할 제품의 ID
        :return: 조회된 제품 데이터 (튜플) 또는 None
        """
        query = "SELECT * FROM Products WHERE productID = ?;"
        self.cursor.execute(query, (product_id,))
        return self.cursor.fetchone()

    def update_product_price(self, product_id, new_price):
        """
        특정 ID를 가진 제품의 가격을 수정합니다.
        :param product_id: 수정할 제품의 ID
        :param new_price: 새로운 가격
        """
        query = "UPDATE Products SET productPrice = ? WHERE productID = ?;"
        self.cursor.execute(query, (new_price, product_id))
        self.conn.commit()
        print(f"제품 ID {product_id}의 가격이 {new_price}(으)로 변경되었습니다.")

    def delete_product(self, product_id):
        """
        특정 ID를 가진 제품을 삭제합니다.
        :param product_id: 삭제할 제품의 ID
        """
        query = "DELETE FROM Products WHERE productID = ?;"
        self.cursor.execute(query, (product_id,))
        self.conn.commit()
        print(f"제품 ID {product_id}이(가) 삭제되었습니다.")

    def close_connection(self):
        """
        데이터베이스 연결을 닫습니다.
        """
        if self.conn:
            self.conn.close()
            print("데이터베이스 연결이 종료되었습니다.")

# --- 메인 실행 로직 ---
if __name__ == "__main__":
    db_file = "MyProduct.db"
    
    # 스크립트 재실행 시 기존 DB 파일이 있다면 삭제하여 초기 상태에서 시작
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"기존 데이터베이스 '{db_file}'를 삭제했습니다.")

    # 1. ProductDB 클래스 인스턴스 생성 (DB 연결 및 테이블 생성)
    db = ProductDB(db_name=db_file)

    # 2. 10만 개의 샘플 데이터 생성
    print("\n--- 10만개 샘플 데이터 생성 및 대량 입력 시작 ---")
    sample_data = []
    for i in range(1, 100001):
        product_name = f"전자제품_{i:06d}"
        product_price = random.randint(10000, 1000000) # 1만원 ~ 100만원 사이의 랜덤 가격
        sample_data.append((product_name, product_price))
    
    # 3. 샘플 데이터 대량 INSERT
    db.insert_bulk_products(sample_data)

    # 4. 데이터 조회 (SELECT) 예제
    print("\n--- 전체 데이터 조회 (상위 5개) ---")
    all_products = db.select_all_products(limit=5)
    for product in all_products:
        print(product)

    print("\n--- 특정 데이터 조회 (ID: 10) ---")
    product_10 = db.select_product_by_id(10)
    print(product_10)

    # 5. 데이터 수정 (UPDATE) 예제
    print("\n--- 데이터 수정 (ID: 10의 가격을 999999로 변경) ---")
    db.update_product_price(product_id=10, new_price=999999)
    print("수정 후 데이터 확인:")
    updated_product_10 = db.select_product_by_id(10)
    print(updated_product_10)

    # 6. 데이터 삭제 (DELETE) 예제
    print("\n--- 데이터 삭제 (ID: 25) ---")
    print("삭제 전 데이터 확인:")
    product_25_before = db.select_product_by_id(25)
    print(product_25_before)
    
    db.delete_product(product_id=25)
    
    print("삭제 후 데이터 확인:")
    product_25_after = db.select_product_by_id(25)
    print(product_25_after)

    # 7. 데이터베이스 연결 종료
    print("\n--- 작업 완료 ---")
    db.close_connection()