import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# =====================================================
# 1. KONFIGURASI HALAMAN & STATE TEMA
# =====================================================
st.set_page_config(
    page_title="Pembangkit Kurva Parametrik V3",
    page_icon="📈",
    layout="wide"
)

# Inisialisasi tema default ke Dark Mode jika belum diset
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# =====================================================
# 2. INJEKSI CUSTOM CSS UNTUK TEMA DINAMIS
# =====================================================
def inject_custom_css(theme):
    if theme == 'dark':
        css = """
        <style>
        :root {
            --bg-color: #0e1117;
            --text-color: #f8f9fa;
            --sidebar-bg: #161922;
            --card-bg: #1f2330;
            --accent-color: #00FFCC;
            --accent-hover: #00CCaa;
            --border-color: #2e3440;
            --shadow-color: rgba(0, 0, 0, 0.4);
        }
        
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Inter', 'Outfit', 'Segoe UI', sans-serif;
        }
        
        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
        }
        
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p,
        [data-testid="stSidebar"] .stMarkdown p {
            color: #E0E0E0 !important;
        }
        
        .stDataFrame, div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-color) !important;
            box-shadow: 0 4px 12px var(--shadow-color);
            background-color: var(--card-bg);
        }
        
        div[data-testid="stVerticalBlockBorderContainer"] {
            background-color: var(--card-bg) !important;
            border-radius: 12px !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: 0 4px 12px var(--shadow-color) !important;
            padding: 1.5rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        .stButton>button {
            background-color: var(--accent-color) !important;
            color: #0e1117 !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 700 !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 2px 4px var(--shadow-color) !important;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: var(--accent-hover) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px var(--shadow-color) !important;
        }
        
        h1, h2, h3 {
            color: var(--text-color) !important;
            font-weight: 700;
        }
        
        .title-gradient {
            background: linear-gradient(90deg, #00FFCC, #00b3ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        
        button[data-baseweb="tab"] {
            color: #9ca3af !important;
            font-weight: 600 !important;
            background-color: transparent !important;
            border-bottom: 2px solid transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--accent-color) !important;
            border-bottom: 2px solid var(--accent-color) !important;
        }
        
        * {
            transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
        }
        </style>
        """
    else:
        css = """
        <style>
        :root {
            --bg-color: #f8f9fa;
            --text-color: #333333;
            --sidebar-bg: #ffffff;
            --card-bg: #ffffff;
            --accent-color: #008080;
            --accent-hover: #006666;
            --border-color: #e9ecef;
            --shadow-color: rgba(0, 0, 0, 0.05);
        }
        
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Inter', 'Outfit', 'Segoe UI', sans-serif;
        }
        
        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
        }
        
        .stDataFrame, div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-color) !important;
            box-shadow: 0 4px 12px var(--shadow-color);
            background-color: var(--card-bg);
        }
        
        div[data-testid="stVerticalBlockBorderContainer"] {
            background-color: var(--card-bg) !important;
            border-radius: 12px !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: 0 4px 12px var(--shadow-color) !important;
            padding: 1.5rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        .stButton>button {
            background-color: var(--accent-color) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 2px 4px var(--shadow-color) !important;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: var(--accent-hover) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px var(--shadow-color) !important;
        }
        
        h1, h2, h3 {
            color: var(--text-color) !important;
            font-weight: 700;
        }
        
        .title-gradient {
            background: linear-gradient(90deg, #008080, #005555);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        
        button[data-baseweb="tab"] {
            color: #6b7280 !important;
            font-weight: 600 !important;
            background-color: transparent !important;
            border-bottom: 2px solid transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--accent-color) !important;
            border-bottom: 2px solid var(--accent-color) !important;
        }
        
        /* Memberikan border dan shadow pada input parameter di sidebar saat Light Mode agar tidak samar */
        [data-testid="stSidebar"] div[data-baseweb="input"], 
        [data-testid="stSidebar"] div[data-baseweb="select"] {
            border: 1px solid #cccccc !important;
            border-radius: 6px !important;
            background-color: #ffffff !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
            transition: border-color 0.2s ease-in-out !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="input"]:focus-within, 
        [data-testid="stSidebar"] div[data-baseweb="select"]:focus-within {
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 1px var(--accent-color) !important;
        }
        [data-testid="stSidebar"] input {
            color: #333333 !important;
        }
        [data-testid="stSidebar"] div[data-baseweb="select"] * {
            color: #333333 !important;
        }
        
        * {
            transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css(st.session_state.theme)

# =====================================================
# 3. VISUALISASI UTAMA (GAYA DASHBOARD CLEAN & BINGKAI LUAR)
# =====================================================
def tampilkan_gaya_pro(param_array, x1, y1, xc, yc, a, b, title, n_pts, step, teks_panel, tipe_kurva="ELIPS", x2=None, y2=None):
    """
    Membuat grafik tunggal dengan sumbu koordinat berada di pinggir (bingkai/box).
    Menampilkan teks_panel yang dinamis sesuai tipe kurva di sebelah kanan.
    Menyesuaikan skema warna secara dinamis berdasarkan tema gelap/terang.
    """
    is_dark = st.session_state.get('theme', 'dark') == 'dark'
    
    # Skema warna dinamis
    if is_dark:
        plt.style.use('dark_background')
        warna_kurva = '#00FFCC'   # Cyan-Neon
        warna_kurva2 = '#FF007F'  # Magenta-Neon
        warna_titik = '#FFFFFF'   # Putih
        warna_teks  = '#E0E0E0'
        warna_bg = '#0e1117'
        warna_box = '#0B1320'
        warna_spine = 'white'
        warna_grid = 'gray'
    else:
        plt.style.use('default')
        warna_kurva = '#008080'   # Teal
        warna_kurva2 = '#D11A5B'  # Crimson/Magenta
        warna_titik = '#000000'   # Hitam
        warna_teks  = '#333333'
        warna_bg = '#f8f9fa'
        warna_box = '#E2E8F0'
        warna_spine = 'black'
        warna_grid = 'gray'

    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor(warna_bg)
    ax.set_facecolor(warna_bg)
    fig.subplots_adjust(left=0.08, right=0.70, top=0.88, bottom=0.10)

    # Judul Utama Gambar
    fig.suptitle(
        f"✦ VISUALISASI {tipe_kurva} PARAMETRIK ✦\nResolusi: {title} | Delta = {step:.4f}",
        fontsize=12, fontweight='bold', color=warna_kurva, y=0.96
    )

    # Plot Jalur Kurva dan Titik Sampel
    if x2 is not None and y2 is not None:
        ax.plot(x1, y1, color=warna_kurva, linewidth=2.5, zorder=2, label='Cabang Kanan')
        ax.plot(x2, y2, color=warna_kurva2, linewidth=2.5, zorder=2, label='Cabang Kiri')
        ax.scatter(x1, y1, color=warna_titik, s=25, zorder=3, edgecolors='black', lw=0.5)
        ax.scatter(x2, y2, color=warna_titik, s=25, zorder=3, edgecolors='black', lw=0.5)
    else:
        ax.plot(x1, y1, color=warna_kurva, linewidth=2.5, zorder=2, label=f'Kurva {tipe_kurva.title()}')
        ax.scatter(x1, y1, color=warna_titik, s=25, zorder=3, edgecolors='black', lw=0.5, label=f'Koordinat ({n_pts} titik)')

    # Titik Pusat / Vertex
    ax.scatter(xc, yc, color='#FFFF00' if is_dark else '#D97706', s=100, marker='P', zorder=5)
    ax.annotate(f"PUSAT ({xc:.1f}, {yc:.1f})", xy=(xc, yc), xytext=(5, 5),
                textcoords="offset points", color='#FFFF00' if is_dark else '#D97706', fontsize=8.5, fontweight='bold')

    # --- PENANDA TITIK AWAL & AKHIR ---
    ax.scatter(x1[0], y1[0], color='#00FF00' if is_dark else '#16A34A', marker='s', s=80, zorder=6, label='Titik Awal')
    ax.annotate(f"► START ({x1[0]:.1f}, {y1[0]:.1f})", xy=(x1[0], y1[0]), 
                xytext=(x1[0] + max(a, 1) * 0.15, y1[0] + max(b, 1) * 0.15),
                color='#00FF00' if is_dark else '#16A34A', fontsize=8.5, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#00FF00' if is_dark else '#16A34A', lw=1.2))

    ax.scatter(x1[-1], y1[-1], color='#FF9900' if is_dark else '#EA580C', marker='x', s=90, zorder=7, label='Titik Akhir')
    ax.annotate(f"■ END ({x1[-1]:.1f}, {y1[-1]:.1f})", xy=(x1[-1], y1[-1]), 
                xytext=(x1[-1] + max(a, 1) * 0.15, y1[-1] - max(b, 1) * 0.15),
                color='#FF9900' if is_dark else '#EA580C', fontsize=8.5, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#FF9900' if is_dark else '#EA580C', lw=1.2))

    # Teks Koordinat Tipis
    step_lbl = max(1, len(x1) // 6)
    for i in range(1, len(x1) - 1, step_lbl):
        ax.annotate(f"({x1[i]:.1f}, {y1[i]:.1f})", (x1[i], y1[i]),
                    textcoords="offset points", xytext=(5, 5), fontsize=7, color='#888888')
        if x2 is not None and y2 is not None:
            ax.annotate(f"({x2[i]:.1f}, {y2[i]:.1f})", (x2[i], y2[i]),
                        textcoords="offset points", xytext=(5, 5), fontsize=7, color='#888888')

    # --- KOTAK INFO PANEL TUNGGAL ---
    bbox_style = dict(boxstyle="square,pad=0.7", fc=warna_box, ec=warna_kurva, lw=1.2, alpha=0.95)
    fig.text(0.73, 0.5, teks_panel, fontsize=9, color=warna_teks, family='monospace', bbox=bbox_style, va='center')

    # Konfigurasi Batas Grafik
    if tipe_kurva in ("ELIPS", "LINGKARAN"):
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(xc - a * 1.6, xc + a * 1.6)
        ax.set_ylim(yc - b * 1.6, yc + b * 1.6)
    else:
        all_x = x1 if x2 is None else np.concatenate([x1, x2])
        all_y = y1 if y2 is None else np.concatenate([y1, y2])
        ax.set_xlim(np.min(all_x) - 2, np.max(all_x) + 2)
        ax.set_ylim(np.min(all_y) - 2, np.max(all_y) + 2)

    # Style Background Grid
    ax.grid(True, linestyle='--', alpha=0.3, color=warna_grid)
    ax.tick_params(colors=warna_teks, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(warna_spine)
        spine.set_linewidth(1)

    ax.axvline(xc, color='gray', linestyle=':', linewidth=0.8, alpha=0.4, zorder=1)
    ax.axhline(yc, color='gray', linestyle=':', linewidth=0.8, alpha=0.4, zorder=1)
    ax.legend(loc='lower left', facecolor=warna_box, edgecolor='none', labelcolor=warna_teks, fontsize=8)
    
    st.pyplot(fig)
    plt.close(fig)

# =====================================================
# 4. SIDEBAR: KONTROL DAN PILIHAN
# =====================================================
col_side_title, col_side_btn = st.sidebar.columns([4, 1], vertical_alignment="center")
with col_side_title:
    st.markdown("<h2 style='margin-top:0px; margin-bottom:0px; padding-top:0px; padding-bottom:0px;'>🎛️ Panel Parameter</h2>", unsafe_allow_html=True)
with col_side_btn:
    current_theme = st.session_state.theme
    icon = "☀️" if current_theme == 'dark' else "🌙"
    if st.button(icon, key="theme_toggle_btn", use_container_width=False):
        st.session_state.theme = 'light' if current_theme == 'dark' else 'dark'
        st.rerun()

st.sidebar.markdown("---")

# Pilihan Jenis Kurva (Navigasi Utama)
curve_type = st.sidebar.selectbox(
    "Pilih Jenis Kurva:",
    ["Lingkaran", "Elips", "Parabola", "Hiperbola"]
)

st.sidebar.divider()
st.sidebar.markdown("### ✏️ Input Parameter")

# Penanganan Nilai Default & Input Form Sesuai V3
if curve_type == "Lingkaran":
    col_pos1, col_pos2 = st.sidebar.columns(2)
    xc = col_pos1.number_input("Pusat X (xc) [contoh: 0.0]", value=0.0, step=0.5)
    yc = col_pos2.number_input("Pusat Y (yc) [contoh: 0.0]", value=0.0, step=0.5)
    
    r = st.sidebar.number_input("Radius (r) [contoh: 5.0]", min_value=0.1, value=5.0, step=0.5)
    
    col_step1, col_step2 = st.sidebar.columns(2)
    step_besar = col_step1.number_input("Step Besar θ [contoh: 0.5]", value=0.5, min_value=0.01, max_value=2.0, step=0.05)
    step_kecil = col_step2.number_input("Step Kecil θ [contoh: 0.05]", value=0.05, min_value=0.001, max_value=0.5, step=0.005)

elif curve_type == "Elips":
    col_pos1, col_pos2 = st.sidebar.columns(2)
    xc = col_pos1.number_input("Pusat X (xc) [contoh: 0.0]", value=0.0, step=0.5)
    yc = col_pos2.number_input("Pusat Y (yc) [contoh: 0.0]", value=0.0, step=0.5)
    
    col_spec1, col_spec2 = st.sidebar.columns(2)
    a = col_spec1.number_input("Sumbu Hor (a) [contoh: 8.0]", min_value=0.1, value=8.0, step=0.5)
    b = col_spec2.number_input("Sumbu Ver (b) [contoh: 5.0]", min_value=0.1, value=5.0, step=0.5)
    
    col_step1, col_step2 = st.sidebar.columns(2)
    step_besar = col_step1.number_input("Step Besar θ [contoh: 0.5]", value=0.5, min_value=0.01, max_value=2.0, step=0.05)
    step_kecil = col_step2.number_input("Step Kecil θ [contoh: 0.05]", value=0.05, min_value=0.001, max_value=0.5, step=0.005)

elif curve_type == "Parabola":
    orientasi_input = st.sidebar.selectbox(
        "Tentukan Orientasi [H/V]:",
        ["Horizontal (Membuka Kiri/Kanan)", "Vertikal (Membuka Atas/Bawah)"]
    )
    orientasi = 'H' if "Horizontal" in orientasi_input else 'V'
    
    col_pos1, col_pos2 = st.sidebar.columns(2)
    xp = col_pos1.number_input("Vertex X (xp) [contoh: 0.0]", value=0.0, step=0.5)
    yp = col_pos2.number_input("Vertex Y (yp) [contoh: 0.0]", value=0.0, step=0.5)
    
    a = st.sidebar.number_input("Faktor Ketajaman a [contoh: 1.0]", value=1.0, step=0.1)
    
    col_step1, col_step2 = st.sidebar.columns(2)
    step_besar = col_step1.number_input("Step Besar parameter t", value=1.0, min_value=0.05, max_value=5.0, step=0.05)
    step_kecil = col_step2.number_input("Step Kecil parameter t", value=0.1, min_value=0.005, max_value=1.0, step=0.005)

elif curve_type == "Hiperbola":
    col_pos1, col_pos2 = st.sidebar.columns(2)
    xc = col_pos1.number_input("Pusat X (xc) [contoh: 0.0]", value=0.0, step=0.5)
    yc = col_pos2.number_input("Pusat Y (yc) [contoh: 0.0]", value=0.0, step=0.5)
    
    col_spec1, col_spec2 = st.sidebar.columns(2)
    a = col_spec1.number_input("Transversal a [contoh: 4.0]", min_value=0.1, value=4.0, step=0.5)
    b = col_spec2.number_input("Konjugasi b [contoh: 3.0]", min_value=0.1, value=3.0, step=0.5)
    
    col_step1, col_step2 = st.sidebar.columns(2)
    step_besar = col_step1.number_input("Step Besar θ [contoh: 0.2]", value=0.2, min_value=0.01, max_value=1.0, step=0.01)
    step_kecil = col_step2.number_input("Step Kecil θ [contoh: 0.02]", value=0.02, min_value=0.001, max_value=0.2, step=0.002)

# =====================================================
# 5. KONTEN UTAMA & HEADER
# =====================================================
st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'><span class='title-gradient'>Visualisator Kurva Parametrik V3</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: gray; margin-bottom: 30px;'>Aplikasi Pembangkit Geometri Konik Parametrik Menggunakan Visualisasi Dashboard Clean.</p>", unsafe_allow_html=True)

# Tiga Tab Utama
tab_low, tab_high, tab_theory = st.tabs(["📉 Resolusi Rendah (Low)", "📈 Resolusi Tinggi (High)", "📖 Penjelasan Teori"])

# =====================================================
# 6. LOGIKA DAN PERHITUNGAN MATEMATIKA SESUAI V3
# =====================================================
if curve_type == "Lingkaran":
    keliling = 2 * np.pi * r
    luas = np.pi * r**2
    configs = [
        ("Resolusi Rendah", step_besar, tab_low),
        ("Resolusi Tinggi", step_kecil, tab_high)
    ]
    
    for title, step_val, tab_obj in configs:
        theta = np.append(np.arange(0, 2 * np.pi, step_val), 2 * np.pi)
        n_pts = len(theta)
        actual_step = 2 * np.pi / (n_pts - 1) if n_pts > 1 else 0
        x = xc + r * np.cos(theta)
        y = yc + r * np.sin(theta)
        
        teks_panel = (
            f" ⚙ DATA SPESIFIKASI LINGKARAN\n"
            f" ════════════════════════════\n"
            f" Pusat (xc,yc): ({xc:.2f}, {yc:.2f})\n"
            f" Radius (r)   : {r}\n"
            f" Luas Area    : {luas:.4f}\n"
            f" Keliling     : {keliling:.4f}\n"
            f" Total Titik  : {n_pts}\n"
            f" Skema        : {title}\n"
            f" ════════════════════════════\n"
            f" PERSAMAAN MATEMATIKA:\n"
            f" (x-{xc})² + (y-{yc})² = {r}²"
        )
        
        with tab_obj:
            # 1. Gambar Grafik (Plot) tampil penuh
            st.markdown(f"### 📊 Dashboard Plot - {title}")
            tampilkan_gaya_pro(theta, x, y, xc, yc, r, r, title, n_pts, actual_step, teks_panel, "LINGKARAN")
            
            st.divider()
            
            # 2. Teks Metadata & Substitusi Rumus di bawah gambar
            st.markdown(f"### 📋 Metadata & Substitusi")
            st.markdown("**Persamaan Parametrik (Rumus Asli):**")
            st.code(f"x(θ) = xc + r * cos(θ)\ny(θ) = yc + r * sin(θ)")
            st.markdown("**Persamaan Parametrik (Substitusi):**")
            st.code(f"x(θ) = {xc} + {r} * cos(θ)\ny(θ) = {yc} + {r} * sin(θ)")
            
            st.divider()
            
            # 3. Tabel Koordinat Hasil Perhitungan di paling bawah
            st.markdown("### 📋 Tabel Koordinat Hasil Perhitungan")
            
            # Pembuatan data table
            idx = np.arange(1, n_pts + 1)
            formula_x_list = [f"X = {xc} + {r}*cos({t:.2f})" for t in theta]
            formula_y_list = [f"Y = {yc} + {r}*sin({t:.2f})" for t in theta]
            
            df_coords = pd.DataFrame({
                'IDX': idx,
                'SUDUT (rad)': theta,
                'FORMULA SUMBU X': formula_x_list,
                'HASIL X': x,
                'FORMULA SUMBU Y': formula_y_list,
                'HASIL Y': y
            }).set_index('IDX')
            
            st.dataframe(df_coords.style.format({
                'SUDUT (rad)': '{:.2f}',
                'HASIL X': '{:.4f}',
                'HASIL Y': '{:.4f}'
            }), use_container_width=True, height=350)

elif curve_type == "Elips":
    c = np.sqrt(abs(a**2 - b**2))
    e = c / max(a, b)
    luas = np.pi * a * b
    keliling = np.pi * (3*(a+b) - np.sqrt((3*a+b)*(a+3*b))) # Ramanujan approx
    configs = [
        ("Resolusi Rendah", step_besar, tab_low),
        ("Resolusi Tinggi", step_kecil, tab_high)
    ]
    
    for title, step_val, tab_obj in configs:
        theta = np.append(np.arange(0, 2 * np.pi, step_val), 2 * np.pi)
        n_pts = len(theta)
        actual_step = 2 * np.pi / (n_pts - 1) if n_pts > 1 else 0
        x = xc + a * np.cos(theta)
        y = yc + b * np.sin(theta)
        
        teks_panel = (
            f" ⚙ DATA SPESIFIKASI ELIPS\n"
            f" ════════════════════════════\n"
            f" Pusat (xc,yc): ({xc:.2f}, {yc:.2f})\n"
            f" Sumbu hor (a): {a}\n"
            f" Sumbu ver (b): {b}\n"
            f" Jarak Fokus c: {c:.4f}\n"
            f" Eksentrisitas: {e:.4f}\n"
            f" Luas Area    : {luas:.4f}\n"
            f" Keliling     : {keliling:.4f}\n"
            f" Total Titik  : {n_pts}\n"
            f" Skema        : {title}\n"
            f" ════════════════════════════\n"
            f" PERSAMAAN MATEMATIKA:\n"
            f" (x-{xc})²/{a}² + (y-{yc})²/{b}² = 1"
        )
        
        with tab_obj:
            # 1. Gambar Grafik (Plot) tampil penuh
            st.markdown(f"### 📊 Dashboard Plot - {title}")
            tampilkan_gaya_pro(theta, x, y, xc, yc, a, b, title, n_pts, actual_step, teks_panel, "ELIPS")
            
            st.divider()
            
            # 2. Teks Metadata & Substitusi Rumus di bawah gambar
            st.markdown(f"### 📋 Metadata & Substitusi")
            st.markdown("**Persamaan Parametrik (Rumus Asli):**")
            st.code(f"x(θ) = xc + a * cos(θ)\ny(θ) = yc + b * sin(θ)")
            st.markdown("**Persamaan Parametrik (Substitusi):**")
            st.code(f"x(θ) = {xc} + {a} * cos(θ)\ny(θ) = {yc} + {b} * sin(θ)")
            
            st.divider()
            
            # 3. Tabel Koordinat Hasil Perhitungan di paling bawah
            st.markdown("### 📋 Tabel Koordinat Hasil Perhitungan")
            
            # Pembuatan data table
            idx = np.arange(1, n_pts + 1)
            formula_x_list = [f"X = {xc} + {a}*cos({t:.2f})" for t in theta]
            formula_y_list = [f"Y = {yc} + {b}*sin({t:.2f})" for t in theta]
            
            df_coords = pd.DataFrame({
                'IDX': idx,
                'SUDUT (rad)': theta,
                'FORMULA SUMBU X': formula_x_list,
                'HASIL X': x,
                'FORMULA SUMBU Y': formula_y_list,
                'HASIL Y': y
            }).set_index('IDX')
            
            st.dataframe(df_coords.style.format({
                'SUDUT (rad)': '{:.2f}',
                'HASIL X': '{:.4f}',
                'HASIL Y': '{:.4f}'
            }), use_container_width=True, height=350)

elif curve_type == "Parabola":
    configs = [
        ("Resolusi Rendah", step_besar, tab_low),
        ("Resolusi Tinggi", step_kecil, tab_high)
    ]
    
    for title, step_val, tab_obj in configs:
        t = np.arange(-5, 5 + step_val, step_val)
        n_pts = len(t)
        
        if orientasi == 'H':
            x = xp + a * t**2
            y = yp + t
            rumus_std = f"(y-{yp})² = {1/a:.4f} * (x-{xp})" if a != 0 else f"y = {yp}"
        else:
            x = xp + t
            y = yp + a * t**2
            rumus_std = f"(x-{xp})² = {1/a:.4f} * (y-{yp})" if a != 0 else f"x = {xp}"
            
        fokus_dist = 1 / (4 * a) if a != 0 else 0
        arah = "Horizontal" if orientasi == 'H' else "Vertikal"
        
        teks_panel = (
            f" ⚙ DATA SPESIFIKASI PARABOLA\n"
            f" ════════════════════════════\n"
            f" Vertex (xp,yp): ({xp:.2f}, {yp:.2f})\n"
            f" Orientasi     : {arah}\n"
            f" Parameter a   : {a}\n"
            f" Dist. Fokus   : {fokus_dist:.4f}\n"
            f" Total Titik   : {n_pts}\n"
            f" Skema         : {title}\n"
            f" ════════════════════════════\n"
            f" PERSAMAAN MATEMATIKA:\n"
            f" {rumus_std}"
        )
        
        with tab_obj:
            # 1. Gambar Grafik (Plot) tampil penuh
            st.markdown(f"### 📊 Dashboard Plot - {title}")
            tampilkan_gaya_pro(t, x, y, xp, yp, a, a, title, n_pts, step_val, teks_panel, "PARABOLA")
            
            st.divider()
            
            # 2. Teks Metadata & Substitusi Rumus di bawah gambar
            st.markdown(f"### 📋 Metadata & Substitusi")
            st.markdown("**Persamaan Parametrik (Rumus Asli):**")
            if orientasi == 'H':
                st.code(f"x(t) = xp + a * t²\ny(t) = yp + t")
            else:
                st.code(f"x(t) = xp + t\ny(t) = yp + a * t²")
                
            st.markdown("**Persamaan Parametrik (Substitusi):**")
            if orientasi == 'H':
                st.code(f"x(t) = {xp} + {a} * t²\ny(t) = {yp} + t")
            else:
                st.code(f"x(t) = {xp} + t\ny(t) = {yp} + {a} * t²")
            
            st.divider()
            
            # 3. Tabel Koordinat Hasil Perhitungan di paling bawah
            st.markdown("### 📋 Tabel Koordinat Hasil Perhitungan")
            
            # Pembuatan data table
            idx = np.arange(1, n_pts + 1)
            formula_x_list = [f"X = {xp} + {a}*({val:.2f})²" if orientasi == 'H' else f"X = {xp} + {val:.2f}" for val in t]
            formula_y_list = [f"Y = {yp} + {val:.2f}" if orientasi == 'H' else f"Y = {yp} + {a}*({val:.2f})²" for val in t]
            
            df_coords = pd.DataFrame({
                'IDX': idx,
                'NILAI t': t,
                'FORMULA SUMBU X': formula_x_list,
                'HASIL X': x,
                'FORMULA SUMBU Y': formula_y_list,
                'HASIL Y': y
            }).set_index('IDX')
            
            st.dataframe(df_coords.style.format({
                'NILAI t': '{:.2f}',
                'HASIL X': '{:.4f}',
                'HASIL Y': '{:.4f}'
            }), use_container_width=True, height=350)

elif curve_type == "Hiperbola":
    batas = 1.25
    c = np.sqrt(a**2 + b**2)
    e = c / a
    configs = [
        ("Resolusi Rendah", step_besar, tab_low),
        ("Resolusi Tinggi", step_kecil, tab_high)
    ]
    
    for title, step_val, tab_obj in configs:
        theta = np.arange(-batas, batas + step_val, step_val)
        n_pts = len(theta)
        x1 = xc + a / np.cos(theta); y1 = yc + b * np.tan(theta)
        x2 = xc - a / np.cos(theta); y2 = yc + b * np.tan(theta)
        
        teks_panel = (
            f" ⚙ DATA SPESIFIKASI HIPERBOLA\n"
            f" ════════════════════════════\n"
            f" Pusat (xc,yc): ({xc:.2f}, {yc:.2f})\n"
            f" Transversal a: {a}\n"
            f" Konjugasi b  : {b}\n"
            f" Jarak Fokus c: {c:.4f}\n"
            f" Eksentrisitas: {e:.4f}\n"
            f" Total Titik  : {n_pts} per cb\n"
            f" Skema         : {title}\n"
            f" ════════════════════════════\n"
            f" PERSAMAAN MATEMATIKA:\n"
            f" (x-{xc})²/{a}² - (y-{yc})²/{b}² = 1"
        )
        
        with tab_obj:
            # 1. Gambar Grafik (Plot) tampil penuh
            st.markdown(f"### 📊 Dashboard Plot - {title}")
            tampilkan_gaya_pro(theta, x1, y1, xc, yc, a, b, title, n_pts, step_val, teks_panel, "HIPERBOLA", x2, y2)
            
            st.divider()
            
            # 2. Teks Metadata & Substitusi Rumus di bawah gambar
            st.markdown(f"### 📋 Metadata & Substitusi")
            st.markdown("**Persamaan Parametrik (Rumus Asli):**")
            st.code(f"x(θ) = xc + a / cos(θ)\ny(θ) = yc + b * tan(θ)")
            st.markdown("**Persamaan Parametrik (Substitusi - Cabang Kanan):**")
            st.code(f"x(θ) = {xc} + {a} / cos(θ)\ny(θ) = {yc} + {b} * tan(θ)")
            
            st.divider()
            
            # 3. Tabel Koordinat Hasil Perhitungan (Cabang Kanan) di paling bawah
            st.markdown("### 📋 Tabel Koordinat Hasil Perhitungan (Cabang Kanan)")
            
            # Pembuatan data table (Cabang Kanan)
            idx = np.arange(1, n_pts + 1)
            formula_x_list = [f"X = {xc} + {a}/cos({t:.2f})" for t in theta]
            formula_y_list = [f"Y = {yc} + {b}*tan({t:.2f})" for t in theta]
            
            df_coords = pd.DataFrame({
                'IDX': idx,
                'SUDUT (rad)': theta,
                'FORMULA CABANG KANAN X': formula_x_list,
                'HASIL X': x1,
                'FORMULA CABANG KANAN Y': formula_y_list,
                'HASIL Y': y1
            }).set_index('IDX')
            
            st.dataframe(df_coords.style.format({
                'SUDUT (rad)': '{:.2f}',
                'HASIL X': '{:.4f}',
                'HASIL Y': '{:.4f}'
            }), use_container_width=True, height=350)

# =====================================================
# 7. TAB PENJELASAN TEORI
# =====================================================
with tab_theory:
    with st.container(border=True):
        if curve_type == "Lingkaran":
            st.markdown(r"""
            ### 🔴 Teori Lingkaran
            
            **Lingkaran** merupakan salah satu kurva konik yang paling dasar. Kurva ini didefinisikan sebagai himpunan semua titik pada bidang dua dimensi yang memiliki jarak konstan (disebut sebagai **radius** atau jari-jari, $r$) dari sebuah titik tertentu yang disebut **titik pusat** $(x_c, y_c)$.
            
            #### Persamaan Parametrik
            Persamaan parametrik dari lingkaran dengan radius $r$ dan titik pusat $(x_c, y_c)$ didefinisikan sebagai:
            """)
            
            st.latex(r"x(\theta) = x_c + r \cdot \cos(\theta)")
            st.latex(r"y(\theta) = y_c + r \cdot \sin(\theta)")
            
            st.markdown(r"""
            di mana parameter $\theta$ merupakan sudut dalam radian yang berada pada rentang:
            """)
            st.latex(r"\theta \in [0, 2\pi]")
            
        elif curve_type == "Elips":
            st.markdown(r"""
            ### 🟢 Teori Elips
            
            **Elips** adalah bentuk kurva tertutup hasil irisan kerucut yang meluas secara simetris terhadap dua sumbu yang saling tegak lurus. Secara geometris, elips didefinisikan sebagai tempat kedudukan titik-titik yang jumlah jaraknya dari dua titik fokus (foci) adalah konstan. 
            
            Elips memiliki dua parameter utama:
            - $a$ : Setengah panjang sumbu mayor (arah horizontal jika mendatar).
            - $b$ : Setengah panjang sumbu minor (arah vertikal jika tegak).
            
            #### Persamaan Parametrik
            Persamaan parametrik elips berpusat di $(x_c, y_c)$ dengan semi-mayor $a$ dan semi-minor $b$ didefinisikan sebagai:
            """)
            
            st.latex(r"x(\theta) = x_c + a \cdot \cos(\theta)")
            st.latex(r"y(\theta) = y_c + b \cdot \sin(\theta)")
            
            st.markdown(r"""
            di mana parameter sudut $\theta$ berada pada rentang:
            """)
            st.latex(r"\theta \in [0, 2\pi]")
            st.markdown(r"""
            > **Catatan**: Jika nilai $a = b = r$, maka persamaan ini akan berubah menjadi persamaan lingkaran dengan radius $r$.
            """)
      
        elif curve_type == "Parabola":
            st.markdown(r"""
            ### 🟡 Teori Parabola
            
            **Parabola** adalah kurva terbuka dua dimensi yang dibentuk oleh sekumpulan titik yang jaraknya ke titik tertentu (fokus) sama dengan jaraknya ke garis lurus tertentu (direktriks). Titik balik terdekat dengan direktriks dan fokus disebut sebagai **puncak** atau **vertex** $(x_p, y_p)$.
            
            Persamaan parametrik parabola tergantung pada orientasi bukaan kurva:
            
            #### 1. Parabola Horizontal (Membuka ke Kiri / Kanan)
            Parabola mendatar memiliki persamaan parametrik dengan parameter bebas $t$:
            """)
            
            st.latex(r"x(t) = x_p + a \cdot t^2")
            st.latex(r"y(t) = y_p + t")
            
            st.markdown(r"""
            #### 2. Parabola Vertikal (Membuka ke Atas / Bawah)
            Parabola tegak memiliki persamaan parametrik dengan parameter bebas $t$:
            """)
            
            st.latex(r"x(t) = x_p + t")
            st.latex(r"y(t) = y_p + a \cdot t^2")
            
            st.markdown(r"""
            di mana:
            - $t$ adalah parameter riil yang mewakili sumbu penjelajah (pada visualisasi dibatasi $t \in [-5, 5]$).
            - $a$ adalah koefisien fokus/lebar parabola. Jika $a > 0$, parabola membuka ke arah positif (kanan atau atas). Jika $a < 0$, parabola membuka ke arah sebaliknya (kiri atau bawah).
            """)
      
        elif curve_type == "Hiperbola":
            st.markdown(r"""
            ### 🔵 Teori Hiperbola
            
            **Hiperbola** adalah kurva terbuka yang memiliki dua cabang simetris (terpisah). Secara geometri, hiperbola didefinisikan sebagai himpunan semua titik pada bidang yang selisih jaraknya ke dua titik fokus tetap konstan.
            
            Hiperbola horizontal memiliki titik pusat $(x_c, y_c)$, setengah sumbu transversal $a$, dan setengah sumbu konjugasi $b$.
            
            #### Persamaan Parametrik
            Persamaan koordinat $x$ memiliki cabang kanan dan cabang kiri, sedangkan koordinat $y$ bernilai sama untuk kedua cabang:
            """)
            
            st.markdown("**Cabang Kanan (Membuka ke Kanan):**")
            st.latex(r"x(\theta) = x_c + a \cdot \sec(\theta) = x_c + \frac{a}{\cos(\theta)}")
            
            st.markdown("**Cabang Kiri (Membuka ke Liri):**")
            st.latex(r"x(\theta) = x_c - a \cdot \sec(\theta) = x_c - \frac{a}{\cos(\theta)}")
            
            st.markdown("**Persamaan Koordinat Y (Kedua Cabang):**")
            st.latex(r"y(\theta) = y_c + b \cdot \tan(\theta)")
            
            st.markdown(r"""
            di mana parameter sudut $\theta$ berada pada rentang:
            """)
            st.latex(r"\theta \in \left(-\frac{\pi}{2}, \frac{\pi}{2}\right)")
            st.markdown(r"""
            > **Penting**: Karena nilai $\cos(\theta) \to 0$ saat $\theta \to \pm\frac{\pi}{2}$, koordinat $x$ akan menuju tak hingga ($\pm\infty$) dan kurva menjadi terputus. Dalam aplikasi ini, kita membatasi parameter sudut $\theta \in [-1.25, 1.25]$ radian untuk keamanan komputasi dan kenyamanan visual.
            """)
