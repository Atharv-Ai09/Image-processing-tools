<h1 align="center">🖼️ ImagePro Studio</h1>

<p align="center">
  <b>Image Processing Tools using OpenCV</b>
</p>

<p align="center">
  A web-based Image Processing application developed using Python, Flask and OpenCV.
</p>

<p align="center">
  <b>Final Year Project | GTTC Belagavi</b>
</p>

<hr>

<h2>📌 Project Overview</h2>

<p>
  <b>ImagePro Studio</b> is a web-based Image Processing application developed
  as a <b>Final Year Project</b> by students of the Artificial Intelligence &
  Machine Learning department at GTTC Belagavi.
</p>

<p>
  The main purpose of this project is to provide a simple, interactive and
  user-friendly platform for performing fundamental digital image processing
  operations using <b>OpenCV</b>.
</p>

<p>
  The application allows users to upload an image from their computer or
  capture an image using a web camera. After selecting an image, users can
  apply different image processing techniques and view the processed result
  directly in the browser.
</p>

<hr>

<h2>🎯 Objectives</h2>

<ul>
  <li>To understand the fundamentals of digital image processing.</li>
  <li>To implement image processing techniques using OpenCV.</li>
  <li>To develop a simple and user-friendly web-based application.</li>
  <li>To support image input through upload and camera capture.</li>
  <li>To perform image enhancement and filtering operations.</li>
  <li>To implement different edge detection techniques.</li>
  <li>To display the processed image in the browser.</li>
  <li>To allow users to download processed images.</li>
  <li>To gain practical knowledge of Python, Flask, OpenCV and NumPy.</li>
</ul>

<hr>

<h2>✨ Key Features</h2>

<ul>
  <li>📤 Upload images from a computer</li>
  <li>📷 Capture images using a web camera</li>
  <li>🖼️ Original image preview</li>
  <li>⚫ Grayscale conversion</li>
  <li>◼️ Binary thresholding</li>
  <li>🌈 RGB to HSV conversion</li>
  <li>📊 Histogram equalization</li>
  <li>☀️ Brightness adjustment</li>
  <li>🎚️ Contrast adjustment</li>
  <li>🔲 Average filtering</li>
  <li>🌫️ Gaussian filtering</li>
  <li>🔍 Laplacian sharpening</li>
  <li>📐 Sobel edge detection</li>
  <li>✏️ Canny edge detection</li>
  <li>💾 Download processed images</li>
  <li>🔄 Reset and process another image</li>
  <li>🖼️ Support for JPG, JPEG, PNG and BMP images</li>
</ul>

<hr>

<h2>🛠️ Technologies Used</h2>

<table border="1" cellpadding="10" cellspacing="0">
  <tr>
    <th>Technology</th>
    <th>Purpose</th>
  </tr>

  <tr>
    <td><b>Python</b></td>
    <td>Main programming language</td>
  </tr>

  <tr>
    <td><b>Flask</b></td>
    <td>Backend web framework</td>
  </tr>

  <tr>
    <td><b>OpenCV</b></td>
    <td>Image processing operations</td>
  </tr>

  <tr>
    <td><b>NumPy</b></td>
    <td>Numerical and image array processing</td>
  </tr>

  <tr>
    <td><b>HTML5</b></td>
    <td>Web page structure</td>
  </tr>

  <tr>
    <td><b>CSS3</b></td>
    <td>Web page styling</td>
  </tr>

  <tr>
    <td><b>JavaScript</b></td>
    <td>Frontend interaction and camera functionality</td>
  </tr>

  <tr>
    <td><b>Web Camera API</b></td>
    <td>Capturing images through the browser</td>
  </tr>

  <tr>
    <td><b>Jinja2</b></td>
    <td>Flask HTML template rendering</td>
  </tr>
</table>

<hr>

<h2>🏗️ Architecture Design</h2>

<pre>
                       ┌─────────────────────┐
                       │        USER         │
                       └──────────┬──────────┘
                                  │
                         Upload / Camera
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │    FRONTEND LAYER   │
                       │                     │
                       │ HTML + CSS + JS     │
                       │                     │
                       │ • Upload Image      │
                       │ • Camera Capture    │
                       │ • Select Operation  │
                       │ • Preview Image     │
                       └──────────┬──────────┘
                                  │
                              HTTP Request
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │     BACKEND LAYER   │
                       │                     │
                       │ Python + Flask      │
                       │                     │
                       │ • File Handling     │
                       │ • Routes            │
                       │ • Request Handling  │
                       └──────────┬──────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ IMAGE PROCESSING    │
                       │       LAYER         │
                       │                     │
                       │ OpenCV + NumPy      │
                       │                     │
                       │ • Grayscale         │
                       │ • Binary            │
                       │ • RGB → HSV         │
                       │ • Histogram         │
                       │ • Filtering         │
                       │ • Laplacian         │
                       │ • Sobel             │
                       │ • Canny             │
                       └──────────┬──────────┘
                                  │
                           Processed Image
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │     OUTPUT LAYER    │
                       │                     │
                       │ • Display Result    │
                       │ • Download JPG      │
                       │ • Download PNG      │
                       │ • Download BMP      │
                       └─────────────────────┘
</pre>

<hr>

<h2>📂 Project File Structure</h2>

<pre>
ImageProStudio_fixed/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── uploads/
│   └── Uploaded images
│
└── outputs/
    └── Processed images
</pre>

<h3>📄 File Description</h3>

<table border="1" cellpadding="10" cellspacing="0">
  <tr>
    <th>File / Folder</th>
    <th>Description</th>
  </tr>

  <tr>
    <td><code>app.py</code></td>
    <td>Main Flask application and backend processing routes.</td>
  </tr>

  <tr>
    <td><code>index.html</code></td>
    <td>Main user interface of the application.</td>
  </tr>

  <tr>
    <td><code>style.css</code></td>
    <td>Provides styling, layout and visual design.</td>
  </tr>

  <tr>
    <td><code>script.js</code></td>
    <td>Handles frontend interaction, processing requests and camera functionality.</td>
  </tr>

  <tr>
    <td><code>requirements.txt</code></td>
    <td>Contains the required Python packages.</td>
  </tr>

  <tr>
    <td><code>uploads/</code></td>
    <td>Stores uploaded or captured images.</td>
  </tr>

  <tr>
    <td><code>outputs/</code></td>
    <td>Stores processed images generated by the application.</td>
  </tr>
</table>

<hr>

<h2>⚙️ Image Processing Operations</h2>

<table border="1" cellpadding="10" cellspacing="0">
  <tr>
    <th>No.</th>
    <th>Operation</th>
    <th>Purpose</th>
  </tr>

  <tr>
    <td>1</td>
    <td><b>Grayscale</b></td>
    <td>Converts a color image into a grayscale image.</td>
  </tr>

  <tr>
    <td>2</td>
    <td><b>Binary Threshold</b></td>
    <td>Converts an image into black and white using a threshold value.</td>
  </tr>

  <tr>
    <td>3</td>
    <td><b>RGB to HSV</b></td>
    <td>Converts the image from RGB/BGR color space to HSV.</td>
  </tr>

  <tr>
    <td>4</td>
    <td><b>Histogram Equalization</b></td>
    <td>Improves the contrast of a grayscale image.</td>
  </tr>

  <tr>
    <td>5</td>
    <td><b>Brightness & Contrast</b></td>
    <td>Adjusts image brightness and contrast.</td>
  </tr>

  <tr>
    <td>6</td>
    <td><b>Average Filter</b></td>
    <td>Smooths the image and reduces noise.</td>
  </tr>

  <tr>
    <td>7</td>
    <td><b>Gaussian Filter</b></td>
    <td>Provides smooth filtering and reduces image noise.</td>
  </tr>

  <tr>
    <td>8</td>
    <td><b>Laplacian</b></td>
    <td>Highlights edges and fine image details.</td>
  </tr>

  <tr>
    <td>9</td>
    <td><b>Sobel</b></td>
    <td>Detects horizontal and vertical edges.</td>
  </tr>

  <tr>
    <td>10</td>
    <td><b>Canny</b></td>
    <td>Detects significant edges in an image.</td>
  </tr>
</table>

<hr>

<h2>🔄 System Working</h2>

<ol>
  <li>User opens the ImagePro Studio web application.</li>
  <li>User uploads an image or captures an image using the camera.</li>
  <li>The selected image is displayed in the application.</li>
  <li>User selects the required image processing operation.</li>
  <li>The request is sent to the Flask backend.</li>
  <li>Flask receives and processes the request.</li>
  <li>OpenCV and NumPy perform the selected operation.</li>
  <li>The processed image is generated and stored in the output folder.</li>
  <li>The processed result is displayed in the browser.</li>
  <li>User can download the processed image.</li>
</ol>

<hr>

<h2>💻 Installation and Setup</h2>

<h3>Prerequisites</h3>

<ul>
  <li>Python 3.x</li>
  <li>Web Browser</li>
  <li>VS Code or PyCharm</li>
  <li>Web Camera (optional)</li>
</ul>

<h3>1. Clone the Repository</h3>

<pre>
git clone https://github.com/Atharv-Ai09/Image-processing-tools.git
cd Image-processing-tools
</pre>

<h3>2. Create Virtual Environment</h3>

<pre>
python -m venv venv
</pre>

<h3>3. Activate Virtual Environment</h3>

<p><b>Windows PowerShell:</b></p>

<pre>
venv\Scripts\activate
</pre>

<h3>4. Install Required Packages</h3>

<pre>
pip install -r requirements.txt
</pre>

<h3>5. Run the Application</h3>

<pre>
python app.py
</pre>

<h3>6. Open the Application</h3>

<p>
  Open the following address in your web browser:
</p>

<pre>
http://127.0.0.1:5000
</pre>

<hr>

<h2>📷 Camera Input</h2>

<p>
  ImagePro Studio supports image capture using the browser's camera.
  The user can allow camera access, capture an image and use the captured
  image for image processing.
</p>

<p>
  Camera functionality is implemented using the browser's
  <b>Web Camera API</b> and JavaScript.
</p>

<hr>

<h2>💾 Supported Image Formats</h2>

<ul>
  <li>JPG</li>
  <li>JPEG</li>
  <li>PNG</li>
  <li>BMP</li>
</ul>

<p>
  Processed images can also be downloaded in supported formats such as
  <b>JPG, PNG and BMP</b>.
</p>

<hr>

<h2>🔐 Project Limitations</h2>

<ul>
  <li>The application is mainly designed for educational purposes.</li>
  <li>Processing performance depends on image size and computer hardware.</li>
  <li>Very large images may require more processing time.</li>
  <li>The application focuses on fundamental image processing techniques.</li>
</ul>

<hr>

<h2>🚀 Future Enhancements</h2>

<ul>
  <li>Add image resizing and rotation.</li>
  <li>Add image cropping functionality.</li>
  <li>Add more advanced filtering techniques.</li>
  <li>Add batch image processing.</li>
  <li>Support additional image formats.</li>
  <li>Improve the user interface and accessibility.</li>
  <li>Add more image enhancement techniques.</li>
</ul>

<hr>

<h2>🎓 Final Year Project</h2>

<p>
  <b>ImagePro Studio – Image Processing Tools</b> is developed as a
  <b>Final Year Project</b> to demonstrate the practical implementation
  of fundamental digital image processing concepts.
</p>

<p>
  The project combines programming, image processing and web development
  technologies to create an interactive and useful application.
</p>

<hr>

<h2>👨‍💻 Project Members</h2>

<table border="1" cellpadding="10" cellspacing="0">
  <tr>
    <th>Sl. No.</th>
    <th>Project Member</th>
    <th>Registration Number</th>
  </tr>

  <tr>
    <td>1</td>
    <td><b>Atharv Shetty</b></td>
    <td>8080110</td>
  </tr>

  <tr>
    <td>2</td>
    <td><b>Adinath Vasulkar</b></td>
    <td>8080102</td>
  </tr>

  <tr>
    <td>3</td>
    <td><b>Nagaveni Patil</b></td>
    <td>8080123</td>
  </tr>

  <tr>
    <td>4</td>
    <td><b>Aditya Godse</b></td>
    <td>8080103</td>
  </tr>
</table>

<hr>

<h2>🏫 Academic Information</h2>

<table border="1" cellpadding="10" cellspacing="0">
  <tr>
    <th>Details</th>
    <th>Information</th>
  </tr>

  <tr>
    <td><b>Project Title</b></td>
    <td>ImagePro Studio – Image Processing Tools</td>
  </tr>

  <tr>
    <td><b>Project Type</b></td>
    <td>Final Year Project</td>
  </tr>

  <tr>
    <td><b>Department</b></td>
    <td>Artificial Intelligence & Machine Learning</td>
  </tr>

  <tr>
    <td><b>Institution</b></td>
    <td>GTTC Belagavi</td>
  </tr>

  <tr>
    <td><b>Academic Year</b></td>
    <td>2026</td>
  </tr>
</table>

<hr>

<h2>📜 Conclusion</h2>

<p>
  The <b>ImagePro Studio</b> project was successfully developed to provide
  a simple and interactive platform for performing fundamental image
  processing operations.
</p>

<p>
  The application demonstrates the practical use of <b>Python, Flask,
  OpenCV, NumPy, HTML, CSS and JavaScript</b> in developing a web-based
  image processing system.
</p>

<p>
  Through this project, the team gained practical knowledge of digital
  image processing, web application development and OpenCV programming.
  The project successfully achieves its objectives and serves as an
  effective <b>Final Year Project</b> for demonstrating fundamental
  image processing concepts and their practical implementation.
</p>

<hr>

<h2>📌 Keywords</h2>

<p>
  Image Processing, OpenCV, Python, Flask, NumPy, Computer Vision,
  Grayscale, Thresholding, Histogram Equalization, Image Filtering,
  Sobel, Canny, Laplacian, Web Application
</p>

<hr>

<p align="center">
  <b>🖼️ ImagePro Studio</b>
</p>

<p align="center">
  Image Processing Tools using OpenCV
</p>

<p align="center">
  <b>Final Year Project – GTTC Belagavi</b>
</p>
