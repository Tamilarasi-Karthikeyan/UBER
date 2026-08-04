import os
import glob
import sqlite3
import kagglehub
import pandas as pd

def main():
    print("Downloading dataset 'rockyt07/uber-sql-database' via kagglehub...")
    path = kagglehub.dataset_download("rockyt07/uber-sql-database")
    print(f"Dataset downloaded to: {path}")

    # Search for sqlite/db files
    db_files = glob.glob(os.path.join(path, "**", "*.sqlite"), recursive=True) + \
               glob.glob(os.path.join(path, "**", "*.db"), recursive=True)

    if not db_files:
        # Fallback to check all files in path
        db_files = [os.path.join(path, f) for f in os.listdir(path) if not os.path.isdir(os.path.join(path, f))]

    print(f"Found database files: {db_files}")
    if not db_files:
        raise FileNotFoundError("No database file found in downloaded path!")

    db_path = db_files[0]
    print(f"Connecting to: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\nTables in database: {tables}")

    for (table_name,) in tables:
        print("="*60)
        print(f"TABLE: {table_name}")
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        cursor.execute(f"SELECT COUNT(*) FROM '{table_name}';")
        count = cursor.fetchone()[0]
        print(f"Total Rows: {count}")

        df_head = pd.read_sql_query(f"SELECT * FROM '{table_name}' LIMIT 5;", conn)
        print("\nSample Data:")
        print(df_head)
        print("="*60)

    conn.close()

if __name__ == "__main__":
    main()
