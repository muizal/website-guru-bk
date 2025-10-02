from flask import Flask, request, render_template

app = Flask(__name__)

# ==============================================================================
# DATA CAPAIAN PEMBELAJARAN (CP) YANG SUDAH DIEKSTRAK DARI PDF
# ==============================================================================
data_cp = {
    "FONDASI": {
        "elemen": "Fase Fondasi (Holistik)",
        "sub_elemen": {
            "Nilai Agama dan Budi Pekerti": [
                "Murid percaya kepada Tuhan Yang Maha Esa sebagai pencipta dirinya, makhluk lain dan alam, serta mulai mengenal dan mempraktikkan ajaran pokok sesuai dengan agama dan kepercayaannya.",
                "Murid menghargai diri sendiri dan memiliki rasa syukur terhadap Tuhan YME sehingga dapat berpartisipasi aktif dalam menjaga kebersihan, kesehatan, dan keselamatan dirinya.",
                "Murid menghargai sesama manusia dengan berbagai perbedaannya sehingga mempraktikkan perilaku baik dan berakhlak mulia.",
                "Murid menghargai alam dan seluruh makhluk hidup ciptaan Tuhan Yang Maha Esa."
            ],
            "Jati Diri": [
                "Murid mengenali identitas dirinya yang terbentuk oleh karakteristik fisik dan gender, minat, kebutuhan, agama, dan sosial budaya.",
                "Murid mengenali kebiasaan-kebiasaan di lingkungan keluarga, satuan pendidikan, dan masyarakat.",
                "Murid mengenali, mengekspresikan, dan mengelola emosi diri, serta membangun hubungan sosial secara sehat.",
                "Murid mengenali perannya sebagai bagian dari keluarga, satuan pendidikan, masyarakat dan warga negara Indonesia sehingga dapat menyesuaikan diri dengan lingkungan, aturan dan norma yang berlaku.",
                "Murid memiliki fungsi gerak (motorik kasar, halus, dan taktil) untuk merawat dirinya, membangun kemandirian dan berkegiatan."
            ],
            "Dasar-Dasar Literasi, Matematika, Sains, Teknologi, Rekayasa, dan Seni": [
                "Murid mengenali dan memahami berbagai informasi, mengomunikasikan perasaan dan pikiran secara lisan, tulisan, atau menggunakan berbagai media serta membangun percakapan.",
                "Murid menunjukkan minat dan berpartisipasi dalam kegiatan pramembaca.",
                "Murid mampu mengamati, menyebutkan alasan, pilihan atau keputusannya, mampu memecahkan masalah sederhana, serta mengetahui hubungan sebab akibat.",
                "Murid menunjukkan kemampuan awal menggunakan dan merekayasa teknologi serta untuk mencari informasi, gagasan, dan keterampilan secara aman dan bertanggung jawab.",
                "Murid mengeksplorasi berbagai proses seni, mengekspresikannya, serta mengapresiasi karya seni."
            ]
        }
    },
    "A": {"elemen": "Fase A (Umumnya Kelas I dan II SD/MI)", "sub_elemen": {"Deskripsi": ["Capaian pembelajaran pada fase A disusun selaras dengan fase fondasi untuk memastikan transisi pembelajaran yang berkesinambungan dari PAUD ke SD."]}},
    "B": {"elemen": "Fase B (Umumnya Kelas III dan IV SD/MI)", "sub_elemen": {"Deskripsi": ["Capaian pembelajaran pada fase B mencakup pengembangan kemampuan dasar literasi, numerasi, dan pemahaman dunia sekitar yang lebih luas."]}},
    "C": {"elemen": "Fase C (Umumnya Kelas V dan VI SD/MI)", "sub_elemen": {"Deskripsi": ["Capaian pembelajaran pada fase C berfokus pada analisis informasi, kemampuan berpikir kritis awal, dan penerapan konsep dalam konteks yang lebih beragam."]}},
    "D": {"elemen": "Fase D (Umumnya Kelas VII, VIII, dan IX SMP/MTs)", "sub_elemen": {"Deskripsi": ["Capaian pembelajaran pada fase D menekankan pada kemampuan menganalisis, mengevaluasi, serta menghubungkan konsep antar mata pelajaran dalam memecahkan masalah."]}},
    "E": {"elemen": "Fase E (Umumnya Kelas X SMA/MA/SMK/MAK)", "sub_elemen": {"Deskripsi": ["Capaian pembelajaran pada fase E bertujuan untuk pendalaman konsep keilmuan sebagai persiapan menuju spesialisasi di fase berikutnya."]}},
    "F": {"elemen": "Fase F (Umumnya Kelas XI dan XII SMA/MA/SMK/MAK)", "sub_elemen": {"Deskripsi": ["Capaian pembelajaran pada fase F berfokus pada penguasaan kompetensi sesuai pilihan peminatan, berpikir kritis tingkat tinggi, dan persiapan studi lanjut atau dunia kerja."]}}
}

# ==============================================================================
# FUNGSI UNTUK ANALISIS CP menjadi TL dan KKTL
# ==============================================================================
def generate_analisis_cl(data_cp_terpilih):
    hasil_analisis = []
    if not data_cp_terpilih or "sub_elemen" not in data_cp_terpilih:
        return hasil_analisis

    for sub_elemen, daftar_cp in data_cp_terpilih['sub_elemen'].items():
        # Lewati sub_elemen 'Deskripsi' karena tidak perlu dianalisis
        if sub_elemen == "Deskripsi":
            continue

        analisis_per_elemen = {'nama_elemen': sub_elemen, 'data': []}
        for cp in daftar_cp:
            # 1. Membuat Tujuan Layanan (TL)
            tl = cp.replace("Murid", "Siswa dapat", 1)

            # 2. Membuat Saran Kriteria Ketercapaian (KKTL) berdasarkan kata kerja
            kktl = "Siswa mampu menunjukkan perubahan perilaku positif yang relevan setelah sesi layanan." # Default
            if "mengenali" in cp or "memahami" in cp:
                kktl = "Siswa mampu menjelaskan kembali atau memberikan contoh konkret terkait topik layanan."
            elif "menghargai" in cp or "menunjukkan" in cp:
                kktl = "Siswa menunjukkan sikap positif atau perilaku yang sesuai melalui observasi dalam kegiatan sehari-hari."
            elif "mempraktikkan" in cp or "menggunakan" in cp or "mengekspresikan" in cp:
                kktl = "Siswa dapat mendemonstrasikan keterampilan yang dimaksud dalam sesi layanan atau simulasi."
            elif "mengelola" in cp or "membangun" in cp:
                kktl = "Siswa menunjukkan kemajuan dalam mengelola emosi atau membangun hubungan sosial dalam studi kasus atau refleksi diri."
            
            analisis_per_elemen['data'].append({
                'cp': cp,
                'tl': tl,
                'kktl': kktl
            })
        hasil_analisis.append(analisis_per_elemen)
        
    return hasil_analisis

# ==============================================================================
# LOGIKA WEBSITE (FLASK)
# ==============================================================================

# Rute untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Rute untuk memproses dan menampilkan hasil
@app.route('/generate-dokumen', methods=['POST'])
def generate_dokumen_route():
    data_guru = {
        'nama_sekolah': request.form['nama_sekolah'],
        'nama_guru': request.form['nama_guru'],
        'nip': request.form['nip'],
        'semester': request.form['semester'],
        'tahun_ajaran': request.form['tahun_ajaran']
    }
    fase_dipilih = request.form['fase']
    cp_terpilih = data_cp.get(fase_dipilih)

    # Panggil fungsi analisis
    hasil_analisis_cl = generate_analisis_cl(cp_terpilih)
    
    # Kirim data ke halaman 'hasil.html' untuk ditampilkan
    return render_template('hasil.html', 
                           data_guru=data_guru, 
                           fase=cp_terpilih,
                           hasil_analisis=hasil_analisis_cl)

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
