from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

# Jalankan inisiasi DB secara otomatis saat aplikasi dimulai
db.init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pustakawan', methods=['GET', 'POST'])
def pustakawan():
    conn = db.get_db_connection()
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        conn.execute('INSERT INTO buku (judul, penulis) VALUES (?, ?)', (judul, penulis))
        conn.commit()
        return redirect(url_for('pustakawan'))

    buku = conn.execute('''
                        SELECT b.id, b.judul, b.penulis, b.status, p.nama_peminjam
                        FROM buku b
                                 LEFT JOIN peminjaman p ON b.id = p.buku_id
                        ''').fetchall()
    conn.close()
    return render_template('pustakawan.html', buku=buku)


@app.route('/peminjam', methods=['GET', 'POST'])
def peminjam():
    conn = db.get_db_connection()
    if request.method == 'POST':
        buku_id = request.form['buku_id']
        nama_peminjam = request.form['nama_peminjam']

        conn.execute("UPDATE buku SET status = 'Dipinjam' WHERE id = ?", (buku_id,))
        conn.execute('INSERT INTO peminjaman (buku_id, nama_peminjam) VALUES (?, ?)', (buku_id, nama_peminjam))
        conn.commit()
        return redirect(url_for('peminjam'))

    buku_tersedia = conn.execute("SELECT * FROM buku WHERE status = 'Tersedia'").fetchall()
    conn.close()
    return render_template('peminjam.html', buku=buku_tersedia)


@app.route('/kembalikan/<int:buku_id>')
def kembalikan(buku_id):
    conn = db.get_db_connection()
    conn.execute("UPDATE buku SET status = 'Tersedia' WHERE id = ?", (buku_id,))
    conn.execute("DELETE FROM peminjaman WHERE buku_id = ?", (buku_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('pustakawan'))


if __name__ == '__main__':
    app.run(debug=True)