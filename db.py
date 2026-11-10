import sqlite3

def get_db_connection():
    conn = sqlite3.connect('perpustakaan.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Tabel untuk menyimpan daftar buku
    conn.execute('''
        CREATE TABLE IF NOT EXISTS buku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            penulis TEXT NOT NULL,
            status TEXT DEFAULT 'Tersedia'
        )
    ''')
    # Tabel untuk mencatat siapa yang meminjam buku
    conn.execute('''
        CREATE TABLE IF NOT EXISTS peminjaman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buku_id INTEGER,
            nama_peminjam TEXT NOT NULL,
            FOREIGN KEY (buku_id) REFERENCES buku (id)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database berhasil diinisialisasi.")