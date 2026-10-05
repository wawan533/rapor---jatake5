import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from fpdf import FPDF
import os

if 'rekap_data' not in st.session_state:
    st.session_state.rekap_data = []

st.set_page_config(page_title="Input Nilai ASTS - SDN Jatake 5", layout="wide")
st.title("📘 Input Nilai ASTS - SDN Jatake 5")

# --- SIDEBAR INPUT ---
col_kiri, col_kanan = st.columns([1, 2.5])
with col_kiri:
    st.subheader("A. Identitas Siswa")
    nama = st.text_input("Nama Peserta Didik", "")
    nisn = st.text_input("NISN / NIS", "")
    kelas = st.text_input("Kelas / Fase", "IV B / B")
    semester = st.selectbox("Semester", ["GANJIL", "GENAP"], 0)
    tahun_ajaran = st.text_input("Tahun Ajaran", "2024/2025")
    st.divider()
    st.subheader("B. Kehadiran & Catatan")
    sakit = st.number_input("Sakit (hari)", 0, 100, 0)
    izin = st.number_input("Izin (hari)", 0, 100, 0)
    alpa = st.number_input("Tanpa Keterangan (hari)", 0, 100, 0)
    catatan = st.text_area("Catatan Wali Kelas", "Adalah siswa yang rajin...")

with col_kanan:
    st.subheader("C. Nilai Mata Pelajaran")
    mapel_list = [
        ("Pendidikan Agama dan Budi Pekerti", "agama"),
        ("Pendidikan Pancasila", "pancasila"),
        ("Bahasa Indonesia", "bindo"),
        ("Matematika", "mtk"),
        ("IPAS", "ipas"),
        ("Seni Budaya / Seni Rupa", "seni"),
        ("PJOK", "pjok"),
        ("Budi Pekerti", "budi"),
        ("Bahasa Inggris", "inggris"),
    ]
    nilai_data = {}
    cols = st.columns(3)
    for i, (label, key) in enumerate(mapel_list):
        with cols[i % 3]:
            st.markdown(f"**{label}**")
            c1, c2 = st.columns(2)
            kkm = c1.number_input(f"KKM", 0, 100, 75, key=f"kkm_{key}")
            nilai = c2.number_input(f"Nilai", 0, 100, 85, key=f"nilai_{key}")
            nilai_data[label] = {"kkm": kkm, "nilai": nilai}

    st.divider()
    if st.button("💾 SIMPAN KE REKAP & BUAT PDF", type="primary", use_container_width=True):
        # 1. Simpan ke Rekap
        baris = {"Waktu": datetime.now().strftime("%d-%m-%Y %H:%M"), "Nama": nama, "NISN": nisn, "Kelas": kelas}
        for mp, v in nilai_data.items():
            baris[f"{mp} (Nilai)"] = v["nilai"]
        st.session_state.rekap_data.append(baris)

        # 2. Buat PDF Bagus
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, "SD NEGERI JATAKE 5", align="C", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, "Jl. Raya Serang Km. 15, Kec. Jatiuwung, Kota Tangerang", align="C", ln=True)
        pdf.line(10, 25, 200, 25)
        pdf.ln(8)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"LAPORAN HASIL BELAJAR (ASTS) - Semester {semester}", align="C", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"Nama: {nama} | NISN: {nisn} | Kelas: {kelas} | TA: {tahun_ajaran}", ln=True)
        pdf.ln(4)
        # Tabel Nilai
        pdf.set_font("Arial", "B", 11)
        pdf.cell(10, 8, "No", 1, 0, "C")
        pdf.cell(80, 8, "Mata Pelajaran", 1, 0, "C")
        pdf.cell(25, 8, "KKM", 1, 0, "C")
        pdf.cell(25, 8, "Nilai", 1, 0, "C")
        pdf.cell(50, 8, "Predikat", 1, 1, "C")
        pdf.set_font("Arial", "", 11)
        no = 1
        for mp, v in nilai_data.items():
            pred = "A" if v['nilai']>=90 else "B" if v['nilai']>=80 else "C"
            pdf.cell(10, 7, str(no), 1, 0, "C")
            pdf.cell(80, 7, f" {mp}", 1, 0, "L")
            pdf.cell(25, 7, str(v['kkm']), 1, 0, "C")
            pdf.cell(25, 7, str(v['nilai']), 1, 0, "C")
            pdf.cell(50, 7, pred, 1, 1, "C")
            no+=1
        pdf.ln(5)
        pdf.cell(0, 6, f"Kehadiran: Sakit {sakit} hari, Izin {izin} hari, Alpa {alpa} hari", ln=True)
        pdf.multi_cell(0, 6, f"Catatan Wali Kelas: {catatan}")
        pdf.ln(10)
        pdf.cell(0, 6, f"Tangerang, {datetime.now().strftime('%d %B %Y')}", align="R", ln=True)
        pdf.cell(0, 6, "Wali Kelas,", align="R", ln=True)
        pdf.ln(15)
        pdf.cell(0, 6, f"( {nama} )", align="R", ln=True)

        pdf_bytes = bytes(pdf.output())
        st.success(f"Berhasil! Data {nama} masuk rekap.")
        st.download_button("📄 DOWNLOAD PDF Rapor yang B A G U S", data=pdf_bytes, file_name=f"Rapor_{nama}_{kelas}.pdf", mime="application/pdf", type="primary", use_container_width=True)

st.divider()
st.header("📊 Rekap Data Tersimpan (Tidak Hilang Selama Browser Terbuka)")
if len(st.session_state.rekap_data) == 0:
    st.info("Belum ada data.")
else:
    df = pd.DataFrame(st.session_state.rekap_data)
    st.dataframe(df, use_container_width=True)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Rekap Nilai")
    output.seek(0)
    st.download_button("📥 DOWNLOAD REKAP EXCEL SEMUA SISWA", data=output, file_name=f"Rekap_Jatake5_{datetime.now().strftime('%Y%m%d')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary")
