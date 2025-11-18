import cv2
import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO
from streamlit_cropper import st_cropper

# Konfigurasi aplikasi
st.set_page_config(page_title="Image Transformation App", layout="wide")

# Judul
st.title("IMAGE ROTATION, SCALING, AND AFFINE TRANSFORMATION VISUALIZER")
st.markdown("Rotate, Scale, Translate, Affine Transform, ROI Scaling, dan Batch Processing")

# Sidebar
st.sidebar.header("⚙ Kontrol Transformasi")

# Pilihan mode pemrosesan
mode = st.sidebar.radio("Mode Pemrosesan", ["Single Image", "Batch Processing"])

# Upload gambar
if mode == "Batch Processing":
    uploaded_files = st.sidebar.file_uploader(
        "Upload Beberapa Gambar",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )
else:
    uploaded_files = st.sidebar.file_uploader(
        "Upload Gambar",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=False
    )

# ========================================================================
# Fungsi DISPLAY Helper
# ========================================================================
def display_resized(image, max_width=350):
    """Resize hanya untuk tampilan agar konsisten."""
    h, w = image.shape[:2]
    scale = max_width / w
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(image, (new_w, new_h))
    return resized

# ========================================================================
# Fungsi transformasi full image dengan mode basic
# ========================================================================
def apply_basic_transform(image, rotation_angle, scale_factor, tx, ty):
    h, w = image.shape[:2]

    # 1. Scaling Full Image
    if scale_factor != 1.0:
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)
        img = cv2.resize(image, (new_w, new_h))
    else:
        img = image.copy()

    h, w = img.shape[:2]

    # 2. Rotation
    if rotation_angle != 0:
        center = (w // 2, h // 2)
        M_rotate = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        cos = np.abs(M_rotate[0, 0])
        sin = np.abs(M_rotate[0, 1])

        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        M_rotate[0, 2] += (new_w / 2) - center[0]
        M_rotate[1, 2] += (new_h / 2) - center[1]

        img = cv2.warpAffine(
            img, M_rotate, (new_w, new_h),
            borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255)
        )

    # 3. Translation
    if tx != 0 or ty != 0:
        M_translate = np.float32([[1, 0, tx], [0, 1, ty]])
        img = cv2.warpAffine(
            img, M_translate, (img.shape[1], img.shape[0]),
            borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255)
        )

    return img

# ========================================================================
# Fungsi transformasi affine
# ========================================================================
def apply_affine_transform(image, pts1, pts2):
    h, w = image.shape[:2]
    M_affine = cv2.getAffineTransform(pts1, pts2)
    transformed = cv2.warpAffine(image, M_affine, (w, h),
                                 borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    return transformed

# ========================================================================
# Fungsi ROI Scaling
# ========================================================================
def scale_roi(image, scale_factor):
    st.info("Pilih area ROI di bawah ini, lalu ROI akan di-scale.")

    roi = st_cropper(
        Image.fromarray(image),
        realtime_update=True,
        box_color="#FF0000",
        aspect_ratio=None
    )

    roi_np = np.array(roi)

    # Scale ROI
    h, w = roi_np.shape[:2]
    new_w = int(w * scale_factor)
    new_h = int(h * scale_factor)
    scaled_roi = cv2.resize(roi_np, (new_w, new_h))

    return roi_np, scaled_roi

# ========================================================================
# Fungsi untuk memproses satu gambar
# ========================================================================
def process_single_image(image, transform_mode, roi_scale_mode=None, **params):
    """
    Memproses satu gambar berdasarkan mode transformasi yang dipilih
    """
    if transform_mode == "Basic (Rotation + Scaling)":
        if roi_scale_mode == "Scale ROI Saja":
            return None  # ROI akan diproses terpisah
        else:
            return apply_basic_transform(
                image,
                params.get('rotation_angle', 0),
                params.get('scale_factor', 1.0),
                params.get('tx', 0),
                params.get('ty', 0)
            )
    elif transform_mode == "Affine Transformation":
        pts1 = params.get('pts1')
        pts2 = params.get('pts2')
        return apply_affine_transform(image, pts1, pts2)

# ========================================================================
# ======================== MODE SINGLE IMAGE =============================
# ========================================================================
if mode == "Single Image":

    if uploaded_files is not None:
        file = uploaded_files

        # Baca gambar
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
        image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        h, w = image.shape[:2]
        st.sidebar.success(f"Ukuran gambar: {w} x {h} pixels")

        # Pilih mode transformasi
        st.sidebar.subheader("🎯 Mode Transformasi")
        transform_mode = st.sidebar.radio("Pilih Mode:", ["Basic (Rotation + Scaling)", "Affine Transformation"])

        if transform_mode == "Basic (Rotation + Scaling)":
            # Mode ROI
            st.sidebar.subheader("🟥 ROI Scaling Mode")
            roi_scale_mode = st.sidebar.radio(
                "Pilih Mode Scaling:",
                ["Scale Full Image", "Scale ROI Saja"]
            )

            # Kontrol Rotation
            st.sidebar.subheader("🔄 Rotation")
            rotation_angle = st.sidebar.slider("Sudut Rotasi (°)", 0, 360, 0, 1)

            # Kontrol Scaling
            st.sidebar.subheader("🔍 Scaling")
            scale_factor = st.sidebar.slider("Faktor Skala", 0.1, 3.0, 1.0, 0.1)

            # Kontrol Translation
            st.sidebar.subheader("↔ Translation")
            col1, col2 = st.sidebar.columns(2)
            tx = col1.number_input("Shift X", -500, 500, 0, 10)
            ty = col2.number_input("Shift Y", -500, 500, 0, 10)

            # Tampilan gambar asli
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📷 Gambar Asli")
                st.image(image, use_container_width=True)
                st.caption(f"Ukuran: {w} x {h} pixels")

            if roi_scale_mode == "Scale Full Image":
                # Proses transformasi basic
                transformed = apply_basic_transform(image, rotation_angle, scale_factor, tx, ty)

                with col2:
                    st.subheader("✨ Hasil Transformasi")
                    st.image(transformed, use_container_width=True)
                    h_final, w_final = transformed.shape[:2]
                    st.caption(f"Ukuran: {w_final} x {h_final} pixels")

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

                # Download
                st.markdown("---")
                buf = BytesIO()
                Image.fromarray(transformed).save(buf, format="PNG")
                st.download_button(
                    label="📥 DOWNLOAD HASIL TRANSFORMASI",
                    data=buf.getvalue(),
                    file_name="transformed.png",
                    mime="image/png"
                )

            else:  # Scale ROI Saja
                st.markdown("---")
                st.subheader("🟥 ROI Scaling")
                original_roi, scaled_roi = scale_roi(image, scale_factor)

                col3, col4 = st.columns(2)
                with col3:
                    st.write("**ROI Asli:**")
                    st.image(original_roi, use_container_width=True)
                    h_roi, w_roi = original_roi.shape[:2]
                    st.caption(f"Ukuran: {w_roi} x {h_roi} pixels")

                with col4:
                    st.write("**ROI Setelah Scaling:**")
                    st.image(scaled_roi, use_container_width=True)
                    h_scaled, w_scaled = scaled_roi.shape[:2]
                    st.caption(f"Ukuran: {w_scaled} x {h_scaled} pixels")

                # Download ROI
                st.markdown("---")
                buf = BytesIO()
                Image.fromarray(scaled_roi).save(buf, format="PNG")
                st.download_button(
                    label="📥 DOWNLOAD ROI SCALED",
                    data=buf.getvalue(),
                    file_name="scaled_roi.png",
                    mime="image/png"
                )

        else:  # Affine Transformation
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
            transformed = apply_affine_transform(image, pts1, pts2)
            
            # Tampilan
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📷 Gambar Asli")
                st.image(image, use_container_width=True)
                st.caption(f"Ukuran: {w} x {h} pixels")

            with col2:
                st.subheader("✨ Hasil Transformasi")
                st.image(transformed, use_container_width=True)
                h_final, w_final = transformed.shape[:2]
                st.caption(f"Ukuran: {w_final} x {h_final} pixels")

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

            # Download
            st.markdown("---")
            buf = BytesIO()
            Image.fromarray(transformed).save(buf, format="PNG")
            st.download_button(
                label="📥 DOWNLOAD HASIL TRANSFORMASI",
                data=buf.getvalue(),
                file_name="affine_transformed.png",
                mime="image/png"
            )

        # Tombol reset
        if st.sidebar.button("🔄 Reset ke Default"):
            st.rerun()

    else:
        st.info("👈 Silakan upload gambar melalui sidebar untuk memulai")
        st.markdown("""
        ### Fitur Aplikasi:
        - 🔄 **Rotation**: Putar gambar dari 0° hingga 360°
        - 🔍 **Scaling**: Perbesar atau perkecil gambar (0.1x - 3.0x)
        - ↔ **Translation**: Geser posisi gambar
        - 🟥 **ROI Scaling**: Scale area tertentu dari gambar
        - 🔷 **Affine Transformation**: Transformasi affine dengan 3 titik kontrol
        - 📦 **Batch Processing**: Proses beberapa gambar sekaligus
        - 💾 **Download**: Simpan hasil transformasi
        """)

# ========================================================================
# ======================== MODE BATCH PROCESSING ========================
# ========================================================================
elif mode == "Batch Processing":

    if not uploaded_files:
        st.info("👈 Upload beberapa gambar untuk diproses secara batch.")
        st.markdown("""
        ### Batch Processing Mode:
        - Upload beberapa gambar sekaligus
        - Terapkan transformasi yang sama ke semua gambar
        - Download hasil satu per satu
        """)
    else:
        st.success(f"✅ {len(uploaded_files)} gambar berhasil diupload")

        # Pilih mode transformasi untuk batch
        st.sidebar.subheader("🎯 Mode Transformasi")
        transform_mode = st.sidebar.radio("Pilih Mode:", ["Basic (Rotation + Scaling)", "Affine Transformation"])

        if transform_mode == "Basic (Rotation + Scaling)":
            # Mode ROI
            st.sidebar.subheader("🟥 ROI Scaling Mode")
            roi_scale_mode = st.sidebar.radio(
                "Pilih Mode Scaling:",
                ["Scale Full Image", "Scale ROI Saja"]
            )

            # Kontrol transformasi
            st.sidebar.subheader("🔄 Rotation")
            rotation_angle = st.sidebar.slider("Sudut Rotasi (°)", 0, 360, 0, 1)

            st.sidebar.subheader("🔍 Scaling")
            scale_factor = st.sidebar.slider("Faktor Skala", 0.1, 3.0, 1.0, 0.1)

            st.sidebar.subheader("↔ Translation")
            col1, col2 = st.sidebar.columns(2)
            tx = col1.number_input("Shift X", -500, 500, 0, 10)
            ty = col2.number_input("Shift Y", -500, 500, 0, 10)

            # Proses setiap gambar
            for idx, file in enumerate(uploaded_files):
                st.markdown(f"## 📷 Gambar {idx + 1}: {file.name}")

                file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
                image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Gambar Asli")
                    st.image(display_resized(image), use_container_width=False)
                    h, w = image.shape[:2]
                    st.caption(f"Ukuran: {w} x {h} pixels")

                if roi_scale_mode == "Scale Full Image":
                    transformed = apply_basic_transform(image, rotation_angle, scale_factor, tx, ty)

                    with col2:
                        st.subheader("Hasil Transformasi")
                        st.image(display_resized(transformed), use_container_width=False)
                        h_final, w_final = transformed.shape[:2]
                        st.caption(f"Ukuran: {w_final} x {h_final} pixels")

                    buf = BytesIO()
                    Image.fromarray(transformed).save(buf, format="PNG")
                    st.download_button(
                        f"📥 Download Hasil {idx + 1}",
                        buf.getvalue(),
                        file_name=f"transformed_{idx + 1}.png",
                        key=f"download_basic_{idx}"
                    )

                else:  # Scale ROI Saja
                    st.markdown("**🟥 ROI Scaling**")
                    original_roi, scaled_roi = scale_roi(image, scale_factor)

                    col3, col4 = st.columns(2)
                    with col3:
                        st.write("ROI Asli:")
                        st.image(display_resized(original_roi), use_container_width=False)

                    with col4:
                        st.write("ROI Setelah Scaling:")
                        st.image(display_resized(scaled_roi), use_container_width=False)

                    buf = BytesIO()
                    Image.fromarray(scaled_roi).save(buf, format="PNG")
                    st.download_button(
                        f"📥 Download ROI Scaled {idx + 1}",
                        buf.getvalue(),
                        file_name=f"scaled_roi_{idx + 1}.png",
                        key=f"download_roi_{idx}"
                    )

                st.markdown("---")

        else:  # Affine Transformation untuk Batch
            st.info("⚠️ Untuk Affine Transformation dalam batch processing, semua gambar akan menggunakan titik yang sama. Pastikan gambar memiliki ukuran yang serupa.")
            
            # Ambil ukuran gambar pertama sebagai referensi
            first_file_bytes = np.asarray(bytearray(uploaded_files[0].read()), dtype=np.uint8)
            first_image = cv2.cvtColor(cv2.imdecode(first_file_bytes, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
            h_ref, w_ref = first_image.shape[:2]
            
            st.sidebar.subheader("🔷 Affine Transform")
            st.sidebar.markdown(f"**Referensi ukuran: {w_ref} x {h_ref}**")
            st.sidebar.markdown("**Source Points:**")
            
            # Source Points
            col1, col2 = st.sidebar.columns(2)
            with col1:
                src_x1 = st.number_input("P1 X", 0, w_ref, min(50, w_ref), 5, key="batch_src_x1")
                src_x2 = st.number_input("P2 X", 0, w_ref, min(200, w_ref), 5, key="batch_src_x2")
                src_x3 = st.number_input("P3 X", 0, w_ref, min(50, w_ref), 5, key="batch_src_x3")
            with col2:
                src_y1 = st.number_input("P1 Y", 0, h_ref, min(50, h_ref), 5, key="batch_src_y1")
                src_y2 = st.number_input("P2 Y", 0, h_ref, min(50, h_ref), 5, key="batch_src_y2")
                src_y3 = st.number_input("P3 Y", 0, h_ref, min(200, h_ref), 5, key="batch_src_y3")
            
            st.sidebar.markdown("**Destination Points:**")
            col3, col4 = st.sidebar.columns(2)
            with col3:
                dst_x1 = st.number_input("P1' X", 0, w_ref, min(10, w_ref), 5, key="batch_dst_x1")
                dst_x2 = st.number_input("P2' X", 0, w_ref, min(200, w_ref), 5, key="batch_dst_x2")
                dst_x3 = st.number_input("P3' X", 0, w_ref, min(100, w_ref), 5, key="batch_dst_x3")
            with col4:
                dst_y1 = st.number_input("P1' Y", 0, h_ref, min(100, h_ref), 5, key="batch_dst_y1")
                dst_y2 = st.number_input("P2' Y", 0, h_ref, min(50, h_ref), 5, key="batch_dst_y2")
                dst_y3 = st.number_input("P3' Y", 0, h_ref, min(250, h_ref), 5, key="batch_dst_y3")
            
            pts1 = np.float32([[src_x1, src_y1], [src_x2, src_y2], [src_x3, src_y3]])
            pts2 = np.float32([[dst_x1, dst_y1], [dst_x2, dst_y2], [dst_x3, dst_y3]])

            # Reset file pointer untuk membaca ulang
            for idx, file in enumerate(uploaded_files):
                st.markdown(f"## 📷 Gambar {idx + 1}: {file.name}")
                
                file.seek(0)  # Reset pointer
                file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
                image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

                transformed = apply_affine_transform(image, pts1, pts2)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Gambar Asli")
                    st.image(display_resized(image), use_container_width=False)
                    
                with col2:
                    st.subheader("Hasil Transformasi")
                    st.image(display_resized(transformed), use_container_width=False)

                buf = BytesIO()
                Image.fromarray(transformed).save(buf, format="PNG")
                st.download_button(
                    f"📥 Download Hasil {idx + 1}",
                    buf.getvalue(),
                    file_name=f"affine_transformed_{idx + 1}.png",
                    key=f"download_affine_{idx}"
                )

                st.markdown("---")