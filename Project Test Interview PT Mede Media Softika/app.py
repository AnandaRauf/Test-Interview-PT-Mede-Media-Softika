from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
app = Flask(__name__)

def get_data_from_database():
    try:
        # Koneksi ke database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="testinterview_dbkomoditas"
        )
        cursor = mydb.cursor()

        # Query untuk mengambil data dari tabel
        query = "SELECT * FROM daftar_komoditas"
        cursor.execute(query)

        # Mengambil hasil query
        result = cursor.fetchall()

        # Menutup koneksi
        cursor.close()
        mydb.close()

        return result
    except Exception as e:
        print("Error:", e)
        return None
# Fungsi untuk mendapatkan data komoditas dari database
def get_data_komoditas():
    mydatabase = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='testinterview_dbkomoditas'
    )
    mycursor = mydatabase.cursor()
    mycursor.execute("SELECT komoditas_nama FROM daftar_komoditas")
    data = mycursor.fetchall()
    mycursor.close()
    mydatabase.close()
    return data
@app.route('/')
def beranda():
    alert = request.args.get('alert')
    # Mengambil data dari database
    data = get_data_from_database()
    if data is None:
        return "Gagal mengambil data dari kolum nama_komoditas tabel daftar_komoditas"
    
    return render_template('index.html',data=data,alert=alert, title='Website Test Interview PT Mede Media Softika | Daftar Komoditas')

@app.route('/form_komoditas')
def form_komoditas():
    
    return render_template("forms_komoditas.html", title='Website Interview PT Mede Media Softika | Form Komoditas')

@app.route('/tambah_data', methods=['POST'])
def tambah_data():
    kode_komoditas = request.form['kode_komoditas']
    nama_komoditas = request.form['komoditas_nama']
    
    mydatabase = mysql.connector.connect(host='localhost', user='root', passwd='', database='testinterview_dbkomoditas')
    mycursor = mydatabase.cursor()
    
    sql = "INSERT INTO daftar_komoditas (kode_komoditas, komoditas_nama) VALUES (%s, %s)"  # perbaikan disini
    val = (kode_komoditas, nama_komoditas)  # perbaikan disini
    mycursor.execute(sql, val)
    
    mydatabase.commit()
    
    mycursor.close()
    mydatabase.close()
    
    # Mengirimkan alert peringatan data berhasil disimpan
    return redirect(url_for('beranda', alert='Data komoditas berhasil disimpan!'))


@app.route('/form_produksi')
def form_produksi():
    # Mengambil data dari database
    data = get_data_komoditas()
    if data is None:
        return "Gagal mengambil data dari tabel daftar_komoditas kolum komoditas_nama"
    return render_template('forms_produksi.html', data= data, title='Website Interview PT Mede Media Softika | Form Produksi')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
