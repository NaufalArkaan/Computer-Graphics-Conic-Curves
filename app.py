import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# =====================================================
# 1. KONFIGURASI HALAMAN & STATE
# =====================================================
st.set_page_config(
    page_title="Pembangkit Kurva Parametrik",
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
            --accent-color: #3b82f6;
            --accent-hover: #1d4ed8;
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
            font-weight: 700 !important;
        }
        
        .title-gradient {
            background: linear-gradient(90deg, #60a5fa, #3b82f6);
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
        
        /* Smooth animations for state change */
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
            --accent-color: #007bff;
            --accent-hover: #0056b3;
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
            font-weight: 700 !important;
        }
        
        .title-gradient {
            background: linear-gradient(90deg, #007bff, #0056b3);
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
        
        * {
            transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css(st.session_state.theme)


# =====================================================
# 3. STRUKTUR DATA & LOGIKA KURVA (OOP)
# =====================================================
class ParametricCurve:
    @staticmethod
    def get_lingkaran(xc, yc, r, step_besar, step_kecil):
        theta_low = np.arange(0, 2 * np.pi, step_besar)
        theta_high = np.arange(0, 2 * np.pi, step_kecil)
        
        # Tambahkan endpoint agar kurva menutup sempurna di visualisasi tinggi
        if theta_high[-1] != 2 * np.pi:
            theta_high = np.append(theta_high, 2 * np.pi)
            
        x_low = xc + r * np.cos(theta_low)
        y_low = yc + r * np.sin(theta_low)
        x_high = xc + r * np.cos(theta_high)
        y_high = yc + r * np.sin(theta_high)
        
        rumus_text = f"x = {xc} + {r}·cos(θ)\ny = {yc} + {r}·sin(θ)"
        
        return {
            'x_low': x_low, 'y_low': y_low,
            'x_high': x_high, 'y_high': y_high,
            'center_x': xc, 'center_y': yc,
            'theta_low': theta_low,
            'theta_high': theta_high,
            'rumus_text': rumus_text
        }

    @staticmethod
    def get_elips(xc, yc, a, b, step_besar, step_kecil):
        theta_low = np.arange(0, 2 * np.pi, step_besar)
        theta_high = np.arange(0, 2 * np.pi, step_kecil)
        
        if theta_high[-1] != 2 * np.pi:
            theta_high = np.append(theta_high, 2 * np.pi)
            
        x_low = xc + a * np.cos(theta_low)
        y_low = yc + b * np.sin(theta_low)
        x_high = xc + a * np.cos(theta_high)
        y_high = yc + b * np.sin(theta_high)
        
        rumus_text = f"x = {xc} + {a}·cos(θ)\ny = {yc} + {b}·sin(θ)"
        
        return {
            'x_low': x_low, 'y_low': y_low,
            'x_high': x_high, 'y_high': y_high,
            'center_x': xc, 'center_y': yc,
            'theta_low': theta_low,
            'theta_high': theta_high,
            'rumus_text': rumus_text
        }

    @staticmethod
    def get_parabola(xp, yp, a, orientasi, step_besar, step_kecil):
        t_low = np.arange(-10, 10 + step_besar, step_besar)
        t_high = np.arange(-10, 10 + step_kecil, step_kecil)
        
        if orientasi == 'H':
            x_low = xp + a * t_low**2
            y_low = yp + t_low
            x_high = xp + a * t_high**2
            y_high = yp + t_high
            rumus_text = f"x = {xp} + {a}·t²\ny = {yp} + t"
        else:
            x_low = xp + t_low
            y_low = yp + a * t_low**2
            x_high = xp + t_high
            y_high = yp + a * t_high**2
            rumus_text = f"x = {xp} + t\ny = {yp} + {a}·t²"
            
        return {
            'x_low': x_low, 'y_low': y_low,
            'x_high': x_high, 'y_high': y_high,
            'center_x': xp, 'center_y': yp,
            't_low': t_low,
            't_high': t_high,
            'rumus_text': rumus_text
        }

    @staticmethod
    def get_hiperbola(xc, yc, a, b, step_besar, step_kecil):
        # Batas θ aman agar sec(θ) tidak mendekati tak-terhingga
        batas = 1.30
        
        theta_low = np.linspace(-batas, batas, max(3, int(2 * batas / step_besar)))
        theta_high = np.linspace(-batas, batas, max(3, int(2 * batas / step_kecil)))
        
        # Cabang kanan
        x1_low = xc + a / np.cos(theta_low)
        y1_low = yc + b * np.tan(theta_low)
        x1_high = xc + a / np.cos(theta_high)
        y1_high = yc + b * np.tan(theta_high)
        
        # Cabang kiri
        x2_low = xc - a / np.cos(theta_low)
        y2_low = yc + b * np.tan(theta_low)
        x2_high = xc - a / np.cos(theta_high)
        y2_high = yc + b * np.tan(theta_high)
        
        rumus_text = (
            f"Cabang Kanan: x = {xc} + {a}·sec(θ)\n"
            f"Cabang Kiri : x = {xc} - {a}·sec(θ)\n"
            f"              y = {yc} + {b}·tan(θ)"
        )
        
        return {
            'x1_low': x1_low, 'y1_low': y1_low,
            'x2_low': x2_low, 'y2_low': y2_low,
            'x1_high': x1_high, 'y1_high': y1_high,
            'x2_high': x2_high, 'y2_high': y2_high,
            'xc': xc, 'yc': yc,
            'theta_low': theta_low,
            'theta_high': theta_high,
            'rumus_text': rumus_text
        }


# =====================================================
# 4. DRAW PLOT DENGAN TEMA MATPLOTLIB DINAMIS
# =====================================================
def draw_plot(curve_type, data, is_dark_mode):
    if is_dark_mode:
        plt.style.use('dark_background')
        text_color = '#f8f9fa'
        grid_color = '#374151'
        low_res_color = '#60a5fa'       # Biru neon lembut
        high_res_color = '#facc15'      # Kuning terang
        center_color = '#ef4444'        # Merah
        high_center_color = '#4ade80'   # Lime green
        bbox_face = '#1e293b'
        bbox_edge = '#3b82f6'
    else:
        plt.style.use('default')
        text_color = '#333333'
        grid_color = '#d1d5db'
        low_res_color = '#1d4ed8'       # Biru tua elegan
        high_res_color = '#d97706'      # Amber/Oranye gelap
        center_color = '#dc2626'        # Merah tua
        high_center_color = '#16a34a'   # Hijau tua
        bbox_face = '#ffffff'
        bbox_edge = '#007bff'

    # Konfigurasi parameter global agar menyatu dengan UI
    plt.rcParams.update({
        'figure.facecolor': 'none',
        'axes.facecolor': 'none',
        'axes.edgecolor': grid_color,
        'axes.labelcolor': text_color,
        'xtick.color': text_color,
        'ytick.color': text_color,
        'grid.color': grid_color,
        'grid.alpha': 0.5,
        'text.color': text_color,
        'legend.facecolor': 'none',
        'legend.edgecolor': grid_color
    })

    fig, ax = plt.subplots(1, 2, figsize=(15, 6.5))

    if curve_type == "Hiperbola":
        # ----------------- PANEL KIRI (LOW RES) -----------------
        ax[0].plot(data['x1_low'], data['y1_low'], 'o-', color=low_res_color, linewidth=2, markersize=6, label='Cabang Kanan')
        ax[0].plot(data['x2_low'], data['y2_low'], 'o-', color='#ec4899' if is_dark_mode else '#db2777', linewidth=2, markersize=6, label='Cabang Kiri')
        
        # Anotasi low-res koordinat
        x1_low, y1_low = data['x1_low'], data['y1_low']
        x2_low, y2_low = data['x2_low'], data['y2_low']
        step_anno = max(1, len(x1_low) // 6)
        
        for i in range(0, len(x1_low), step_anno):
            # Annotate cabang kanan
            ax[0].annotate(
                f"({x1_low[i]:.1f}, {y1_low[i]:.1f})",
                (x1_low[i], y1_low[i]),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=7.5,
                color=text_color
            )
            # Annotate cabang kiri
            ax[0].annotate(
                f"({x2_low[i]:.1f}, {y2_low[i]:.1f})",
                (x2_low[i], y2_low[i]),
                textcoords="offset points",
                xytext=(-15, 5),
                fontsize=7.5,
                color=text_color
            )

        ax[0].scatter(data['xc'], data['yc'], color=center_color, s=150, zorder=5, label='Pusat')
        ax[0].axhline(0, color=text_color, linewidth=0.8, alpha=0.5)
        ax[0].axvline(0, color=text_color, linewidth=0.8, alpha=0.5)
        ax[0].grid(True, linestyle='--', alpha=0.4)
        ax[0].set_xlabel("X")
        ax[0].set_ylabel("Y")
        ax[0].set_title(f"Resolusi Rendah  |  Titik = {len(x1_low) * 2}", fontsize=12, color=text_color)
        ax[0].legend()
        ax[0].axis('equal')

        # ----------------- PANEL KANAN (HIGH RES) -----------------
        ax[1].plot(data['x1_high'], data['y1_high'], color=high_res_color, linewidth=2, label='Cabang Kanan')
        ax[1].plot(data['x2_high'], data['y2_high'], color='#f59e0b' if is_dark_mode else '#c2410c', linewidth=2, label='Cabang Kiri')
        ax[1].scatter(data['x1_high'], data['y1_high'], color=center_color, s=20, zorder=3)
        ax[1].scatter(data['x2_high'], data['y2_high'], color=center_color, s=20, zorder=3)
        ax[1].scatter(data['xc'], data['yc'], color=high_center_color, s=150, zorder=5, label='Pusat')
        ax[1].axhline(0, color=text_color, linewidth=0.8, alpha=0.5)
        ax[1].axvline(0, color=text_color, linewidth=0.8, alpha=0.5)
        ax[1].grid(True, linestyle='--', alpha=0.4)
        ax[1].set_xlabel("X")
        ax[1].set_ylabel("Y")
        ax[1].set_title(f"Resolusi Tinggi  |  Titik = {len(data['x1_high']) * 2}", fontsize=12, color=text_color)
        ax[1].legend()
        ax[1].axis('equal')

    else:
        x_low, y_low = data['x_low'], data['y_low']
        x_high, y_high = data['x_high'], data['y_high']
        center_x, center_y = data['center_x'], data['center_y']
        
        # ----------------- PANEL KIRI (LOW RES) -----------------
        ax[0].plot(x_low, y_low, 'o-', color=low_res_color, linewidth=2, markersize=8, label='Kurva')
        
        # Anotasi titik koordinat
        step_anno = max(1, len(x_low) // 8)
        for i in range(0, len(x_low), step_anno):
            ax[0].annotate(
                f"({x_low[i]:.1f}, {y_low[i]:.1f})",
                (x_low[i], y_low[i]),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=7.5,
                color=text_color
            )

        ax[0].scatter(center_x, center_y, color=center_color, s=150, zorder=5, label='Pusat / Vertex')
        ax[0].axhline(0, color=text_color, linewidth=0.8, alpha=0.5)
        ax[0].axvline(0, color=text_color, linewidth=0.8, alpha=0.5)
        ax[0].grid(True, linestyle='--', alpha=0.4)
        ax[0].set_xlabel("X")
        ax[0].set_ylabel("Y")
        ax[0].set_title(f"Resolusi Rendah  |  Titik = {len(x_low)}", fontsize=12, color=text_color)
        ax[0].legend()
        ax[0].axis('equal')

        # ----------------- PANEL KANAN (HIGH RES) -----------------
        ax[1].plot(x_high, y_high, color=high_res_color, linewidth=2, label='Kurva')
        ax[1].scatter(x_high, y_high, color=center_color, s=25, zorder=3)
        ax[1].scatter(center_x, center_y, color=high_center_color, s=150, zorder=5, label='Pusat / Vertex')
        ax[1].axhline(0, color=text_color, linewidth=0.8, alpha=0.5)
        ax[1].axvline(0, color=text_color, linewidth=0.8, alpha=0.5)
        ax[1].grid(True, linestyle='--', alpha=0.4)
        ax[1].set_xlabel("X")
        ax[1].set_ylabel("Y")
        ax[1].set_title(f"Resolusi Tinggi  |  Titik = {len(x_high)}", fontsize=12, color=text_color)
        ax[1].legend()
        ax[1].axis('equal')

    # Kotak Rumus Parametrik
    ax[1].text(
        0.03, 0.05, data['rumus_text'],
        transform=ax[1].transAxes,
        fontsize=9.5,
        color=text_color,
        bbox=dict(facecolor=bbox_face, edgecolor=bbox_edge, alpha=0.85, pad=6, boxstyle='round,pad=0.5')
    )

    plt.suptitle(f"VISUALISASI PARAMETRIK — {curve_type.upper()}", fontsize=16, fontweight='bold', color=text_color)
    plt.tight_layout()
    return fig


# =====================================================
# 5. SIDEBAR: KONTROL DAN TEMA
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

# Pilihan Jenis Kurva
curve_type = st.sidebar.selectbox(
    "Pilih Jenis Kurva:",
    ["Lingkaran", "Elips", "Parabola", "Hiperbola"]
)

st.sidebar.divider()

st.sidebar.markdown("### ✏️ Parameter Kurva")

# Dynamic parameter inputs
if curve_type == "Lingkaran":
    xc = st.sidebar.slider("Pusat X (xc)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
    yc = st.sidebar.slider("Pusat Y (yc)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
    r = st.sidebar.slider("Radius (r)", min_value=0.1, max_value=15.0, value=5.0, step=0.5)
    
    with st.sidebar.expander("⚙️ Pengaturan Resolusi (Lanjutan)"):
        col3, col4 = st.columns(2)
        step_besar = col3.number_input("Step Besar (Low)", value=0.5, min_value=0.05, max_value=2.0, step=0.05)
        step_kecil = col4.number_input("Step Kecil (High)", value=0.05, min_value=0.005, max_value=0.5, step=0.005)
    
    # Generate data
    curve_data = ParametricCurve.get_lingkaran(xc, yc, r, step_besar, step_kecil)

elif curve_type == "Elips":
    xc = st.sidebar.slider("Pusat X (xc)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
    yc = st.sidebar.slider("Pusat Y (yc)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
    a = st.sidebar.slider("Semi Mayor (a)", min_value=0.1, max_value=15.0, value=6.0, step=0.5)
    b = st.sidebar.slider("Semi Minor (b)", min_value=0.1, max_value=15.0, value=4.0, step=0.5)
    
    with st.sidebar.expander("⚙️ Pengaturan Resolusi (Lanjutan)"):
        col5, col6 = st.columns(2)
        step_besar = col5.number_input("Step Besar (Low)", value=0.5, min_value=0.05, max_value=2.0, step=0.05)
        step_kecil = col6.number_input("Step Kecil (High)", value=0.05, min_value=0.005, max_value=0.5, step=0.005)
    
    # Generate data
    curve_data = ParametricCurve.get_elips(xc, yc, a, b, step_besar, step_kecil)

elif curve_type == "Parabola":
    orientasi = st.sidebar.selectbox(
        "Orientasi Parabola:",
        ["Horizontal (Membuka Kiri/Kanan)", "Vertikal (Membuka Atas/Bawah)"]
    )
    orientasi_code = 'H' if "Horizontal" in orientasi else 'V'
    
    xp = st.sidebar.slider("Vertex X (xp)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
    yp = st.sidebar.slider("Vertex Y (yp)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
    a = st.sidebar.slider("Nilai Fokus/Koefisien (a)", min_value=-5.0, max_value=5.0, value=1.0, step=0.1)
    
    with st.sidebar.expander("⚙️ Pengaturan Resolusi (Lanjutan)"):
        col3, col4 = st.columns(2)
        step_besar = col3.number_input("Step Besar (Low)", value=0.5, min_value=0.05, max_value=5.0, step=0.05)
        step_kecil = col4.number_input("Step Kecil (High)", value=0.05, min_value=0.005, max_value=1.0, step=0.005)
    
    # Generate data
    curve_data = ParametricCurve.get_parabola(xp, yp, a, orientasi_code, step_besar, step_kecil)

elif curve_type == "Hiperbola":
    xc = st.sidebar.slider("Pusat X (xc)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
    yc = st.sidebar.slider("Pusat Y (yc)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5)
    a = st.sidebar.slider("Sumbu Transversal (a)", min_value=0.1, max_value=15.0, value=3.0, step=0.5)
    b = st.sidebar.slider("Sumbu Konjugasi (b)", min_value=0.1, max_value=15.0, value=2.0, step=0.5)
    
    with st.sidebar.expander("⚙️ Pengaturan Resolusi (Lanjutan)"):
        col5, col6 = st.columns(2)
        step_besar = col5.number_input("Step Besar (Low)", value=0.2, min_value=0.01, max_value=1.0, step=0.01)
        step_kecil = col6.number_input("Step Kecil (High)", value=0.02, min_value=0.001, max_value=0.2, step=0.002)
    
    # Generate data
    curve_data = ParametricCurve.get_hiperbola(xc, yc, a, b, step_besar, step_kecil)


# =====================================================
# 6. KONTEN UTAMA & NAVIGASI TAB
# =====================================================
st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'><span class='title-gradient'>Visualisator Kurva Parametrik</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; color: gray; margin-bottom: 30px;'>Eksplorasi interaktif pembentukan geometri (Lingkaran, Elips, Parabola, Hiperbola) melalui penyesuaian parameter matematika secara real-time.</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Visualisasi", "📖 Penjelasan Teori"])

with tab1:
    # Plot Matplotlib
    st.markdown("### 📈 Visualisasi Kurva")
    fig = draw_plot(curve_type, curve_data, st.session_state.theme == 'dark')
    
    # Tampilkan plot dalam kontainer ter-style
    with st.container(border=True):
        st.pyplot(fig)
    
    # Tampilkan tabel koordinat
    st.markdown("### 📋 Tabel Koordinat")
    
    # Buat Pandas DataFrame untuk data resolusi rendah dan tinggi
    if curve_type == "Hiperbola":
        # Resolusi Rendah
        df_coords_low = pd.DataFrame({
            'No': np.arange(1, len(curve_data['x1_low']) + 1),
            'θ (Radian)': curve_data['theta_low'],
            'X (Cabang Kanan)': curve_data['x1_low'],
            'Y (Cabang Kanan)': curve_data['y1_low'],
            'X (Cabang Kiri)': curve_data['x2_low'],
            'Y (Cabang Kiri)': curve_data['y2_low']
        }).set_index('No')
        
        styled_df_low = df_coords_low.style.format({
            'θ (Radian)': '{:.4f}',
            'X (Cabang Kanan)': '{:.4f}',
            'Y (Cabang Kanan)': '{:.4f}',
            'X (Cabang Kiri)': '{:.4f}',
            'Y (Cabang Kiri)': '{:.4f}'
        })
        
        # Resolusi Tinggi
        df_coords_high = pd.DataFrame({
            'No': np.arange(1, len(curve_data['x1_high']) + 1),
            'θ (Radian)': curve_data['theta_high'],
            'X (Cabang Kanan)': curve_data['x1_high'],
            'Y (Cabang Kanan)': curve_data['y1_high'],
            'X (Cabang Kiri)': curve_data['x2_high'],
            'Y (Cabang Kiri)': curve_data['y2_high']
        }).set_index('No')
        
        styled_df_high = df_coords_high.style.format({
            'θ (Radian)': '{:.4f}',
            'X (Cabang Kanan)': '{:.4f}',
            'Y (Cabang Kanan)': '{:.4f}',
            'X (Cabang Kiri)': '{:.4f}',
            'Y (Cabang Kiri)': '{:.4f}'
        })
        
    elif curve_type == "Parabola":
        # Resolusi Rendah
        df_coords_low = pd.DataFrame({
            'No': np.arange(1, len(curve_data['x_low']) + 1),
            't (Parameter)': curve_data['t_low'],
            'X': curve_data['x_low'],
            'Y': curve_data['y_low']
        }).set_index('No')
        
        styled_df_low = df_coords_low.style.format({
            't (Parameter)': '{:.4f}',
            'X': '{:.4f}',
            'Y': '{:.4f}'
        })
        
        # Resolusi Tinggi
        df_coords_high = pd.DataFrame({
            'No': np.arange(1, len(curve_data['x_high']) + 1),
            't (Parameter)': curve_data['t_high'],
            'X': curve_data['x_high'],
            'Y': curve_data['y_high']
        }).set_index('No')
        
        styled_df_high = df_coords_high.style.format({
            't (Parameter)': '{:.4f}',
            'X': '{:.4f}',
            'Y': '{:.4f}'
        })
        
    else: # Lingkaran dan Elips
        # Resolusi Rendah
        df_coords_low = pd.DataFrame({
            'No': np.arange(1, len(curve_data['x_low']) + 1),
            'θ (Radian)': curve_data['theta_low'],
            'X': curve_data['x_low'],
            'Y': curve_data['y_low']
        }).set_index('No')
        
        styled_df_low = df_coords_low.style.format({
            'θ (Radian)': '{:.4f}',
            'X': '{:.4f}',
            'Y': '{:.4f}'
        })
        
        # Resolusi Tinggi
        df_coords_high = pd.DataFrame({
            'No': np.arange(1, len(curve_data['x_high']) + 1),
            'θ (Radian)': curve_data['theta_high'],
            'X': curve_data['x_high'],
            'Y': curve_data['y_high']
        }).set_index('No')
        
        styled_df_high = df_coords_high.style.format({
            'θ (Radian)': '{:.4f}',
            'X': '{:.4f}',
            'Y': '{:.4f}'
        })
        
    # Render berdampingan menggunakan columns
    col_table_low, col_table_high = st.columns(2)
    with col_table_low:
        st.markdown("**Resolusi Rendah (Low Resolution)**")
        st.dataframe(styled_df_low, width="stretch", height=280)
        
    with col_table_high:
        st.markdown("**Resolusi Tinggi (High Resolution)**")
        st.dataframe(styled_df_high, width="stretch", height=280)

with tab2:
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
            st.latex(r"\theta \in [0, 2\pi)")
            
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
            st.latex(r"\theta \in [0, 2\pi)")
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
            - $t$ adalah parameter riil yang mewakili sumbu penjelajah (pada visualisasi dibatasi $t \in [-10, 10]$).
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
            
            st.markdown("**Cabang Kiri (Membuka ke Kiri):**")
            st.latex(r"x(\theta) = x_c - a \cdot \sec(\theta) = x_c - \frac{a}{\cos(\theta)}")
            
            st.markdown("**Persamaan Koordinat Y (Kedua Cabang):**")
            st.latex(r"y(\theta) = y_c + b \cdot \tan(\theta)")
            
            st.markdown(r"""
            di mana parameter sudut $\theta$ berada pada rentang:
            """)
            st.latex(r"\theta \in \left(-\frac{\pi}{2}, \frac{\pi}{2}\right)")
            st.markdown(r"""
            > **Penting**: Karena nilai $\cos(\theta) \to 0$ saat $\theta \to \pm\frac{\pi}{2}$, koordinat $x$ akan menuju tak hingga ($\pm\infty$) dan kurva menjadi terputus. Dalam aplikasi ini, kita membatasi parameter sudut $\theta \in [-1.30, 1.30]$ radian (sekitar $\pm74.5^\circ$) untuk keamanan komputasi dan kenyamanan visual.
            """)
