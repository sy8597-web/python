"""ProductsDB: SQLite helper for Products table.

Usage:
  - Import and use ProductsDB in your code.
  - Run this script with --generate to create and populate 100000 sample rows:
      python c:\work\products_db.py --generate

By default (no args) the script runs a small smoke test (creates the table and inserts 5 rows).
"""
import sqlite3
import os
import random
import time
import argparse


class ProductsDB:
    """Simple wrapper around a SQLite database for product data.

    Table schema:
      Products(
        productID INTEGER PRIMARY KEY AUTOINCREMENT,
        productName TEXT,
        productPrice INTEGER
      )

    Methods are simple and safe for basic single-process usage.
    """

    def __init__(self, db_path=r"c:\work\MyProduct.db"):
        self.db_path = db_path
        # ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _connect(self):
        # Use a short timeout to avoid long lock waits in tests
        conn = sqlite3.connect(self.db_path, timeout=5)
        conn.row_factory = sqlite3.Row
        return conn

    def create_table(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS Products(
                    productID INTEGER PRIMARY KEY AUTOINCREMENT,
                    productName TEXT,
                    productPrice INTEGER
                );
                """
            )
            conn.commit()

    def insert_product(self, productName, productPrice):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO Products(productName, productPrice) VALUES(?,?);",
                        (productName, productPrice))
            conn.commit()
            return cur.lastrowid

    def bulk_insert(self, products, chunk_size=10000):
        """Insert many products.

        products: iterable of (productName, productPrice)
        Uses executemany in chunks inside a single transaction per chunk for speed.
        """
        start = time.time()
        inserted = 0
        # apply pragmas to speed up big inserts (best-effort)
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("PRAGMA synchronous = OFF;")
            cur.execute("PRAGMA journal_mode = MEMORY;")

            chunk = []
            for row in products:
                chunk.append(row)
                if len(chunk) >= chunk_size:
                    cur.executemany("INSERT INTO Products(productName, productPrice) VALUES(?,?);", chunk)
                    conn.commit()
                    inserted += len(chunk)
                    chunk = []
            if chunk:
                cur.executemany("INSERT INTO Products(productName, productPrice) VALUES(?,?);", chunk)
                conn.commit()
                inserted += len(chunk)
        finally:
            conn.close()

        duration = time.time() - start
        return inserted, duration

    def update_product(self, productID, productName=None, productPrice=None):
        if productName is None and productPrice is None:
            return 0
        parts = []
        params = []
        if productName is not None:
            parts.append("productName = ?")
            params.append(productName)
        if productPrice is not None:
            parts.append("productPrice = ?")
            params.append(productPrice)
        params.append(productID)
        sql = f"UPDATE Products SET {', '.join(parts)} WHERE productID = ?;"
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            return cur.rowcount

    def delete_product(self, productID):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Products WHERE productID = ?;", (productID,))
            conn.commit()
            return cur.rowcount

    def get_product_by_id(self, productID):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Products WHERE productID = ?;", (productID,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_all(self, limit=None, offset=0):
        with self._connect() as conn:
            cur = conn.cursor()
            sql = "SELECT * FROM Products"
            if limit is not None:
                sql += f" LIMIT {limit} OFFSET {offset}"
            sql += ";"
            cur.execute(sql)
            return [dict(r) for r in cur.fetchall()]

    def count(self):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as cnt FROM Products;")
            return cur.fetchone()[0]


def sample_product_generator(total):
    """Yield tuples of (productName, productPrice)."""
    # Generate simple product names; avoid external libraries for portability
    for i in range(1, total + 1):
        name = f"Product {i:06d}"
        price = random.randint(1000, 100000)
        yield (name, price)


def main():
    parser = argparse.ArgumentParser(description="ProductsDB helper script")
    parser.add_argument("--generate", action="store_true", help="Generate 100000 sample rows (this may take a while)")
    parser.add_argument("--count", type=int, default=100000, help="Number of rows to generate when --generate is used")
    args = parser.parse_args()

    db = ProductsDB()
    print(f"Using DB: {db.db_path}")
    db.create_table()

    if args.generate:
        n = args.count
        print(f"Generating {n} sample rows into Products (this may take a while)...")
        start = time.time()
        inserted, duration = db.bulk_insert(sample_product_generator(n))
        print(f"Inserted {inserted} rows in {duration:.2f}s (wall time {time.time()-start:.2f}s)")
        print(f"Total rows after insert: {db.count()}")
    else:
        # small smoke test
        print("Running smoke test: inserting 5 sample rows...")
        small = [(f"TestProduct{i}", 1000 + i * 10) for i in range(1, 6)]
        inserted, duration = db.bulk_insert(small, chunk_size=10)
        print(f"Inserted {inserted} rows (smoke).")
        print("Sample rows:")
        rows = db.get_all(limit=5)
        for r in rows:
            print(r)


if __name__ == "__main__":
    main()
