# 🖼️ Image Transformation Visualizer

An interactive web application for image transformation using OpenCV and Streamlit. This application supports various types of transformations such as rotation, scaling, translation, and affine transformation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔄 Basic Mode (Rotation + Scaling)
- **Rotation**: Rotate images from 0° to 360°
- **Scaling**: Zoom in or out (0.1x - 3.0x)
- **Translation**: Shift image position horizontally and vertically

### 🔷 Affine Transformation Mode
- Affine transformation with 3-point control
- Set source and destination points
- Supports rotation, scaling, shearing, and translation in one transformation
- Real-time visualization of transformation results

### 💾 Additional Features
- Side-by-side preview of original and transformed images
- Image dimensions and transformation parameter info
- Download transformed results in PNG format
- Reset button to restore default settings
- Responsive and user-friendly interface

## 🚀 Demo
[Live Demo](https://image-transformation.streamlit.app/)

![App Screenshot](https://drive.google.com/file/d/13Xc6YkrX883JNM_u5t74UCLLdzNu9f3E/view?usp=sharing)
*Screenshot showing the image transformation interface*

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🔧 Installation

### 1. Clone Repository

```bash
git https://github.com/RaffiDM/Image-Transformation.git
cd Image-Transformation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
streamlit
opencv-python
pillow
```

### 3. Install System Dependencies (Linux/Ubuntu)

For Linux users, install system dependencies:

```bash
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx
```

**packages.txt** (for Streamlit Cloud deployment):
```
libgl1-mesa-glx
```

## 🎮 Usage

### Running the Application

```bash
streamlit run transformation.py
```

The application will open in your browser at `http://localhost:8501`

### Step-by-Step Guide

1. **Upload Image**
   - Click "Upload Gambar" button in the sidebar
   - Select an image (formats: JPG, JPEG, PNG)

2. **Select Transformation Mode**
   - **Basic**: For rotation, scaling, and translation
   - **Affine**: For affine transformation with point control

3. **Adjust Parameters**
   
   **Basic Mode:**
   - Slide the rotation slider (0°-360°)
   - Set scale factor (0.1x-3.0x)
   - Input X and Y translation values
   
   **Affine Mode:**
   - Set 3 source points (P1, P2, P3)
   - Set 3 destination points (P1', P2', P3')
   - View transformation results in real-time

4. **Download Results**
   - Click "DOWNLOAD HASIL TRANSFORMASI" button
   - Image will be saved as `transformed_image.png`

## 📁 Project Structure

```
Image-Transformation/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── packages.txt          # System dependencies
├── README.md             # Documentation
```

## 🔬 Technical Details

### Transformations Used

#### 1. Rotation
Using `cv2.getRotationMatrix2D()` and `cv2.warpAffine()`:
```python
M_rotate = cv2.getRotationMatrix2D(center, angle, scale)
rotated = cv2.warpAffine(image, M_rotate, (w, h))
```

#### 2. Scaling
Using `cv2.resize()`:
```python
scaled = cv2.resize(image, (new_width, new_height))
```

#### 3. Translation
Using translation matrix:
```python
M_translate = np.float32([[1, 0, tx], [0, 1, ty]])
translated = cv2.warpAffine(image, M_translate, (w, h))
```

#### 4. Affine Transformation
Using 3 control points to calculate affine matrix:
```python
pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3]])  # Source
pts2 = np.float32([[x1', y1'], [x2', y2'], [x3', y3']])  # Destination
M = cv2.getAffineTransform(pts1, pts2)
affine = cv2.warpAffine(image, M, (w, h))
```

## 🎓 Use Cases

- **Education**: Learning image transformation and computer vision
- **Image Processing**: Preprocessing for machine learning
- **Perspective Correction**: Fixing photo angles
- **Graphic Design**: Experimenting with visual transformations
- **Research**: Analyzing transformation effects on images

## 🐛 Troubleshooting

### Error: "No module named 'cv2'"
```bash
pip install opencv-python
```

### Error: "libGL.so.1: cannot open shared object file"
```bash
sudo apt-get install libgl1-mesa-glx
```

### Error: "StreamlitAPIException: default value exceeds max_value"
- Ensure uploaded images have minimum dimensions of 250x250 pixels
- Or use images with larger dimensions

## 🤝 Contributing

Contributions are always welcome! Please:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Author
- Raffi Dzaky Mahendra
- Valentino Ryo Koesdarto
- Liem, Ivan Budiono

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Framework for creating web apps
- [OpenCV](https://opencv.org/) - Computer vision library
- [NumPy](https://numpy.org/) - Numerical computing library
- [Pillow](https://python-pillow.org/) - Image processing library

---

⭐ If this project helps you, don't forget to give it a star on GitHub!