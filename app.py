from flask import Flask, request, render_template

app = Flask(__name__)

# ==============================================================================
# DATA CP (CAPAIAN PEMBELAJARAN) - (Struktur data tetap sama)
# ==============================================================================
data_cp = {
    # Data untuk Fase Fondasi memiliki struktur 'sub_elemen'
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
            "Dasar-Dasar Literasi, dsb.": [
                "Murid mengenali dan memahami berbagai informasi, mengomunikasikan perasaan dan pikiran secara lisan, tulisan, atau menggunakan berbagai media serta membangun percakapan.",
                "Murid menunjukkan minat dan berpartisipasi dalam kegiatan pramembaca.",
                "Murid mampu mengamati, menyebutkan alasan, pilihan atau keputusannya, mampu memecahkan masalah sederhana, serta mengetahui hubungan sebab akibat.",
            ]
        }
    },
    # Data untuk Fase A - F memiliki struktur 'cp_list'
    "A": {"elemen": "Fase A (Pendidikan Pancasila - Kls 1-2 SD)","cp_list": ["Mengenal bendera negara, lagu kebangsaan, simbol dan sila-sila Pancasila.","Menerapkan nilai-nilai Pancasila di lingkungan keluarga.","Mengenal aturan di lingkungan keluarga.","Mengenal semboyan Bhinneka Tunggal Ika.","Mengidentifikasi dan menghargai identitas dirinya (jenis kelamin, hobi, dll).","Mengenal karakteristik lingkungan tempat tinggal dan sekolah.","Mempraktikkan bekerja sama menjaga lingkungan sekitar dalam keberagaman."]},
    "B": {"elemen": "Fase B (Pendidikan Pancasila - Kls 3-4 SD)","cp_list": ["Mengidentifikasi makna sila-sila Pancasila, dan penerapannya dalam kehidupan sehari-hari.","Menunjukkan sikap bangga menjadi anak Indonesia.","Mengidentifikasi dan melaksanakan aturan di sekolah dan lingkungan tempat tinggal.","Mengidentifikasi dan menerapkan hak dan kewajiban sebagai anggota keluarga dan warga sekolah.","Membedakan dan menghargai identitas keluarga, dan teman-temannya.","Menunjukkan perilaku bekerja sama dalam berbagai bentuk keberagaman suku bangsa, sosial, dan budaya."]},
    "C": {"elemen": "Fase C (Pendidikan Pancasila - Kls 5-6 SD)","cp_list": ["Memahami kronologi sejarah kelahiran Pancasila.","Menghubungkan sila-sila dalam Pancasila sebagai suatu kesatuan yang utuh.","Mengimplementasikan bentuk-bentuk norma, hak, dan kewajiban sebagai warga negara.","Mempraktikkan musyawarah untuk membuat kesepakatan dan aturan bersama.","Menyajikan hasil identifikasi sikap menghormati, menjaga, dan melestarikan keberagaman budaya.","Menunjukkan perilaku gotong royong untuk menjaga persatuan sebagai wujud bela negara."]},
    "D": {"elemen": "Fase D (Pendidikan Pancasila - Kls 7-9 SMP)","cp_list": ["Memahami kedudukan Pancasila sebagai dasar negara, pandangan hidup, dan ideologi negara.","Menerapkan norma dan aturan dalam masyarakat.","Menggunakan hak dan menerapkan kewajiban sebagai warga negara.","Mempraktikkan kemerdekaan berpendapat sebagai warga negara dalam era keterbukaan informasi.","Menerima keberagaman suku bangsa, agama, ras, dan antargolongan dalam bingkai Bhinneka Tunggal Ika.","Menumbuhkan sikap tanggung jawab dan berperan aktif melestarikan praktik tradisi dan kearifan lokal.","Memahami Proklamasi Kemerdekaan dan berpartisipasi aktif menjaga keutuhan wilayah NKRI."]},
    "E": {"elemen": "Fase E (Pendidikan Pancasila - Kls 10 SMA/SMK)","cp_list": ["Menganalisis cara pandang para perumus Pancasila tentang dasar negara.","Menganalisis kedudukan Pancasila sebagai dasar negara, pandangan hidup, dan ideologi negara.","Menerapkan perilaku taat hukum berdasarkan peraturan yang berlaku.","Menganalisis makna kedudukan Pancasila sebagai sumber dari segala sumber hukum negara.","Memahami prinsip gotong royong sebagai perwujudan sistem ekonomi Pancasila.","Memahami peran dan kedudukannya sebagai warga Negara Indonesia.","Menganalisis peran Indonesia dalam hubungan antarnegara."]},
    "F": {"elemen": "Fase F (Pendidikan Pancasila - Kls 11-12 SMA/SMK)","cp_list": ["Menganalisis peluang dan tantangan penerapan nilai-nilai Pancasila dalam kehidupan global.","Membiasakan perilaku yang sesuai dengan nilai-nilai Pancasila sebagai identitas nasional.","Menunjukkan sikap demokratis dalam era keterbukaan informasi.","Menganalisis kasus pelanggaran hak dan pengingkaran kewajiban warga negara.","Menganalisis potensi konflik dan memberi solusi yang berkeadilan terhadap permasalahan keberagaman.","Merancang kegiatan bersama dengan prinsip gotong royong dalam praktik hidup sehari-hari.","Menganalisis ancaman, tantangan, hambatan, dan gangguan (ATHG) yang dihadapi Indonesia."]}
}


# ==============================================================================
# FUNGSI-FUNGSI PINTAR UNTUK GENERATOR DOKUMEN (TETAP SAMA)
# ==============================================================================
def petakan_ke_bidang_bk(kalimat):
    kalimat = kalimat.lower()
    if any(kata in kalimat for kata in ["karir", "profesi", "usaha", "pekerjaan", "wirausaha", "ekonomi"]): return "Karir"
    if any(kata in kalimat for kata in ["belajar", "kritis", "informasi", "keterampilan", "musyawarah", "pendapat"]): return "Belajar"
    if any(kata in kalimat for kata in ["sosial", "interaksi", "teman", "masyarakat", "gotong royong", "keberagaman", "bersama"]): return "Sosial"
    if any(kata in kalimat for kata in ["pribadi", "akhlak", "emosi", "identitas diri", "sikap", "norma", "aturan", "hak", "kewajiban", "nilai-nilai"]): return "Pribadi"
    return "Pribadi"

def buat_saran_kegiatan(kalimat):
    kalimat = kalimat.lower()
    if any(kata in kalimat for kata in ["menganalisis", "membandingkan", "mengevaluasi"]): return "Diskusi Kelompok, Debat Terstruktur, Analisis Studi Kasus, Membuat Peta Pikiran (Mind Mapping)."
    if any(kata in kalimat for kata in ["menerapkan", "mempraktikkan", "melaksanakan", "merancang", "menunjukkan"]): return "Bermain Peran (Role Playing), Simulasi, Proyek Kelompok, Membuat Poster/Infografis."
    if any(kata in kalimat for kata in ["memahami", "mengidentifikasi", "mengenal", "menjelaskan"]): return "Ceramah Interaktif, Menonton Video Reflektif, Curah Pendapat (Brainstorming), Games Edukatif."
    return "Diskusi dan tanya jawab, Refleksi diri."

def proses_satu_cp(cp):
    """Fungsi kecil untuk memproses satu buah kalimat CP."""
    tl = cp.replace("Mengenal", "Siswa dapat mengenal").replace("Menerapkan", "Siswa dapat menerapkan").replace("Mengidentifikasi", "Siswa dapat mengidentifikasi").replace("Membedakan", "Siswa dapat membedakan").replace("Memahami", "Siswa dapat memahami").replace("Menghubungkan", "Siswa dapat menghubungkan").replace("Mengimplementasikan", "Siswa dapat mengimplementasikan").replace("Mempraktikkan", "Siswa dapat mempraktikkan").replace("Menyajikan", "Siswa dapat menyajikan").replace("Menunjukkan", "Siswa dapat menunjukkan").replace("Menggunakan", "Siswa dapat menggunakan").replace("Menerima", "Siswa dapat menerima").replace("Menumbuhkan", "Siswa dapat menumbuhkan").replace("Menganalisis", "Siswa dapat menganalisis").replace("Membiasakan", "Siswa dapat membiasakan").replace("Merancang", "Siswa dapat merancang").replace("Murid", "Siswa dapat", 1)
    
    kktl = "Siswa menunjukkan perubahan perilaku/pemahaman yang relevan melalui observasi atau unjuk kerja."
    if "mengenal" in tl or "memahami" in tl or "mengidentifikasi" in tl: kktl = "Siswa mampu menyebutkan, menjelaskan, atau memberi contoh terkait tujuan layanan."
    elif "menerapkan" in tl or "mempraktikkan" in tl or "menunjukkan" in tl: kktl = "Siswa mampu mendemonstrasikan perilaku atau keterampilan yang diharapkan dalam simulasi atau kegiatan nyata."
    elif "menganalisis" in tl: kktl = "Siswa mampu menguraikan, membandingkan, atau menyimpulkan suatu kasus/informasi terkait tujuan layanan."
    
    return {'cp': cp, 'tl': tl, 'bidang': petakan_ke_bidang_bk(tl), 'kktl': kktl, 'kegiatan': buat_saran_kegiatan(tl)}

def generate_prosem(analisis_data, semester):
    prosem = {'Pribadi': [], 'Sosial': [], 'Belajar': [], 'Karir': []}
    for item in analisis_data: prosem[item['bidang']].append(item['tl'])
    if semester.lower() == 'ganjil': bulan = ["Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    else: bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni"]
    return prosem, bulan

# ==============================================================================
# LOGIKA WEBSITE (FLASK) - DENGAN PERBAIKAN
# ==============================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-dokumen', methods=['POST'])
def generate_dokumen_route():
    data_guru = {'nama_sekolah': request.form['nama_sekolah'],'nama_guru': request.form['nama_guru'],'nip': request.form['nip'],'semester': request.form['semester'],'tahun_ajaran': request.form['tahun_ajaran']}
    fase_dipilih = request.form['fase']
    cp_data = data_cp.get(fase_dipilih)

    if not cp_data: return "Fase tidak valid."

    hasil_analisis = []
    
    # INI BAGIAN PERBAIKANNYA: Cek format data dan proses sesuai formatnya
    if 'cp_list' in cp_data:
        # Format untuk Fase A - F
        temp_data = []
        for cp in cp_data['cp_list']:
            temp_data.append(proses_satu_cp(cp))
        hasil_analisis.append({'nama_elemen': 'Pendidikan Pancasila (Adaptasi untuk Layanan BK)', 'data': temp_data})

    elif 'sub_elemen' in cp_data:
        # Format untuk Fase Fondasi
        for nama_elemen, daftar_cp in cp_data['sub_elemen'].items():
            temp_data = []
            for cp in daftar_cp:
                temp_data.append(proses_satu_cp(cp))
            hasil_analisis.append({'nama_elemen': nama_elemen, 'data': temp_data})

    # Menggabungkan semua TL dari hasil analisis untuk Prosem
    semua_tl_teranalisis = []
    for elemen in hasil_analisis:
        semua_tl_teranalisis.extend(elemen['data'])
        
    prosem_data, bulan_prosem = generate_prosem(semua_tl_teranalisis, data_guru['semester'])

    return render_template('hasil.html', 
                           data_guru=data_guru, 
                           fase=cp_data,
                           hasil_analisis=hasil_analisis,
                           prosem_data=prosem_data,
                           bulan_prosem=bulan_prosem)

if __name__ == '__main__':
    app.run(debug=True)
