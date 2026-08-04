import os
import glob
import shutil
import sqlite3
import kagglehub

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    target_db_path = os.path.join(project_dir, "uber_data.sqlite")

    print("Downloading dataset 'rockyt07/uber-sql-database' via kagglehub...")
    cache_path = kagglehub.dataset_download("rockyt07/uber-sql-database")
    print(f"Dataset downloaded to cache: {cache_path}")

    # Find sqlite or db files in cache_path
    db_files = glob.glob(os.path.join(cache_path, "**", "*.sqlite"), recursive=True) + \
               glob.glob(os.path.join(cache_path, "**", "*.db"), recursive=True)

    if not db_files:
        # Check all files in directory
        all_files = [os.path.join(cache_path, f) for f in os.listdir(cache_path) if not os.path.isdir(os.path.join(cache_path, f))]
        print("All files in cache path:", all_files)
        db_files = [f for f in all_files if f.endswith(('.sqlite', '.db', '.sql')) or 'uber' in f.lower()]

    if not db_files:
        raise FileNotFoundError(f"No SQLite database file found in {cache_path}")

    source_db = db_files[0]
    print(f"Found source database: {source_db}")
    print(f"Copying database to project folder: {target_db_path}")
    shutil.copy2(source_db, target_db_path)
    print("Database copy complete!")

    # Inspect the SQLite database
    print("\nInspecting SQLite Database structure...")
    conn = sqlite3.connect(target_db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables found ({len(tables)}):", [t[0] for t in tables])

    for (table_name,) in tables:
        print("\n" + "="*50)
        print(f"TABLE NAME: {table_name}")
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        cols = cursor.fetchall()
        print("Columns:")
        for c in cols:
            print(f"  - {c[1]} (Type: {c[2]})")
        
        cursor.execute(f"SELECT COUNT(*) FROM '{table_name}';")
        count = cursor.fetchone()[0]
        print(f"Total Rows: {count:,}")

        cursor.execute(f"SELECT * FROM '{table_name}' LIMIT 3;")
        rows = cursor.fetchall()
        col_names = [c[1] for c in cols]
        print("Sample Rows:")
        for r in rows:
            print("  ", dict(zip(col_names, r)))
        print("="*50)

    conn.close()
    print("\nDatabase setup and inspection successfully completed!")

if __name__ == "__main__":
    main()
