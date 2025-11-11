import cv2
import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO

# Konfigurasi halaman
st.set_page_config(page_title="Image Transformation App", layout="wide")

# Judul aplikasi
st.title("IMAGE ROTATION, SCALING, AND AFFINE TRANSFORMATION VISUALIZER")
st.markdown("Rotate, Scale, Affine Transform dan manipulasi gambar dengan kontrol interaktif")

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

    # Pilih mode transformasi
    st.sidebar.subheader("🎯 Mode Transformasi")
    transform_mode = st.sidebar.radio("Pilih Mode:", ["Basic (Rotation + Scaling)", "Affine Transformation"])

    if transform_mode == "Basic (Rotation + Scaling)":
        # Kontrol Rotation
        st.sidebar.subheader("🔄 Rotation")
        rotation_angle = st.sidebar.slider("Sudut Rotasi (derajat)", 0, 360, 0, 1)

        # Kontrol Scaling
        st.sidebar.subheader("🔍 Scaling")
        scale_factor = st.sidebar.slider("Faktor Skala", 0.1, 3.0, 1.0, 0.1)

        # Kontrol Translation
        st.sidebar.subheader("↔ Translation")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            tx = st.number_input("Shift X", -500, 500, 0, 10)
        with col2:
            ty = st.number_input("Shift Y", -500, 500, 0, 10)

        # Proses Transformasi Basic
        transformed = image.copy()

        # Scaling
        if scale_factor != 1.0:
            new_w = int(w * scale_factor)
            new_h = int(h * scale_factor)
            transformed = cv2.resize(transformed, (new_w, new_h))

        h_trans, w_trans = transformed.shape[:2]

        # Rotation
        if rotation_angle != 0:
            center = (w_trans // 2, h_trans // 2)
            M_rotate = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
            cos = np.abs(M_rotate[0, 0])
            sin = np.abs(M_rotate[0, 1])
            new_w = int((h_trans * sin) + (w_trans * cos))
            new_h = int((h_trans * cos) + (w_trans * sin))
            M_rotate[0, 2] += (new_w / 2) - center[0]
            M_rotate[1, 2] += (new_h / 2) - center[1]
            transformed = cv2.warpAffine(transformed, M_rotate, (new_w, new_h),
                                         borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

        # Translation
        if tx != 0 or ty != 0:
            h_trans, w_trans = transformed.shape[:2]
            M_translate = np.float32([[1, 0, tx], [0, 1, ty]])
            transformed = cv2.warpAffine(transformed, M_translate, (w_trans, h_trans),
                                         borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

        # Info metrics
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

    else:
        # Affine Transformation
        st.sidebar.subheader("🔷 Affine Transform")
        st.sidebar.markdown("**Source Points (Titik Asal):**")
        
        # Source Points
        col1, col2 = st.sidebar.columns(2)
        with col1:
            src_x1 = st.number_input("P1 X", 0, w, min(50, w), 5, key="src_x1")
            src_x2 = st.number_input("P2 X", 0, w, min(200, w), 5, key="src_x2")
            src_x3 = st.number_input("P3 X", 0, w, min(50, w), 5, key="src_x3")
        with col2:
            src_y1 = st.number_input("P1 Y", 0, h, min(50, h), 5, key="src_y1")
            src_y2 = st.number_input("P2 Y", 0, h, min(50, h), 5, key="src_y2")
            src_y3 = st.number_input("P3 Y", 0, h, min(200, h), 5, key="src_y3")
        
        st.sidebar.markdown("**Destination Points (Titik Tujuan):**")
        
        # Destination Points
        col3, col4 = st.sidebar.columns(2)
        with col3:
            dst_x1 = st.number_input("P1' X", 0, w, min(10, w), 5, key="dst_x1")
            dst_x2 = st.number_input("P2' X", 0, w, min(200, w), 5, key="dst_x2")
            dst_x3 = st.number_input("P3' X", 0, w, min(100, w), 5, key="dst_x3")
        with col4:
            dst_y1 = st.number_input("P1' Y", 0, h, min(100, h), 5, key="dst_y1")
            dst_y2 = st.number_input("P2' Y", 0, h, min(50, h), 5, key="dst_y2")
            dst_y3 = st.number_input("P3' Y", 0, h, min(250, h), 5, key="dst_y3")
        
        # Hitung Affine Transform
        pts1 = np.float32([[src_x1, src_y1], [src_x2, src_y2], [src_x3, src_y3]])
        pts2 = np.float32([[dst_x1, dst_y1], [dst_x2, dst_y2], [dst_x3, dst_y3]])
        M_affine = cv2.getAffineTransform(pts1, pts2)
        transformed = cv2.warpAffine(image, M_affine, (w, h),
                                     borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
        
        st.markdown("---")
        st.info("🔷 Mode Affine Transformation aktif")
        
        # Tampilkan info titik
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown("**Titik Source:**")
            st.text(f"P1: ({src_x1}, {src_y1})")
            st.text(f"P2: ({src_x2}, {src_y2})")
            st.text(f"P3: ({src_x3}, {src_y3})")
        with col_info2:
            st.markdown("**Titik Destination:**")
            st.text(f"P1': ({dst_x1}, {dst_y1})")
            st.text(f"P2': ({dst_x2}, {dst_y2})")
            st.text(f"P3': ({dst_x3}, {dst_y3})")

    # Tombol reset
    if st.sidebar.button("🔄 Reset ke Default"):
        st.rerun()

    # Tampilan Output
    st.markdown("---")
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
    buf = BytesIO()
    result_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 DOWNLOAD HASIL TRANSFORMASI",
        data=byte_im,
        file_name="transformed_image.png",
        mime="image/png"
    )

else:
    st.info("👈 Silakan upload gambar melalui sidebar untuk memulai")
    st.markdown("""
    ### Fitur Aplikasi:
    - 🔄 **Rotation**: Putar gambar dari 0° hingga 360°
    - 🔍 **Scaling**: Perbesar atau perkecil gambar (0.1x - 3.0x)
    - ↔ **Translation**: Geser posisi gambar
    - 🔷 **Affine Transformation**: Transformasi affine dengan 3 titik kontrol
    - 💾 **Download**: Simpan hasil transformasi
    """)
    st.markdown("---")
    st.subheader("📖 Cara Penggunaan:")
    st.markdown("""
    1. Upload gambar menggunakan tombol di sidebar
    2. Pilih mode transformasi:
       - **Basic**: Untuk rotasi, scaling, dan translasi
       - **Affine**: Untuk transformasi affine dengan kontrol 3 titik
    3. Atur parameter sesuai kebutuhan
    4. Lihat hasil transformasi secara langsung
    5. Download gambar hasil jika sudah sesuai
    
    **Tips Affine Transformation:**
    - Atur 3 titik source (P1, P2, P3) pada posisi awal
    - Atur 3 titik destination (P1', P2', P3') ke posisi tujuan
    - Transformasi akan memetakan segitiga source ke segitiga destination
    """)