import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import subprocess
import os

doc = Document()

# Set standard page margins (1 inch)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Colors
COLOR_PRIMARY = RGBColor(24, 76, 120)     # Deep Blue
COLOR_DARK = RGBColor(33, 37, 41)         # Off Black
COLOR_MUTED = RGBColor(108, 117, 125)     # Gray

def style_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p

def style_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p

def add_body(text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = COLOR_DARK
    return p

def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_DARK
    return p

def add_code_block(code_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Inches(0.2)
    run = p.add_run(code_text)
    run.font.name = "Courier New"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(40, 40, 40)
    # Background shading
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F3F5"/>')
    p._p.get_or_add_pPr().append(shd)
    return p

# Document Title
p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(2)
r_title = p_title.add_run("Panduan Instalasi dan Penggunaan")
r_title.font.name = "Arial"
r_title.font.size = Pt(22)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_PRIMARY

p_sub = doc.add_paragraph()
p_sub.paragraph_format.space_after = Pt(14)
r_sub = p_sub.add_run("User & Deployment Guide — Aplikasi Chat TCP Multi-Client Berbasis Terminal")
r_sub.font.name = "Calibri"
r_sub.font.size = Pt(12)
r_sub.font.italic = True
r_sub.font.color.rgb = COLOR_MUTED

# Divider line
p_div = doc.add_paragraph()
p_div.paragraph_format.space_after = Pt(10)
p_div_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="184C78"/></w:pBdr>')
p_div._p.get_or_add_pPr().append(p_div_border)

# Section 1
style_heading_1("1. Prasyarat Perangkat Lunak dan Lingkungan")
add_body("Aplikasi chat ini dirancang menggunakan pustaka standar (standard library) Python 3 tanpa ketergantungan paket eksternal (zero third-party dependencies). Hal ini memastikan portabilitas tinggi dan kemudahan deployment di berbagai platform sistem operasi.")

add_bullet(" Linux, macOS, atau Windows.", "Sistem Operasi: ")
add_bullet(" Python 3.8 atau versi lebih tinggi.", "Runtime: ")
add_bullet(" Modul bawaan standard library:", "Pustaka Python: ")

add_bullet("pengelolaan koneksi jaringan socket TCP berorientasi stream (AF_INET, SOCK_STREAM).", "  • socket: ")
add_bullet("pengelolaan konkurensi multi-thread (satu thread listener dan thread independen per client).", "  • threading: ")
add_bullet("serialisasi dan deserialisasi frame pesan berbasis format teks JSON.", "  • json: ")
add_bullet("pemberian timestamp waktu lokal server dan client (format HH:MM:SS).", "  • time: ")
add_bullet("antarmuka I/O terminal dan pemrosesan argumen baris perintah.", "  • sys: ")
add_bullet("penanganan error level socket sistem operasi.", "  • errno: ")

add_bullet(" Port TCP 6767 terbuka pada firewall host server (atau port alternatif yang disepakati). Mendukung pengujian pada localhost (127.0.0.1) maupun Local Area Network (LAN/Wi-Fi).", "Kebutuhan Jaringan: ")

# Section 2
style_heading_1("2. Langkah-Langkah Instalasi dan Konfigurasi")
add_body("Berikut adalah tahapan mempersiapkan repositori proyek di komputer lokal:")

add_body("Buka antarmuka baris perintah (Terminal pada macOS/Linux atau CMD/PowerShell pada Windows) lalu unduh repositori dari GitHub:", "Langkah 1: Kloning Repositori — ")
add_code_block("git clone https://github.com/Fathzzzzz/OHMayJarkomz.git\ncd OHMayJarkomz")

add_body("Pastikan seluruh berkas program dan dokumentasi telah berada di dalam folder:", "Langkah 2: Verifikasi Berkas — ")
add_bullet("Program utama server socket TCP dan pengelola sesi client.", "server.py: ")
add_bullet("Program antarmuka terminal client dan penerima pesan asinkron.", "client.py: ")
add_bullet("Dokumentasi spesifikasi protokol payload JSON.", "protocol.md: ")
add_bullet("Petunjuk ringkas pengoperasian aplikasi.", "README.md: ")

# Section 3
style_heading_1("3. Prosedur Menjalankan Server dan Client")

style_heading_2("A. Menjalankan Server")
add_body("Server bertindak sebagai pusat pengelolaan koneksi dan perutean seluruh pesan chat. Server harus dijalankan terlebih dahulu sebelum client terhubung.")
add_body("Perintah eksekusi server dari direktori proyek:")
add_code_block("python3 server.py")
add_body("Keterangan Operasional Server:")
add_bullet(" Server melakukan bind ke interface 0.0.0.0 pada port 6767 sehingga siap menerima koneksi dari localhost maupun alamat IP jaringan fisik.")
add_bullet(" Thread utama server menjalankan listen(50) dan accept loop non-blocking secara asinkron via thread worker.")
add_bullet(" Tekan tombol kombinasi Ctrl + C pada terminal server untuk menghentikan layanan secara rapi (graceful shutdown).")

style_heading_2("B. Menjalankan Client")
add_body("Program client terminal dapat dijalankan pada komputer yang sama dengan server atau komputer berbeda di jaringan lokal.")

add_body("Jalankan perintah berikut pada terminal baru:", "Skenario 1 — Menjalankan di Satu Komputer (Localhost):")
add_code_block("python3 client.py")
add_body("(Client secara otomatis menggunakan target default 127.0.0.1 pada port 6767).")

add_body("Jalankan perintah dengan menyertakan parameter alamat IP host server dan port:", "Skenario 2 — Menjalankan di Komputer Berbeda (Jaringan LAN / Wi-Fi):")
add_code_block("python3 client.py <IP_SERVER> 6767\n# Contoh:\npython3 client.py 192.168.1.50 6767")

style_heading_2("C. Panduan Input dan Sintaks Perintah Client")
add_body("Saat pertama kali dijalankan, pengguna diminta memasukkan username unik (1–20 karakter, tanpa spasi, tidak diawali karakter '/'). Setelah server memvalidasi nama, pengguna dapat menggunakan perintah berikut:")

# Table for commands
table = doc.add_table(rows=1, cols=3)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table.rows[0].cells
headers = ["Perintah / Format", "Fungsi dan Keterangan", "Contoh Penggunaan"]
col_widths = [Inches(1.8), Inches(2.7), Inches(2.0)]

for i, h_text in enumerate(headers):
    hdr_cells[i].text = h_text
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="184C78"/>')
    hdr_cells[i]._tc.get_or_add_tcPr().append(shd)
    for p in hdr_cells[i].paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)

cmd_data = [
    ("<teks biasa>", "Mengirim pesan publik ke seluruh client aktif (broadcast).", "Halo rekan-rekan semua!"),
    ("/pm <user> <pesan>", "Mengirim pesan privat khusus ke satu pengguna aktif.", "/pm Jundan mohon cek dokumen"),
    ("/users", "Menampilkan daftar seluruh username yang sedang online.", "/users"),
    ("/help", "Menampilkan daftar bantuan perintah di layar terminal.", "/help"),
    ("/quit atau /exit", "Memutuskan koneksi socket dan keluar secara rapi.", "/quit")
]

for row_idx, data in enumerate(cmd_data):
    row_cells = table.add_row().cells
    bg_hex = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
    for c_idx, cell_value in enumerate(data):
        row_cells[c_idx].text = cell_value
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_hex}"/>')
        row_cells[c_idx]._tc.get_or_add_tcPr().append(shd)
        for p in row_cells[c_idx].paragraphs:
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(9.5)
                run.font.color.rgb = COLOR_DARK

# Set widths
for row in table.rows:
    for idx, width in enumerate(col_widths):
        row.cells[idx].width = width

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 4
style_heading_1("4. Pengujian Sistem Multi-Client")
add_body("Pengujian dilakukan untuk membuktikan keandalan server dalam menangani banyak client secara simultan melalui arsitektur multi-threading.")

add_body("Rangkaian Skenario Pengujian:", space_after=2)
add_bullet(" Inisialisasi proses server socket TCP yang mendengarkan port 6767.", "1. Server Standby: ")
add_bullet(" Tiga client terhubung secara bergantian dengan identitas Fathan, Jundan, dan Radis. Server memperbarui registry pengguna aktif dan menyiarkan notifikasi bergabung.", "2. Join Multi-Client: ")
add_bullet(" Client Fathan mengirim pesan publik. Pesan disiarkan secara serentak ke seluruh client aktif.", "3. Komunikasi Publik: ")
add_bullet(" Pengguna Jundan mengirim pesan pribadi (/pm Radis ...) yang hanya diterima oleh Radis dan dikonfirmasi ke Jundan tanpa bocor ke Fathan.", "4. Komunikasi Privat (PM): ")
add_bullet(" Pengguna Radis melakukan kueri daftar user online via perintah /users.", "5. Kueri Pengguna Online: ")
add_bullet(" Pengguna Radis mengeksekusi /quit. Server menutup koneksi secara bersih dan mengumumkan pembaruan user online kepada client yang tersisa tanpa interupsi.", "6. Graceful Disconnect: ")

add_body("Screenshot Bukti Pengujian Multi-Client:", bold_prefix=None, space_after=4)

# Embed image
img_path = "/Users/rpurusa/OHMayJarkomz/screenshot_pengujian_multi_client.png"
if os.path.exists(img_path):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(6.4))

p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.paragraph_format.space_after = Pt(8)
r_cap = p_cap.add_run("Gambar 1: Tangkapan Layar Pengujian 1 Server dan 3 Client Terhubung Sekaligus")
r_cap.font.name = "Calibri"
r_cap.font.size = Pt(9.5)
r_cap.font.italic = True
r_cap.font.color.rgb = COLOR_MUTED

add_body("Deskripsi Panel Pengujian:", space_after=2)
add_bullet(" Memperlihatkan log aktivitas daemon, pembentukan thread worker client (client-127.0.0.1:port), pencatatan pesan siaran, dan rute PM.", "• Terminal 1 (Kiri Atas - Server): ")
add_bullet(" Client Fathan menerima notifikasi bertahap saat Jundan dan Radis bergabung, serta pesan broadcast.", "• Terminal 2 (Kanan Atas - Client Fathan): ")
add_bullet(" Client Jundan menerima pesan publik dan melakukan percakapan privat eksklusif dengan Radis.", "• Terminal 3 (Kiri Bawah - Client Jundan): ")
add_bullet(" Client Radis membalas pesan PM, memeriksa daftar user (/users), dan melakukan pemutusan sesi mandiri (/quit).", "• Terminal 4 (Kanan Bawah - Client Radis): ")

output_docx = "/Users/rpurusa/OHMayJarkomz/Panduan_Instalasi_dan_Penggunaan.docx"
output_docx_dl = "/Users/rpurusa/Downloads/Panduan_Instalasi_dan_Penggunaan.docx"
doc.save(output_docx)
doc.save(output_docx_dl)
print(f"DOCX created: {output_docx}")

# Convert to PDF
try:
    cmd = ["/opt/homebrew/bin/soffice", "--headless", "--convert-to", "pdf", output_docx, "--outdir", "/Users/rpurusa/OHMayJarkomz"]
    subprocess.run(cmd, check=True)
    subprocess.run(["/opt/homebrew/bin/soffice", "--headless", "--convert-to", "pdf", output_docx_dl, "--outdir", "/Users/rpurusa/Downloads"], check=True)
    print("PDF conversion successful via LibreOffice")
except Exception as e:
    print("PDF conversion error:", e)
