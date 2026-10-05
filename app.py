import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from fpdf import FPDF

if 'rekap_data' not in st.session_state:
    st.session_state.rekap_data = []

st.set_page_config(page_title="Input Nilai ASTS - SDN Jatake 5", layout="wide")
st.title("Input Nilai ASTS - SDN Jatake 5")

col_kiri, col_kanan = st.columns([1, 3])

with col_kiri:
    st.subheader("A. Identitas Siswa")
    nama = st.text_input("Nama Peserta Didik", value="")
    nisn = st.text_input("Nomor Induk / NISN", value="")
    kelas = st.text_input("Kelas / Fase", value="IV B / B")
    semester = st.selectbox("Semester", ["GANJIL", "GENAP"], index=0)
    st.divider()
    st.subheader("B. Kehadiran & Catatan")
    sakit = st.number_input("Sakit", 0, 100, 0)
    izin = st.number_input("Izin", 0, 100, 0)
    alpa = st.number_input("Tanpa Keterangan", 0, 100, 0)
    catatan = st.text_area("Catatan Wali Kelas")

with col_kanan:
    st.subheader("Nilai")
    mapel_list = [
        ("Agama dan Budi Pekerti", "agama"),
        ("Pancasila", "pancasila"),
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
            kkm = c1.number_input(f"KKM {label}", 0, 100, 75, key=f"kkm_{key}")
            nilai = c2.number_input(f"Nilai {label}", 0, 100, 85, key=f"nilai_{key}")
            nilai_data[label] = {"kkm": kkm, "nilai": nilai}

    if st.button("💾 SIMPAN & BUAT PDF", type="primary", use_container_width=True):
        baris = {"Waktu": datetime.now().strftime("%d-%m-%Y %H:%M"), "Nama": nama, "NISN": nisn, "Kelas": kelas, "Semester": semester, "Sakit": sakit, "Izin": izin, "Alpa": alpa}
        for mp, v in nilai_data.items():
            baris[f"{mp} (KKM)"] = v["kkm"]; baris[f"{mp} (Nilai)"] = v["nilai"]
        baris["Catatan"] = catatan
        st.session_state.rekap_data.append(baris)
        st.success(f"Data {nama} masuk rekap! Total {len(st.session_state.rekap_data)} siswa.")
        pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", "B", 14); pdf.cell(0, 10, f"Rapor ASTS - {nama}", ln=True, align="C")
        pdf.set_font("Arial", "", 11); pdf.cell(0, 8, f"NISN: {nisn} | Kelas: {kelas} | Semester: {semester}", ln=True); pdf.ln(5)
        for mp, v in nilai_data.items(): pdf.cell(0, 7, f"{mp}: KKM {v['kkm']} - Nilai {v['nilai']}", ln=True)
        pdf.ln(5); pdf.cell(0, 7, f"Kehadiran S:{sakit} I:{izin} A:{alpa}", ln=True); pdf.multi_cell(0, 7, f"Catatan: {catatan}")
        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        st.download_button("📄 DOWNLOAD PDF RAPOR INI", data=pdf_bytes, file_name=f"Rapor_{nama}_{kelas}.pdf", mime="application/pdf")

st.divider()
st.header("📊 Rekap Data Tersimpan")
if len(st.session_state.rekap_data) == 0:
    st.info("Belum ada data. Isi di atas lalu klik SIMPAN.")
else:
    df = pd.DataFrame(st.session_state.rekap_data); st.dataframe(df, use_container_width=True)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer: df.to_excel(writer, index=False, sheet_name="Rekap Nilai")
    output.seek(0)
    col1, col2 = st.columns(2)
    col1.download_button("📥 DOWNLOAD REKAP EXCEL (Semua Siswa)", data=output, file_name=f"Rekap_Rapor_Jatake5_{datetime.now().strftime('%Y%m%d')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", type="primary", use_container_width=True)
    if col2.button("🗑️ Hapus Semua Rekap", use_container_width=True): st.session_state.rekap_data = []; st.rerun()
