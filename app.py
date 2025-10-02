from flask import Flask, request, render_template
import datetime

app = Flask(__name__)

# ==============================================================================
# DATA CP (CAPAIAN PEMBELAJARAN) - DARI EKSTRAKSI PDF BSKAP
# ==============================================================================
data_cp = {
    "A": {"elemen": "Fase A (Pendidikan Pancasila - Kelas 1-2 SD)","cp_list": ["Mengenal bendera negara, lagu kebangsaan, simbol dan sila-sila Pancasila.","Menerapkan nilai-nilai Pancasila di lingkungan keluarga.","Mengenal aturan di lingkungan keluarga.","Mengenal semboyan Bhinneka Tunggal Ika.","Mengidentifikasi dan menghargai identitas dirinya (jenis kelamin, hobi, dll).","Mengenal karakteristik lingkungan tempat tinggal dan sekolah.","Mempraktikkan bekerja sama menjaga lingkungan sekitar dalam keberagaman."]},
    "B": {"elemen": "Fase B (Pendidikan Pancasila - Kelas 3-4 SD)","cp_list": ["Mengidentifikasi makna sila-sila Pancasila, dan penerapannya dalam kehidupan sehari-hari.","Menunjukkan sikap bangga menjadi anak Indonesia.","Mengidentifikasi dan melaksanakan aturan di sekolah dan lingkungan tempat tinggal.","Mengidentifikasi dan menerapkan hak dan kewajiban sebagai anggota keluarga dan warga sekolah.","Membedakan dan menghargai identitas keluarga, dan teman-temannya.","Menunjukkan perilaku bekerja sama dalam berbagai bentuk keberagaman suku bangsa, sosial, dan budaya."]},
    "C": {"elemen": "Fase C (Pendidikan Pancasila - Kelas 5-6 SD)","cp_list": ["Memahami kronologi sejarah kelahiran Pancasila.","Menghubungkan sila-sila dalam Pancasila sebagai suatu kesatuan yang utuh.","Mengimplementasikan bentuk-bentuk norma, hak, dan kewajiban sebagai warga negara.","Mempraktikkan musyawarah untuk membuat kesepakatan dan aturan bersama.","Menyajikan hasil identifikasi sikap menghormati, menjaga, dan melestarikan keberagaman budaya.","Menunjukkan perilaku gotong royong untuk menjaga persatuan sebagai wujud bela negara."]},
    "D": {"elemen": "Fase D (Pendidikan Pancasila - Kelas 7-9 SMP)","cp_list": ["Memahami kedudukan Pancasila sebagai dasar negara, pandangan hidup, dan ideologi negara.","Menerapkan norma dan aturan dalam masyarakat.","Menggunakan hak dan menerapkan kewajiban sebagai warga negara.","Mempraktikkan kemerdekaan berpendapat sebagai warga negara dalam era keterbukaan informasi.","Menerima keberagaman suku bangsa, agama, ras, dan antargolongan dalam bingkai Bhinneka Tunggal Ika.","Menumbuhkan sikap tanggung jawab dan berperan aktif melestarikan praktik tradisi dan kearifan lokal.","Memahami Proklamasi Kemerdekaan dan berpartisipasi aktif menjaga keutuhan wilayah NKRI."]},
    "E": {"elemen": "Fase E (Pendidikan Pancasila - Kelas 10 SMA/SMK)","cp_list": ["Menganalisis cara pandang para perumus Pancasila tentang dasar negara.","Menganalisis kedudukan Pancasila sebagai dasar negara, pandangan hidup, dan ideologi negara.","Menerapkan perilaku taat hukum berdasarkan peraturan yang berlaku.","Menganalisis makna kedudukan Pancasila sebagai sumber dari segala sumber hukum negara.","Memahami prinsip gotong royong sebagai perwujudan sistem ekonomi Pancasila.","Memahami peran dan kedudukannya sebagai warga Negara Indonesia.","Menganalisis peran Indonesia dalam hubungan antarnegara."]},
    "F": {"elemen": "Fase F (Pendidikan Pancasila - Kelas 11-12 SMA/SMK)","cp_list": ["Menganalisis peluang dan tantangan penerapan nilai-nilai Pancasila dalam kehidupan global.","Membiasakan perilaku yang sesuai dengan nilai-nilai Pancasila sebagai identitas nasional.","Menunjukkan sikap demokratis dalam era keterbukaan informasi.","Menganalisis kasus pelanggaran hak dan pengingkaran kewajiban warga negara.","Menganalisis potensi konflik dan memberi solusi yang berkeadilan terhadap permasalahan keberagaman.","Merancang kegiatan bersama dengan prinsip gotong royong dalam praktik hidup sehari-hari.","Menganalisis ancaman, tantangan, hambatan, dan gangguan (ATHG) yang dihadapi Indonesia."]}
}

# ==============================================================================
# FUNGSI-FUNGSI GENERATOR DOKUMEN
# ==============================================================================

def petakan_ke_bidang_bk(kalimat):
    kalimat = kalimat.lower()
    if any(kata in kalimat for kata in ["karir", "profesi", "usaha", "pekerjaan", "wirausaha", "ekonomi", "peran"]): return "Karir"
    if any(kata in kalimat for kata in ["belajar", "kritis", "informasi", "keterampilan", "musyawarah", "pendapat", "sejarah"]): return "Belajar"
    if any(kata in kalimat for kata in ["sosial", "interaksi", "teman", "masyarakat", "gotong royong", "keberagaman", "bersama", "konflik"]): return "Sosial"
    return "Pribadi"

def buat_saran_kegiatan(tl):
    tl = tl.lower()
    if any(kata in tl for kata in ["menganalisis", "membandingkan", "mengevaluasi"]): return "Diskusi Kelompok, Debat Terstruktur, Analisis Studi Kasus, Membuat Peta Pikiran (Mind Mapping)."
    if any(kata in tl for kata in ["menerapkan", "mempraktikkan", "melaksanakan", "merancang", "menunjukkan"]): return "Bermain Peran (Role Playing), Simulasi, Proyek Kelompok, Membuat Poster/Infografis."
    if any(kata in tl for kata in ["memahami", "mengidentifikasi", "mengenal", "menjelaskan"]): return "Ceramah Interaktif, Menonton Video Reflektif, Curah Pendapat (Brainstorming), Games Edukatif."
    return "Diskusi dan tanya jawab, Refleksi diri."

def generate_analisis_cl(daftar_cp):
    hasil_analisis = []
    for cp in daftar_cp:
        tl_raw = cp.replace("Mengenal", "Siswa dapat mengenal").replace("Menerapkan", "Siswa dapat menerapkan").replace("Mengidentifikasi", "Siswa dapat mengidentifikasi").replace("Membedakan", "Siswa dapat membedakan").replace("Memahami", "Siswa dapat memahami").replace("Menghubungkan", "Siswa dapat menghubungkan").replace("Mengimplementasikan", "Siswa dapat mengimplementasikan").replace("Mempraktikkan", "Siswa dapat mempraktikkan").replace("Menyajikan", "Siswa dapat menyajikan").replace("Menunjukkan", "Siswa dapat menunjukkan").replace("Menggunakan", "Siswa dapat menggunakan").replace("Menerima", "Siswa dapat menerima").replace("Menumbuhkan", "Siswa dapat menumbuhkan").replace("Menganalisis", "Siswa dapat menganalisis").replace("Membiasakan", "Siswa dapat membiasakan").replace("Merancang", "Siswa dapat merancang")
        tl = tl_raw if "Siswa dapat" in tl_raw else "Siswa dapat " + tl_raw[0].lower() + tl_raw[1:]

        kktl = "Siswa menunjukkan perubahan perilaku/pemahaman yang relevan melalui observasi atau unjuk kerja."
        if "mengenal" in tl or "memahami" in tl or "mengidentifikasi" in tl: kktl = "Siswa mampu menyebutkan, menjelaskan, atau memberi contoh terkait tujuan layanan."
        elif "menerapkan" in tl or "mempraktikkan" in tl or "menunjukkan" in tl: kktl = "Siswa mampu mendemonstrasikan perilaku atau keterampilan yang diharapkan dalam simulasi atau kegiatan nyata."
        elif "menganalisis" in tl: kktl = "Siswa mampu menguraikan, membandingkan, atau menyimpulkan suatu kasus/informasi terkait tujuan layanan."
        
        hasil_analisis.append({'cp': cp, 'tl': tl, 'bidang': petakan_ke_bidang_bk(tl), 'kktl': kktl, 'kegiatan': buat_saran_kegiatan(tl)})
    return hasil_analisis

def generate_program_tahunan(analisis_data):
    prota = {'Ganjil': [], 'Genap': []}
    for item in analisis_data:
        # Asumsi sederhana: bagi 2 rata antara semester
        if len(prota['Ganjil']) <= len(prota['Genap']):
            prota['Ganjil'].append(f"({item['bidang']}) {item['tl']}")
        else:
            prota['Genap'].append(f"({item['bidang']}) {item['tl']}")
    return prota

def generate_program_semester(analisis_data, semester):
    prosem = {'Pribadi': [], 'Sosial': [], 'Belajar': [], 'Karir': []}
    for item in analisis_data:
        prosem[item['bidang']].append(item['tl'])
    
    bulan = ["Juli", "Agustus", "September", "Oktober", "November", "Desember"] if semester.lower() == 'ganjil' else ["Januari", "Februari", "Maret", "April", "Mei", "Juni"]
    return prosem, bulan

def generate_rpl_templates(analisis_data):
    templates = []
    for item in analisis_data:
        rpl = {
            'topik': item['tl'].replace("Siswa dapat ", "").capitalize(),
            'bidang': item['bidang'],
            'tujuan': item['tl'],
            'kegiatan_inti': item['kegiatan']
        }
        templates.append(rpl)
    return templates

# ==============================================================================
# LOGIKA WEBSITE (FLASK)
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

    # 1. Generate Analisis CL
    hasil_analisis = generate_analisis_cl(cp_data['cp_list'])
    
    # 2. Generate PROTA
    prota_data = generate_program_tahunan(hasil_analisis)

    # 3. Generate PROSEM
    prosem_data, bulan_prosem = generate_program_semester(hasil_analisis, data_guru['semester'])

    # 4. Generate Draf RPL
    rpl_templates = generate_rpl_templates(hasil_analisis)

    # Dapatkan tanggal hari ini
    tanggal_hari_ini = datetime.date.today().strftime('%d %B %Y')

    return render_template('hasil.html', 
                           data_guru=data_guru, 
                           fase=cp_data,
                           hasil_analisis=hasil_analisis,
                           prota_data=prota_data,
                           prosem_data=prosem_data,
                           bulan_prosem=bulan_prosem,
                           rpl_templates=rpl_templates,
                           tanggal_pembuatan=tanggal_hari_ini)

if __name__ == '__main__':
    app.run(debug=True)
