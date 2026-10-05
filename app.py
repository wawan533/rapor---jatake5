import streamlit as st
from fpdf import FPDF
import os

st.set_page_config(page_title="Rapor ASTS Jatake 5 Final", layout="wide")

def get_ket(nilai, kkm):
    if nilai >= kkm:
        if nilai >= 90: return "Tuntas, Pertahankan!"
        elif nilai >= 80: return "Tuntas"
        else: return "Belum Tuntas, Perlu Ditingkatkan"
    else:
        return "Perlu Bimbingan"

# --- SIDEBAR IDENTITAS ---
st.sidebar.header("A. Identitas Siswa")
nama = st.sidebar.text_input("Nama Peserta Didik", "Ahmad Fauzi")
nisn = st.sidebar.text_input("Nomor Induk / NISN", "0051234567")
kelas = st.sidebar.text_input("Kelas / Fase", "IV B / B")
semester = st.sidebar.selectbox("Semester", ["GANJIL","GENAP"])

st.sidebar.divider()
st.sidebar.header("B. Kehadiran & Catatan")
sakit = st.sidebar.text_input("Sakit (hari)", "0")
izin = st.sidebar.text_input("Izin (hari)", "1")
alpha = st.sidebar.text_input("Tanpa Keterangan (hari)", "0")
catatan = st.sidebar.text_area("Catatan Wali Kelas", "Ananda sangat baik dan aktif dalam pembelajaran.")
ekskul1 = st.sidebar.selectbox("Pramuka (Wajib)", ["Tuntas","Belum Tuntas","Cukup"])
ekskul2_nama = st.sidebar.text_input("Ekskul Pilihan", "Futsal")
ekskul2_val = st.sidebar.selectbox("Nilai Ekskul Pilihan", ["Baik","Sangat Baik","Cukup"])

st.sidebar.divider()
st.sidebar.header("C. TTD - Input Wali Kelas")
# INI YANG BARU
nama_wali = st.sidebar.text_input("Nama Wali Kelas", "SITI NURJANAH, S.Pd")
nip_wali = st.sidebar.text_input("NIP Wali Kelas", "198505122010012003")
# Kepala sekolah tetap default Bu Rukmini, tapi bisa diganti juga kalau mau
nama_kepsek = st.sidebar.text_input("Nama Kepala Sekolah", "RUKMINI,S.PD.SD")
nip_kepsek = st.sidebar.text_input("NIP Kepala Sekolah", "197212041993072001")

st.sidebar.divider()
st.sidebar.header("Upload 2 Logo Kop")
logo_kiri = st.sidebar.file_uploader("Logo Kiri (Kota Tangerang)", type=["png","jpg"])
logo_kanan = st.sidebar.file_uploader("Logo Kanan (SD)", type=["png","jpg"])

st.title("Input Nilai ASTS - SDN Jatake 5")
mapel_umum = [
    "Pendidikan Agama dan Budi Pekerti",
    "Pendidikan Pancasila",
    "Bahasa Indonesia",
    "Matematika",
    "Ilmu Pengetahuan Alam dan Sosial (IPAS)",
    "Seni Budaya dan Prakarya / Seni Rupa",
    "Pendidikan Jasmani, Olahraga, dan Kesehatan"
]
mapel_mulok = ["Budi Pekerti", "Bahasa Inggris"]

all_nilai = {}
cols = st.columns(3)
for i, m in enumerate(mapel_umum + mapel_mulok):
    with cols[i % 3]:
        c1,c2 = st.columns([1,1])
        with c1: kkm = st.number_input(f"KKM {m}", 0,100,75, key=f"kkm_{m}")
        with c2: nil = st.number_input(f"Nilai {m}", 0,100,85, key=f"nil_{m}")
        all_nilai[m] = (kkm, nil)

def make_pdf_final():
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(15, 10, 15)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    def save_temp(upload, name):
        if upload:
            path = f"temp_{name}.png"
            with open(path, "wb") as f:
                f.write(upload.getbuffer())
            return path
        return None
    p_kiri = save_temp(logo_kiri, "kiri")
    p_kanan = save_temp(logo_kanan, "kanan")

    if p_kiri: pdf.image(p_kiri, x=10, y=8, w=18)
    if p_kanan: pdf.image(p_kanan, x=182, y=8, w=18)

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0,4,"PEMERINTAH KOTA TANGERANG",0,1,'C')
    pdf.cell(0,4,"DINAS PENDIDIKAN",0,1,'C')
    pdf.cell(0,6,"UPT SATUAN PENDIDIKAN SD NEGERI JATAKE 5",0,1,'C')
    pdf.set_font("Arial",'',8)
    pdf.cell(0,3,"NSS : 1010 2230 4032 NPSN : 20607186",0,1,'C')
    pdf.cell(0,3,"Jl. Pajajaran Raya No.1a Kel. Gandasari Kec. Jatiuwung Kota Tangerang",0,1,'C')
    pdf.cell(0,3,"Email : upt.sp.sdnjatake5@gmail.com Pos Kode : 15137",0,1,'C')
    pdf.ln(2)
    y = pdf.get_y()
    pdf.set_line_width(0.8); pdf.line(10,y,200,y)
    pdf.set_line_width(0.3); pdf.line(10,y+1,200,y+1)
    pdf.ln(6)

    pdf.set_font("Arial",'',12)
    pdf.multi_cell(0,6,"LAPORAN HASIL ASESMEN SUMATIF TENGAH SEMESTER ( ASTS ) GANJIL\nTAHUN AJARAN 2026/2027",0,'C')
    pdf.ln(5)

    pdf.set_font("Arial",'B',10)
    pdf.cell(0,6,"A. IDENTITAS PESERTA DIDIK",0,1,'L')
    pdf.set_font("Arial",'',10)
    pdf.cell(55,6,"Nama Peserta Didik",0,0); pdf.cell(5,6,":",0,0); pdf.cell(0,6,nama,0,1)
    pdf.cell(55,6,"Nomor Induk / NISN",0,0); pdf.cell(5,6,":",0,0); pdf.cell(0,6,nisn,0,1)
    pdf.cell(55,6,"Kelas / Fase",0,0); pdf.cell(5,6,":",0,0); pdf.cell(0,6,kelas,0,1)
    pdf.cell(55,6,"Semester",0,0); pdf.cell(5,6,":",0,0); pdf.cell(0,6,semester,0,1)
    pdf.ln(3)

    pdf.set_font("Arial",'B',10)
    pdf.cell(0,6,"B. NILAI DAN CAPAIAN KOMPETENSI MATA PELAJARAN",0,1,'L')
    pdf.ln(1)
    pdf.set_font("Arial",'B',9)
    pdf.cell(10,8,"NO",1,0,'C'); pdf.cell(85,8,"MATA PELAJARAN",1,0,'C'); pdf.cell(15,8,"KKM",1,0,'C'); pdf.cell(15,8,"NILAI",1,0,'C'); pdf.cell(65,8,"KETERANGAN",1,1,'C')
    pdf.set_font("Arial",'B',9); pdf.cell(190,6,"I.KELOMPOK MATA PELAJARAN UMUM",1,1,'L')
    pdf.set_font("Arial",'',9)
    no=1
    for m in mapel_umum:
        kkm,nil = all_nilai[m]; ket = get_ket(nil, kkm)
        pdf.cell(10,6,f"{no}.",1,0,'C'); pdf.cell(85,6,m,1,0,'L'); pdf.cell(15,6,str(kkm),1,0,'C'); pdf.cell(15,6,str(nil),1,0,'C'); pdf.cell(65,6,ket,1,1,'L'); no+=1
    pdf.set_font("Arial",'B',9); pdf.cell(190,6,"II.MUATAN LOKAL",1,1,'L')
    pdf.set_font("Arial",'',9)
    for m in mapel_mulok:
        kkm,nil = all_nilai[m]; ket = get_ket(nil, kkm)
        pdf.cell(10,6,f"{no}.",1,0,'C'); pdf.cell(85,6,m,1,0,'L'); pdf.cell(15,6,str(kkm),1,0,'C'); pdf.cell(15,6,str(nil),1,0,'C'); pdf.cell(65,6,ket,1,1,'L'); no+=1

    pdf.ln(5)
    pdf.set_font("Arial",'B',10); pdf.cell(0,6,"C. Catatan Perkembangan Karakter & Ekstrakurikuler",0,1,'L')
    pdf.set_font("Arial",'',10); pdf.cell(0,6,"1. Kehadiran",0,1,'L')
    pdf.set_font("Arial",'B',10); pdf.cell(35,6,f"Sakit : {sakit} hari",0,0); pdf.cell(35,6,f"Izin : {izin} hari",0,0); pdf.cell(0,6,f"Tanpa Keterangan : {alpha} hari",0,1)
    pdf.set_font("Arial",'',10); pdf.cell(0,6,"2. Catatan Wali Kelas (Sikap & Perilaku)",0,1,'L'); pdf.multi_cell(0,5, catatan); pdf.ln(2)
    pdf.cell(0,6,f"3. Kegiatan Ekstrakurikuler :",0,1,'L'); pdf.cell(0,6,f"Pramuka (wajib): ({ekskul1}) {ekskul2_nama} (pilihan): ({ekskul2_val})",0,1,'L')

    pdf.ln(3); pdf.cell(0,6,"Tangerang, 10 Oktober 2026",0,1,'R'); pdf.ln(2)
    pdf.cell(95,6,"Mengetahui,",0,0,'L'); pdf.cell(95,6,"",0,1,'R')
    pdf.cell(95,6,"Kepala Sekolah",0,0,'L'); pdf.cell(95,6,"Wali Kelas",0,1,'L')
    pdf.cell(95,6,"SD Negeri Jatake 5",0,0,'L'); pdf.cell(95,6,"",0,1,'L')
    pdf.ln(15)
    pdf.set_font("Arial",'B',10)
    pdf.cell(95,6,nama_kepsek.upper(),0,0,'L'); pdf.cell(95,6,nama_wali.upper(),0,1,'L')
    pdf.set_font("Arial",'',9)
    pdf.cell(95,6,f"NIP.{nip_kepsek}",0,0,'L'); pdf.cell(95,6,f"NIP.{nip_wali}",0,1,'L')

    for p in [p_kiri, p_kanan]:
        if p and os.path.exists(p):
            try: os.remove(p)
            except: pass
    return bytes(pdf.output())

if st.button("💾 SIMPAN & BUAT PDF", type="primary"):
    pdf_bytes = make_pdf_final()
    st.success(f"PDF jadi atas nama wali kelas: {nama_wali}")
    st.download_button("📥 DOWNLOAD PDF RESMI JATAKE 5", data=pdf_bytes, file_name=f"RAPOR_ASTS_{nama}_{kelas}.pdf", mime="application/pdf")