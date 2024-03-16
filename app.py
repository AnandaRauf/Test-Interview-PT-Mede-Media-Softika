from flask import Flask, render_template, request, redirect, url_for,make_response
import pdfkit
import mysql.connector
# Path dan konfigurasi
path_wkhtmltopdf = r'C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
app = Flask(__name__)



def get_data_from_daftarkomoditas():
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
    mycursor.execute("SELECT * FROM daftar_produksi")
    data= mycursor.fetchall()
    mycursor.close()
    mydatabase.close()
    return data
def get_data_produksi():
    mydatabase = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='testinterview_dbkomoditas'
    )
    mycursor = mydatabase.cursor()
    mycursor.execute("SELECT komoditas_kode,tanggal,nama_komoditas,jumlah FROM daftar_produksi")
    data= mycursor.fetchall()
    mycursor.close()
    mydatabase.close()
    return data
@app.route('/')
def beranda():
    alert = request.args.get('alert')
    # Mengambil data dari database
    data = get_data_from_daftarkomoditas()
    if data is None:
        return "Gagal mengambil data dari kolum nama_komoditas tabel daftar_komoditas"
    
    return render_template('index.html',data=data,alert=alert, title='Website Test Interview PT Mede Media Softika | Daftar Komoditas')

@app.route('/form_komoditas')
def form_komoditas():
    
    return render_template("forms_komoditas.html", title='Website Interview PT Mede Media Softika | Form Komoditas')

@app.route('/tambah_datakomoditas', methods=['GET','POST'])
def tambah_datakomoditas():
    if request.method == 'POST':
        Kode_komoditas = request.form['kodekomoditas']
        Nama_komoditas = request.form['namakomoditas']
    
    
    
    try:
        mydatabase = mysql.connector.connect(host='localhost', user='root', passwd='', database='testinterview_dbkomoditas')
        mycursor = mydatabase.cursor()
        sql = "INSERT INTO daftar_komoditas (komoditas_kode, komoditas_nama) VALUES (%s, %s)"  # perbaikan disini
        val = (Kode_komoditas, Nama_komoditas)  # perbaikan disini
        mycursor.execute(sql, val)
        mydatabase.commit()
        mycursor.close()
        mydatabase.close()
        return redirect(url_for('beranda', alert='Data komoditas berhasil disimpan!'))
    except:
        return 'Terjadi Kesalahan saat menyimpan data'
    # Mengirimkan alert peringatan data berhasil disimpan
    return render_template('forms_komoditas.html')
   
@app.route('/tambah_dataproduksi', methods=['GET','POST'])
def tambah_dataproduksi():
    if request.method == 'POST':
        Kode_Komoditas = request.form['kodekomoditas']
        Tanggal_produksi = request.form['tanggalproduksi']
        Nama_komoditas = request.form['namakomoditas']
        Jumlah_produksi = request.form['jumlahproduksi']
    
    
    try:
        mydatabase = mysql.connector.connect(host='localhost', user='root', passwd='', database='testinterview_dbkomoditas')
        mycursor = mydatabase.cursor()
        sql = "INSERT INTO daftar_produksi (komoditas_kode,tanggal, nama_komoditas,jumlah) VALUES (%s, %s)"  # perbaikan disini
        val = (Kode_Komoditas,Tanggal_produksi, Nama_komoditas,Jumlah_produksi)  # perbaikan disini
        mycursor.execute(sql, val)
        mydatabase.commit()
        mycursor.close()
        mydatabase.close()
        return redirect(url_for('lihat_data_produksi', alert='Data produksi berhasil disimpan!'))
    except:
        return 'Terjadi Kesalahan saat menyimpan data'
    # Mengirimkan alert peringatan data berhasil disimpan
    return render_template('forms_produksi.html')

@app.route('/lihat_data_produksi')
def lihat_data_produksi():
    alert = request.args.get('alert')
    # Mengambil data dari database
    data = get_data_produksi()
    if data is None:
        return "Gagal mengambil data dari kolum nama_komoditas tabel daftar_produksi"
    
    return render_template('details_produksi.html',data=data,alert=alert, title='Website Test Interview PT Mede Media Softika | Daftar Produksi')
    
    

@app.route('/form_produksi')
def form_produksi():
    # Mengambil data dari database
    data = get_data_komoditas()
   
    if data is None:
        return "Gagal mengambil data dari tabel daftar_komoditas kolum komoditas_nama"
    return render_template('forms_produksi.html', data= data, title='Website Interview PT Mede Media Softika | Form Produksi')

@app.route('/lihat_data_transaksi')
def lihat_data_transaksi():
    #alert = request.args.get('alert')
    # Mengambil data dari database
    #data = get_data_produksi()
    #if data is None:
     #   return "Gagal mengambil data dari kolum nama_komoditas tabel daftar_produksi"
    
    return render_template('lihat_transaksi.html', title='Website Test Interview PT Mede Media Softika | Data Transaksi')

@app.route('/cetak_data_transaksi', methods=['GET', 'POST'])
def cetak_data_transaksi():
    try:
        # Mengambil data dari database
        data = get_data_produksi()

        # Memeriksa apakah data berhasil diambil
        if data is None:
            return "Gagal mengambil data dari tabel daftar_produksi"

        # Render template dengan data
        html = render_template('lihat_transaksi.html', data=data)

        # Konversi HTML ke PDF dengan konfigurasi yang sudah ditentukan
        pdf = pdfkit.from_string(html, False, configuration=config)

        # Mengatur response untuk file PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=hasiltransaksi.pdf'

        return response
    except Exception as e:
        return f'Terjadi Kesalahan: {str(e)}'

    return render_template('lihat_transaksi.html', title='Website Test Interview PT Mede Media Softika | Data Transaksi')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run(debug=True)
