import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from fpdf import FPDF

if 'rekap_data' not in st.session_state:
    st.session_state.rekap_data = []

st.set_page_config(page_title="Input Nilai ASTS - SDN Jatake 5", layout="wide")
st.title("📘 Input Nilai ASTS - SDN Jatake 5")

col_kiri, col_kanan = st.columns([1, 2.5])
with col_kiri:
    st.subheader("A. Identitas Siswa")
    nama = st.text_input("Nama Peserta Didik", "aDE")
    nisn = st.text_input("Nomor Induk / NISN", "0051234567")
    kelas = st.text_input("Kelas / Fase", "VI C")
    semester = st.selectbox("Semester", ["GANJIL", "GENAP"], 0)
    tahun_ajaran = st.text_input("Tahun Ajaran", "2026/2027")
    st.divider()
    st.subheader("C. Kehadiran & Catatan")
    sakit = st.text_input("Sakit", "01 hari")
    izin = st.text_input("Izin", "1 hari")
    alpa = st.text_input("Tanpa Keterangan", "0 hari")
    catatan = st.text_area("Catatan Wali Kelas", "Ananda sangat baik dan aktif dalam pembelajaran.")
    ekskul = st.text_input("Ekstrakurikuler", "Pramuka (wajib): (Tuntas) Futsal (pilihan): (Baik)")
    kepsek = st.text_input("Nama Kepsek", "RUKMINI,S.PD.SD")
    nip_kepsek = st.text_input("NIP Kepsek", "197212041993072001")
    wali = st.text_input("Nama Wali Kelas", "LINDAWATI, S.PD")
    nip_wali = st.text_input("NIP Wali", "198505122010012003")

with col_kanan:
    st.subheader("B. Nilai Mapel")
    mapel = [
        ("I. KELOMPOK MATA PELAJARAN UMUM", ""),
        ("Pendidikan Agama dan Budi Pekerti", "agama"),
        ("Pendidikan Pancasila", "pancasila"),
        ("Bahasa Indonesia", "bindo"),
        ("Matematika", "mtk"),
        ("Ilmu Pengetahuan Alam dan Sosial (IPAS)", "ipas"),
        ("Seni Budaya dan Prakarya / Seni Rupa", "seni"),
        ("Pendidikan Jasmani, Olahraga, dan Kesehatan", "pjok"),
        ("II. MUATAN LOKAL", ""),
        ("Budi Pekerti", "budi"),
        ("Bahasa Inggris", "inggris"),
    ]
    nilai_data = {}
    for label, key in mapel:
        if key == "":
            st.markdown(f"**{label}**")
        else:
            c1, c2, c3 = st.columns([3,1,1])
            c1.write(label)
            kkm = c2.number_input(f"KKM {key}", 0, 100, 75, key=f"kkm_{key}")
            nilai = c3.number_input(f"Nilai {key}", 0, 100, 85, key=f"nilai_{key}")
            nilai_data[label] = {"kkm": kkm, "nilai": nilai}

    if st.button("💾 SIMPAN & BUAT PDF SESUAI TEMPLATE ASLI", type="primary", use_container_width=True):
        baris = {"Nama": nama, "NISN": nisn, "Kelas": kelas}
        for mp, v in nilai_data.items(): baris[mp] = v["nilai"]
        st.session_state.rekap_data.append(baris)

        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        # KOP DENGAN LOGO
        if os.path.exists("logo.png"):
        pdf.image("logo.png", x=15, y=8, w=18)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 5, "PEMERINTAH KOTA TANGERANG", align="C", ln=True)
        pdf.cell(0, 5, "DINAS PENDIDIKAN", align="C", ln=True)
        pdf.cell(0, 5, "UPT SATUAN PENDIDIKAN SD NEGERI JATAKE 5", align="C", ln=True)
        pdf.set_font("Arial", "", 8)
        pdf.cell(0, 4, "NSS : 1010 2230 4032 NPSN : 20607186", align="C", ln=True)
        pdf.cell(0, 4, "Jl. Pajajaran Raya No.1a Kel. Gandasari Kec. Jatiuwung Kota Tangerang", align="C", ln=True)
        pdf.cell(0, 4, "Email : upt.sp.sdnjatake5@gmail.com Pos Kode : 15137", align="C", ln=True)
        pdf.line(10, 32, 200, 32)
        pdf.ln(4)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"LAPORAN HASIL ASESMEN SUMATIF TENGAH SEMESTER ( ASTS ) {semester}", align="C", ln=True)
        pdf.cell(0, 6, f"TAHUN AJARAN {tahun_ajaran}", align="C", ln=True)
        pdf.ln(3)
        # Identitas
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, "A. IDENTITAS PESERTA DIDIK", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(45, 6, "Nama Peserta Didik"); pdf.cell(0, 6, f": {nama}", ln=True)
        pdf.cell(45, 6, "Nomor Induk / NISN"); pdf.cell(0, 6, f": {nisn}", ln=True)
        pdf.cell(45, 6, "Kelas / Fase"); pdf.cell(0, 6, f": {kelas}", ln=True)
        pdf.cell(45, 6, "Semester"); pdf.cell(0, 6, f": {semester}", ln=True)
        pdf.ln(2)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, "B. NILAI DAN CAPAIAN KOMPETENSI MATA PELAJARAN", ln=True)
        # Header Tabel
        pdf.set_font("Arial", "B", 10)
        pdf.cell(10, 8, "NO", 1, 0, "C")
        pdf.cell(95, 8, "MATA PELAJARAN", 1, 0, "C")
        pdf.cell(20, 8, "KKM", 1, 0, "C")
        pdf.cell(20, 8, "NILAI", 1, 0, "C")
        pdf.cell(45, 8, "KETERANGAN", 1, 1, "C")
        pdf.set_font("Arial", "", 10)
        no = 1
        for label, key in mapel:
            if key == "":
                pdf.set_font("Arial", "B", 10)
                pdf.cell(190, 7, label, 1, 1, "L")
                pdf.set_font("Arial", "", 10)
            else:
                v = nilai_data[label]
                ket = "Tuntas" if v["nilai"] >= v["kkm"] else "Belum Tuntas"
                pdf.cell(10, 7, f"{no}.", 1, 0, "C")
                pdf.cell(95, 7, f" {label}", 1, 0, "L")
                pdf.cell(20, 7, str(v["kkm"]), 1, 0, "C")
                pdf.cell(20, 7, str(v["nilai"]), 1, 0, "C")
                pdf.cell(45, 7, ket, 1, 1, "C")
                no+=1
        pdf.ln(3)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, "C. Catatan Perkembangan Karakter & Ekstrakurikuler", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, f"1. Kehadiran Sakit : {sakit} Izin : {izin} Tanpa Keterangan : {alpa}", ln=True)
        pdf.cell(0, 6, "2. Catatan Wali Kelas (Sikap & Perilaku)", ln=True)
        pdf.multi_cell(0, 6, catatan)
        pdf.cell(0, 6, f"3. Kegiatan Ekstrakurikuler : {ekskul}", ln=True)
        pdf.ln(5)
        pdf.cell(0, 6, f"Tangerang, {datetime.now().strftime('%d %B %Y')}", align="R", ln=True)
        pdf.cell(0, 6, "Mengetahui,", align="L", ln=True)
        pdf.cell(90, 6, "Kepala Sekolah", align="C")
        pdf.cell(90, 6, "Wali Kelas", align="C", ln=True)
        pdf.cell(90, 6, "SD Negeri Jatake 5", align="C", ln=True)
        pdf.ln(12)
        pdf.cell(90, 6, kepsek, align="C")
        pdf.cell(90, 6, wali, align="C", ln=True)
        pdf.set_font("Arial", "", 8)
        pdf.cell(90, 4, f"NIP.{nip_kepsek}", align="C")
        pdf.cell(90, 4, f"NIP.{nip_wali}", align="C", ln=True)

        # INI YANG BENER, ANTI ERROR
        pdf_bytes = bytes(pdf.output())
        st.success("PDF Berhasil dibuat sesuai template asli!")
        st.download_button("📄 DOWNLOAD PDF (Format Asli)", data=pdf_bytes, file_name=f"RAPOR_ASTS_{nama}_{kelas}.pdf", mime="application/pdf", type="primary", use_container_width=True)

st.divider()
st.header("📊 Rekap Data Tersimpan")
if st.session_state.rekap_data:
    df = pd.DataFrame(st.session_state.rekap_data)
    st.dataframe(df, use_container_width=True)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer: df.to_excel(writer, index=False)
    output.seek(0)
    st.download_button("📥 DOWNLOAD REKAP EXCEL", data=output, file_name=f"Rekap_Jatake5.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
