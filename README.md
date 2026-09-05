# 🖼️ ImagePro Studio – Image Processing Tools

<p align="center">
  <b>A Simple Web-Based Image Processing Application using Python, Flask & OpenCV</b>
</p>

<p align="center">
  Upload images, capture images using your camera, apply image-processing operations, and download the processed result.
</p>

---

## 📌 About the Project

**ImagePro Studio** is a web-based image processing application developed using **Python, Flask, OpenCV, NumPy, HTML, CSS, and JavaScript**.

The application provides a simple and interactive interface for performing common image-processing operations. Users can upload an image from their computer or capture an image using their browser camera, select an operation, process the image, and download the result.

This project is designed for **educational purposes** and demonstrates fundamental concepts of digital image processing using OpenCV.

---

## ✨ Features

- 📤 Upload images from your computer
- 📷 Capture images using the browser camera
- 🖼️ Preview the original image
- ⚙️ Apply different image-processing operations
- 🎚️ Adjust processing parameters
- 👀 View the processed image
- 💾 Download processed images
- 🔄 Reset and process another image
- 📱 Responsive web interface
- 🐍 Python + Flask backend
- 🔬 OpenCV-based image processing

---

## 🛠️ Image Processing Operations

The application currently supports the following operations:

| No. | Operation |
|---:|---|
| 1 | Load and Display Image |
| 2 | Convert Image to Grayscale |
| 3 | Convert Image to Binary |
| 4 | Convert Image Between JPG, PNG and BMP |
| 5 | RGB to Grayscale |
| 6 | RGB to HSV |
| 7 | Histogram Equalization |
| 8 | Brightness and Contrast Adjustment |
| 9 | Average Filter |
| 10 | Gaussian Filter |
| 11 | Laplacian Sharpening |
| 12 | Sobel Edge Detection |
| 13 | Canny Edge Detection |

---

## 💻 Technologies Used

### Backend
- Python
- Flask
- OpenCV
- NumPy

### Frontend
- HTML5
- CSS3
- JavaScript

### Image Processing
- OpenCV
- NumPy

---

## 📂 Project Structure

```text
Image-processing-tools/
│
├── app.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── script.js
│   └── style.css
│
├── uploads/
│
└── outputs/

🔄 How the Application Works
              USER
                │
                ▼
        ┌─────────────────┐
        │  Web Interface  │
        └────────┬────────┘
                 │
        ┌────────┴─────────┐
        │                  │
        ▼                  ▼
   Upload Image       Camera Capture
        │                  │
        └────────┬─────────┘
                 ▼
        ┌─────────────────┐
        │  Flask Backend  │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ OpenCV + NumPy  │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Processed Image │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Display Result  │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Download Image  │
        └─────────────────┘


🚀 Installation and Setup

1️⃣ Clone the Repository

Open PowerShell or Command Prompt and run:

git clone https://github.com/Atharv-Ai09/Image-processing-tools.git

Then enter the project folder:

cd Image-processing-tools

2️⃣ Create a Virtual Environment

For Windows:

python -m venv venv

Activate the virtual environment:

venv\Scripts\activate

After activation, you should see something similar to:

(venv) PS C:\...\Image-processing-tools>

3️⃣ Install Required Packages

Run:

pip install -r requirements.txt

If requirements.txt is not available, install the main packages manually:

pip install flask opencv-python numpy

4️⃣ Run the Application

Run:

python app.py

You should see something similar to:

Running on http://127.0.0.1:5000

Open your browser and visit:

http://127.0.0.1:5000

📷 Camera Feature

ImagePro Studio supports image capture through the browser camera.

When you select the Camera option:

Click Start Camera
Allow camera permission in your browser
Position the object/image in front of the camera
Click Capture
The captured image is sent to the Flask backend
Select an image-processing operation
Click Process Image
View and download the result

Note: Camera access requires browser permission.

🖼️ Example Operations

Grayscale Conversion

Converts a color image into a grayscale image.

Color Image
     ↓
Grayscale Conversion
     ↓
Gray Image
Binary Image

Converts an image into black and white using a threshold value.

Grayscale Image
       ↓
   Threshold
       ↓
 Binary Image
RGB to HSV

Converts an RGB/BGR image into the HSV color space.

HSV represents:

Hue
Saturation
Value
Histogram Equalization

Improves the contrast of an image by redistributing intensity values.

Gaussian Filter

Used for image smoothing and noise reduction.

Laplacian Sharpening

Enhances details and edges in an image.

Sobel Edge Detection

Detects edges in a selected direction:

Horizontal
Vertical
Both
Canny Edge Detection

Detects important edges in an image using the Canny edge detection algorithm.

Users can adjust:

Lower threshold
Upper threshold
📥 Supported Image Formats

The application supports:

JPG
JPEG
PNG
BMP

Processed images can also be downloaded in:

JPG
PNG
BMP
🎯 Project Objectives

The main objectives of this project are:

To understand fundamental image-processing concepts.
To implement image-processing techniques using OpenCV.
To create a simple web interface for image processing.
To understand communication between frontend and Flask backend.
To provide an easy-to-use platform for experimenting with image-processing operations.
To demonstrate practical applications of Python and OpenCV.
🎓 Educational Purpose

This project is developed as an academic/educational project for learning and demonstrating fundamental concepts of Digital Image Processing and Computer Vision.

It can be used for:

Image Processing Laboratory
Python Projects
OpenCV Learning
Computer Vision Basics
Diploma Project Demonstration
Academic Viva and Presentation
🔮 Future Enhancements

The project can be extended with additional features such as:

✂️ Image Cropping
🔄 Image Rotation
↔️ Image Flipping
📐 Image Resizing
🔍 Image Zoom
🖌️ Drawing Tools
🧹 Advanced Noise Removal
📊 Histogram Visualization
🖼️ Side-by-Side Image Comparison
↩️ Processing History
🌐 Online Deployment
📱 Improved mobile support
🔐 File Handling

Uploaded and processed images are stored temporarily in:

uploads/
outputs/

These folders are intended for application-generated files.

For GitHub repositories, generated image files should generally not be committed to the repository.

📋 Requirements

Recommended environment:

Python 3.x
Flask
OpenCV
NumPy
Modern Web Browser

Install dependencies using:

pip install -r requirements.txt
👨‍💻 Author
Atharv Shetty

Diploma in Artificial Intelligence and Machine Learning

GitHub:

Atharv-Ai09 on GitHub

⭐ Project Repository

Image Processing Tools – GitHub Repository

If you find this project useful for learning, consider giving the repository a ⭐.

📜 License

This project is created for educational and academic purposes.

You are free to study and modify the source code for learning purposes.

❤️ Acknowledgement

This project was developed to demonstrate the practical implementation of fundamental Image Processing techniques using Python and OpenCV through a web-based interface.

<p align="center"> <b>🖼️ ImagePro Studio</b><br> Image Processing Made Simple </p> ```
