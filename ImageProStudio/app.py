"""
ImagePro Studio - Image Processing using OpenCV
-------------------------------------------------
A Flask + OpenCV academic project implementing classic digital image
processing practicals (grayscale, binary, RGB<->HSV, histogram
equalization, brightness/contrast, spatial filters, edge detection,
and format conversion) through a simple browser UI.

No AI / ML / deep learning is used anywhere in this project - every
result is produced directly by an OpenCV (cv2) function call.
"""

import os
import time
import uuid
import traceback
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file

# --------------------------------------------------------------------------
# App configuration
# --------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp"}

# Make sure the folders exist automatically, every time the app starts.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

MAX_AGE_SECONDS = 60 * 60  # 1 hour


def cleanup_old_files(folder: str) -> None:
    """Best-effort removal of files older than MAX_AGE_SECONDS so
    uploads/outputs don't grow forever during a long session. Never lets
    a cleanup failure break the request that triggered it."""
    try:
        now = time.time()
        for name in os.listdir(folder):
            if name == ".gitkeep":
                continue
            path = os.path.join(folder, name)
            try:
                if os.path.isfile(path) and (now - os.path.getmtime(path)) > MAX_AGE_SECONDS:
                    os.remove(path)
            except OSError:
                pass
    except OSError:
        pass

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB safety cap


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def unique_name(prefix: str, ext: str) -> str:
    """Build a collision-free filename using a millisecond timestamp plus a
    short random suffix (two requests in the same millisecond would
    otherwise silently overwrite each other's files)."""
    ext = ext.lower().lstrip(".")
    if ext == "jpeg":
        ext = "jpg"  # normalize so files are consistently named .jpg
    suffix = uuid.uuid4().hex[:6]
    return f"{prefix}_{int(time.time() * 1000)}_{suffix}.{ext}"


def read_image(path: str):
    """Read an image with OpenCV and raise a clear error if it fails."""
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not read the image file. It may be corrupted or in an unsupported format.")
    return img


def save_image(img, folder: str, prefix: str, ext: str) -> str:
    """Save an OpenCV image (BGR ndarray) to disk using cv2.imwrite and
    return just the filename (not the full path)."""
    ext = ext.lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS:
        ext = "png"
    filename = unique_name(prefix, ext)
    full_path = os.path.join(folder, filename)

    # cv2.imwrite chooses the codec purely from the file extension, so this
    # single call is what actually performs JPG / PNG / BMP conversion.
    ok = cv2.imwrite(full_path, img)
    if not ok:
        raise ValueError(f"OpenCV failed to write the image as .{ext}")
    return filename


def to_3channel(img):
    """Ensure a single-channel (grayscale/binary) image is converted back
    to a 3-channel BGR image so it can be written/displayed like any other
    photo (JPG/PNG/BMP viewers expect 3 channels)."""
    if img is None:
        return img
    if len(img.shape) == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


# --------------------------------------------------------------------------
# ---------------------  OpenCV processing functions  ----------------------
# Each of the 13 practicals is implemented as its own, separate function.
# --------------------------------------------------------------------------

def op_load_display(img, params):
    """1. Load and Display an Image - identity operation, simply returns
    the image exactly as it was read by cv2.imread."""
    return img.copy()


def op_grayscale(img, params):
    """2. Convert an Image to Grayscale using cv2.cvtColor(BGR2GRAY)."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return to_3channel(gray)


def op_binary(img, params):
    """3. Convert an Image to Binary using a user-controlled threshold."""
    threshold = int(params.get("threshold", 127))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return to_3channel(binary)


def op_format_convert(img, params):
    """4. Convert an Image Between JPG, PNG and BMP formats.
    The actual re-encoding happens in save_image() via cv2.imwrite, using
    the extension chosen by the user (params['format']); here we simply
    pass the pixels through unchanged."""
    return img.copy()


def op_rgb_to_gray(img, params):
    """5. Convert RGB to Grayscale.
    OpenCV loads images as BGR, so we first convert BGR->RGB (to work in
    "true" RGB order) and then RGB->GRAY, exactly as the practical asks."""
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    return to_3channel(gray)


def op_rgb_to_hsv(img, params):
    """6. Convert RGB to HSV.
    BGR -> RGB -> HSV. The resulting H/S/V planes are returned as a 3
    channel image so it can be saved/viewed like a normal picture (colors
    will look "false-colored" because H/S/V values are not R/G/B values -
    this is expected and is explained to the user)."""
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    return hsv


def op_histogram_equalization(img, params):
    """7. Histogram Equalization using cv2.equalizeHist on the luminance
    (grayscale) channel."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    return to_3channel(equalized)


def op_brightness_contrast(img, params):
    """8. Brightness and Contrast Adjustment using cv2.convertScaleAbs.
    new_pixel = alpha * pixel + beta
      alpha (contrast) : 0.0 - 3.0   (1.0 = no change)
      beta  (brightness): -100 - 100 (0   = no change)"""
    brightness = int(params.get("brightness", 0))
    contrast = float(params.get("contrast", 1.0))
    return cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)


def op_average_filter(img, params):
    """9. Average (mean) filter using cv2.blur - smooths the image by
    averaging pixels inside a kernel window."""
    ksize = int(params.get("ksize", 5))
    ksize = max(1, ksize)
    return cv2.blur(img, (ksize, ksize))


def op_gaussian_filter(img, params):
    """10. Gaussian filter using cv2.GaussianBlur - smooths the image
    with a weighted (Gaussian) kernel, preserving edges better than a
    plain average filter."""
    ksize = int(params.get("ksize", 5))
    if ksize % 2 == 0:
        ksize += 1  # GaussianBlur requires an odd kernel size
    ksize = max(1, ksize)
    return cv2.GaussianBlur(img, (ksize, ksize), 0)


def op_laplacian_sharpen(img, params):
    """11. Laplacian filter for sharpening.
    The Laplacian highlights regions of rapid intensity change (edges).
    Subtracting it from the original image sharpens those edges."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
    laplacian_abs = cv2.convertScaleAbs(laplacian)

    sharpened = cv2.addWeighted(gray, 1.0, laplacian_abs, 1.0, 0)
    return to_3channel(sharpened)


def op_sobel_edge(img, params):
    """12. Sobel Edge Detection - computes the image gradient in the X
    and/or Y direction using cv2.Sobel."""
    direction = params.get("direction", "both")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    if direction == "x":
        result = cv2.convertScaleAbs(sobel_x)
    elif direction == "y":
        result = cv2.convertScaleAbs(sobel_y)
    else:  # both
        sobel_x = cv2.convertScaleAbs(sobel_x)
        sobel_y = cv2.convertScaleAbs(sobel_y)
        result = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)

    return to_3channel(result)


def op_canny_edge(img, params):
    """13. Canny Edge Detection using cv2.Canny with user-controlled
    lower/upper hysteresis thresholds."""
    low = int(params.get("low", 100))
    high = int(params.get("high", 200))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, low, high)
    return to_3channel(edges)


OPERATIONS = {
    "load_display": op_load_display,
    "grayscale": op_grayscale,
    "binary": op_binary,
    "format_convert": op_format_convert,
    "rgb_to_gray": op_rgb_to_gray,
    "rgb_to_hsv": op_rgb_to_hsv,
    "histogram_equalization": op_histogram_equalization,
    "brightness_contrast": op_brightness_contrast,
    "average_filter": op_average_filter,
    "gaussian_filter": op_gaussian_filter,
    "laplacian_sharpen": op_laplacian_sharpen,
    "sobel_edge": op_sobel_edge,
    "canny_edge": op_canny_edge,
}


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/outputs/<path:filename>")
def serve_output(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)


@app.route("/upload", methods=["POST"])
def upload():
    """Handles the 'Upload from PC' flow (multipart/form-data)."""
    try:
        cleanup_old_files(app.config["UPLOAD_FOLDER"])
        cleanup_old_files(app.config["OUTPUT_FOLDER"])

        if "image" not in request.files:
            return jsonify(success=False, error="No image received"), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify(success=False, error="No file selected"), 400

        if not allowed_file(file.filename):
            return jsonify(success=False, error="Only JPG, JPEG, PNG or BMP files are allowed"), 400

        original_name = secure_filename(file.filename)
        ext = original_name.rsplit(".", 1)[1].lower()
        filename = unique_name("upload", ext)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        # Verify OpenCV can actually decode it (catches fake/corrupted files)
        img = cv2.imread(save_path, cv2.IMREAD_COLOR)
        if img is None:
            os.remove(save_path)
            return jsonify(success=False, error="The uploaded file is not a valid image"), 400

        return jsonify(
            success=True,
            filename=filename,
            image_url=f"/uploads/{filename}",
            message="Image uploaded successfully",
        )

    except RequestEntityTooLarge:
        return jsonify(success=False, error="File is too large. Maximum upload size is 25 MB."), 413
    except Exception as exc:  # never let an exception turn into an HTML page
        traceback.print_exc()
        return jsonify(success=False, error=f"Upload failed: {exc}"), 500


@app.route("/camera", methods=["POST"])
def camera_capture():
    """Handles a captured camera frame sent as a Blob via FormData."""
    try:
        if "image" not in request.files:
            return jsonify(success=False, error="No image received from camera"), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify(success=False, error="Empty camera frame received"), 400

        filename = unique_name("capture", "jpg")
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        img = cv2.imread(save_path, cv2.IMREAD_COLOR)
        if img is None:
            os.remove(save_path)
            return jsonify(success=False, error="Could not decode the captured camera frame"), 400

        return jsonify(
            success=True,
            filename=filename,
            image_url=f"/uploads/{filename}",
            message="Image captured",
        )

    except RequestEntityTooLarge:
        return jsonify(success=False, error="File is too large. Maximum upload size is 25 MB."), 413
    except Exception as exc:
        traceback.print_exc()
        return jsonify(success=False, error=f"Camera capture failed: {exc}"), 500


@app.route("/process", methods=["POST"])
def process():
    """Applies the selected OpenCV operation and ALWAYS returns JSON."""
    try:
        data = request.get_json(silent=True) or request.form

        filename = data.get("filename")
        operation = data.get("operation")

        if not filename:
            return jsonify(success=False, error="No image received"), 400
        if operation not in OPERATIONS:
            return jsonify(success=False, error=f"Unknown operation: {operation}"), 400

        # The "Target Format" control is only shown to the user for the
        # Format Conversion operation, so it should only affect that
        # operation. Every other operation always saves as lossless PNG,
        # regardless of whatever value is left over in that hidden field.
        if operation == "format_convert":
            out_format = (data.get("format") or "png").lower()
            if out_format not in ALLOWED_EXTENSIONS:
                out_format = "png"
        else:
            out_format = "png"

        source_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))
        if not os.path.exists(source_path):
            return jsonify(success=False, error="Source image not found. Please upload or capture again."), 404

        img = read_image(source_path)

        params = {
            "threshold": data.get("threshold", 127),
            "brightness": data.get("brightness", 0),
            "contrast": data.get("contrast", 1.0),
            "ksize": data.get("ksize", 5),
            "direction": data.get("direction", "both"),
            "low": data.get("low", 100),
            "high": data.get("high", 200),
            "format": out_format,
        }

        result = OPERATIONS[operation](img, params)
        if result is None:
            return jsonify(success=False, error="Processing produced no output"), 500

        result_filename = save_image(result, app.config["OUTPUT_FOLDER"], "result", out_format)

        return jsonify(
            success=True,
            image_url=f"/outputs/{result_filename}",
            filename=result_filename,
            message="Processing completed",
        )

    except cv2.error as exc:
        traceback.print_exc()
        return jsonify(success=False, error=f"OpenCV error: {exc}"), 500
    except Exception as exc:
        traceback.print_exc()
        return jsonify(success=False, error=str(exc)), 500


@app.route("/download/<path:filename>")
def download(filename):
    """Lets the user download a previously processed result. If a
    different target format is requested via ?format=jpg|png|bmp, the
    image is re-encoded on the fly with cv2.imwrite before sending."""
    try:
        safe_name = secure_filename(filename)
        src_path = os.path.join(app.config["OUTPUT_FOLDER"], safe_name)
        if not os.path.exists(src_path):
            return jsonify(success=False, error="File not found"), 404

        requested_format = request.args.get("format")
        if requested_format:
            requested_format = requested_format.lower().lstrip(".")
            if requested_format not in ALLOWED_EXTENSIONS:
                return jsonify(success=False, error="Unsupported download format"), 400

            current_ext = safe_name.rsplit(".", 1)[1].lower()
            if requested_format != current_ext:
                img = read_image(src_path)
                new_name = save_image(img, app.config["OUTPUT_FOLDER"], "download", requested_format)
                src_path = os.path.join(app.config["OUTPUT_FOLDER"], new_name)
                safe_name = new_name

        return send_file(src_path, as_attachment=True, download_name=safe_name)

    except Exception as exc:
        traceback.print_exc()
        return jsonify(success=False, error=str(exc)), 500


@app.errorhandler(RequestEntityTooLarge)
def too_large(_e):
    return jsonify(success=False, error="File is too large. Maximum upload size is 25 MB."), 413


@app.errorhandler(404)
def not_found(_e):
    if request.path.startswith(("/process", "/upload", "/camera", "/download")):
        return jsonify(success=False, error="Not found"), 404
    return "Page not found", 404


@app.errorhandler(500)
def server_error(_e):
    if request.path.startswith(("/process", "/upload", "/camera", "/download")):
        return jsonify(success=False, error="Internal server error"), 500
    return "Internal server error", 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
