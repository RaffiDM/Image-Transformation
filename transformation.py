import cv2
import numpy as np
import streamlit as st
from PIL import Image

# Konfigurasi halaman
st.set_page_config(page_title="Image Transformation App", layout="wide")

# Judul aplikasi
st.title("IMAGE ROTATION AND SCALING VISUALIZER")
st.markdown("Rotate, Scale, dan Transform gambar dengan kontrol interaktif")

# Sidebar untuk upload dan kontrol
st.sidebar.header("⚙ Kontrol Transformasi")

# Upload gambar
uploaded_file = st.sidebar.file_uploader("Upload Gambar", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Baca gambar
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    h, w = image.shape[:2]
    
    st.sidebar.success(f"Ukuran gambar: {w} x {h} pixels")
    
    # Kontrol Rotation
    st.sidebar.subheader("🔄 Rotation")
    rotation_angle = st.sidebar.slider(
        "Sudut Rotasi (derajat)",
        min_value=0,
        max_value=360,
        value=0,
        step=1
    )
    
    # Kontrol Scaling
    st.sidebar.subheader("🔍 Scaling")
    scale_factor = st.sidebar.slider(
        "Faktor Skala",
        min_value=0.1,
        max_value=3.0,
        value=1.0,
        step=0.1
    )
    
    # Kontrol Translation
    st.sidebar.subheader("↔ Translation")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        tx = st.number_input("Shift X", min_value=-500, max_value=500, value=0, step=10)
    with col2:
        ty = st.number_input("Shift Y", min_value=-500, max_value=500, value=0, step=10)

    # Tombol reset
    if st.sidebar.button("🔄 Reset ke Default"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # -------------------------
    # Proses Transformasi
    # -------------------------
    
    # 1. Scaling
    if scale_factor != 1.0:
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)
        transformed = cv2.resize(image, (new_w, new_h))
    else:
        transformed = image.copy()
    
    h_trans, w_trans = transformed.shape[:2]
    
    # 2. Rotation
    if rotation_angle != 0:
        center = (w_trans // 2, h_trans // 2)
        M_rotate = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        cos = np.abs(M_rotate[0, 0])
        sin = np.abs(M_rotate[0, 1])
        new_w = int((h_trans * sin) + (w_trans * cos))
        new_h = int((h_trans * cos) + (w_trans * sin))
        M_rotate[0, 2] += (new_w / 2) - center[0]
        M_rotate[1, 2] += (new_h / 2) - center[1]
        transformed = cv2.warpAffine(
            transformed, M_rotate, (new_w, new_h),
            borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255)
        )
    
    # 3. Translation
    if tx != 0 or ty != 0:
        h_trans, w_trans = transformed.shape[:2]
        M_translate = np.float32([[1, 0, tx], [0, 1, ty]])
        transformed = cv2.warpAffine(
            transformed, M_translate, (w_trans, h_trans),
            borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255)
        )
    
    # -------------------------
    # Tampilan Output
    # -------------------------
    
    st.markdown("---")
    col_info1, col_info2, col_info3, col_info4 = st.columns(4)
    with col_info1:
        st.metric("Rotasi", f"{rotation_angle}°")
    with col_info2:
        st.metric("Skala", f"{scale_factor}x")
    with col_info3:
        st.metric("Translation X", f"{tx}px")
    with col_info4:
        st.metric("Translation Y", f"{ty}px")
    
    # Tampilkan gambar
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📷 Gambar Asli")
        st.image(image, use_column_width=True)
        st.caption(f"Ukuran: {w} x {h} pixels")
    
    with col2:
        st.subheader("✨ Hasil Transformasi")
        st.image(transformed, use_column_width=True)
        h_final, w_final = transformed.shape[:2]
        st.caption(f"Ukuran: {w_final} x {h_final} pixels")
    
    # Opsi download
    st.markdown("---")
    st.subheader("💾 Download Hasil")
    
    result_pil = Image.fromarray(transformed)
    from io import BytesIO
    buf = BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="📥 DOWNLOAD",
        data=byte_im,
        file_name="transformed_image.png",
        mime="image/png"
    )

else:
    st.info("👈 Silakan upload gambar melalui sidebar untuk memulai")
    st.markdown("""
    ### Fitur Aplikasi:
    - 🔄 Rotation: Putar gambar dari 0° hingga 360°
    - 🔍 Scaling: Perbesar atau perkecil gambar (0.1x - 3.0x)
    - ↔ Translation: Geser posisi gambar
    - 💾 Download: Simpan hasil transformasi
    """)
    st.markdown("---")
    st.subheader("📖 Cara Penggunaan:")
    st.markdown("""
    1. Upload gambar menggunakan tombol di sidebar
    2. Atur rotasi, skala, dan translasi sesuai kebutuhan
    3. Lihat hasil transformasi secara langsung
    4. Download gambar hasil jika sudah sesuai
    """)