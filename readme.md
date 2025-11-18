# 🖼️ Image Transformation Visualizer

An interactive web application for image transformation using OpenCV and Streamlit. This application supports various types of transformations such as rotation, scaling, translation, affine transformation, ROI scaling, and batch processing.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔄 Basic Mode (Rotation + Scaling)
- **Rotation**: Rotate images from 0° to 360°
- **Scaling**: Zoom in or out (0.1x - 3.0x)
- **Translation**: Shift image position horizontally and vertically
- **Full Image Scaling**: Apply transformations to the entire image
- **ROI Scaling**: Select and scale specific regions of interest

### 🟥 ROI (Region of Interest) Scaling
- Interactive ROI selection using cropper tool
- Scale only selected area of the image
- Visual comparison between original and scaled ROI
- Maintain original image while transforming specific regions

### 🔷 Affine Transformation Mode
- Affine transformation with 3-point control
- Set source and destination points
- Supports rotation, scaling, shearing, and translation in one transformation
- Real-time visualization of transformation results

### 📦 Batch Processing Mode
- Process multiple images simultaneously
- Apply same transformation to all uploaded images
- Support for both Basic and Affine transformations
- Individual download for each processed image
- Consistent transformation parameters across all images

### 💾 Additional Features
- **Single Image Mode**: Process one image at a time with detailed controls
- **Batch Processing Mode**: Handle multiple images efficiently
- Side-by-side preview of original and transformed images
- Image dimensions and transformation parameter info
- Download transformed results in PNG format
- Reset button to restore default settings
- Responsive and user-friendly interface

## 🚀 Demo
[Live Demo](https://image-transformation.streamlit.app/)

![App Screenshot](https://github.com/user-attachments/assets/8ad2b010-0dbc-4288-a78c-fad8d223f306)
![App Screenshot](https://github.com/user-attachments/assets/b34a1fd2-45d6-4856-a064-8d30a466d599)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🔧 Installation

### 1. Clone Repository

```bash
git clone https://github.com/RaffiDM/Image-Transformation.git
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
numpy
streamlit-cropper
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

#### 1. **Select Processing Mode**
   - **Single Image**: Process one image with detailed controls
   - **Batch Processing**: Process multiple images at once

#### 2. **Upload Image(s)**
   - **Single Image Mode**: Upload one image
   - **Batch Processing Mode**: Upload multiple images
   - Supported formats: JPG, JPEG, PNG

#### 3. **Select Transformation Mode**
   - **Basic (Rotation + Scaling)**: For rotation, scaling, translation, and ROI
   - **Affine Transformation**: For affine transformation with point control

#### 4. **Adjust Parameters**
   
   **Basic Mode:**
   - Choose scaling mode:
     - **Scale Full Image**: Apply transformations to entire image
     - **Scale ROI Saja**: Select and scale specific region
   - Slide the rotation slider (0°-360°)
   - Set scale factor (0.1x-3.0x)
   - Input X and Y translation values
   
   **ROI Scaling Mode:**
   - Select area on the image using the cropper tool
   - Adjust scale factor for the selected region
   - Compare original ROI with scaled version
   
   **Affine Mode:**
   - Set 3 source points (P1, P2, P3)
   - Set 3 destination points (P1', P2', P3')
   - View transformation results in real-time

#### 5. **Download Results**
   - Click download button for each processed image
   - Images saved as PNG format
   - Batch mode: Download each image individually

## 📁 Project Structure

```
Image-Transformation/
│
├── transformation.py     # Main application file
├── requirements.txt      # Python dependencies
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

#### 5. ROI Scaling
Using `streamlit-cropper` and `cv2.resize()`:
```python
# Interactive ROI selection
roi = st_cropper(Image.fromarray(image), realtime_update=True)
# Scale selected ROI
scaled_roi = cv2.resize(roi_np, (new_w, new_h))
```

## 🎓 Use Cases

- **Education**: Learning image transformation and computer vision
- **Image Processing**: Preprocessing for machine learning
- **Batch Editing**: Process multiple images with same transformation
- **Perspective Correction**: Fixing photo angles
- **ROI Analysis**: Focus on specific image regions
- **Graphic Design**: Experimenting with visual transformations
- **Research**: Analyzing transformation effects on images

## 🆕 What's New

### Version 2.0
- ✅ **Batch Processing Mode**: Process multiple images simultaneously
- ✅ **ROI Scaling**: Select and transform specific image regions
- ✅ **Enhanced UI**: Improved layout and user experience
- ✅ **Mode Selection**: Switch between Single Image and Batch Processing
- ✅ **Display Optimization**: Better image visualization with consistent sizing

## 🐛 Troubleshooting

### Error: "No module named 'cv2'"
```bash
pip install opencv-python
```

### Error: "No module named 'streamlit_cropper'"
```bash
pip install streamlit-cropper
```

### Error: "libGL.so.1: cannot open shared object file"
```bash
sudo apt-get install libgl1-mesa-glx
```

### Error: "StreamlitAPIException: default value exceeds max_value"
- Ensure uploaded images have minimum dimensions of 250x250 pixels
- Or use images with larger dimensions

### Batch Processing Tips
- For Affine transformation in batch mode, use images with similar dimensions
- The first uploaded image determines reference points for Affine transformation
- Processing time increases with number of images and their sizes

## 🤝 Contributing

Contributions are always welcome! Please:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Authors
- Raffi Dzaky Mahendra
- Valentino Ryo Koesdarto
- Liem, Ivan Budiono

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Framework for creating web apps
- [OpenCV](https://opencv.org/) - Computer vision library
- [NumPy](https://numpy.org/) - Numerical computing library
- [Pillow](https://python-pillow.org/) - Image processing library
- [Streamlit-Cropper](https://github.com/turner-anderson/streamlit-cropper) - Interactive image cropping component

---

⭐ If this project helps you, don't forget to give it a star on GitHub!