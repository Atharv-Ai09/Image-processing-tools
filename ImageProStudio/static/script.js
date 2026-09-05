// ImagePro Studio - frontend logic
// Handles: upload, camera capture, dynamic operation controls,
// calling /process, and downloading results.
// IMPORTANT: never blindly calls response.json() - always checks
// response.ok + Content-Type first, so an HTML error page never
// crashes the UI.

(() => {
  "use strict";

  // ---- state -------------------------------------------------------
  let currentFilename = null;   // filename of the image currently in "uploads/"
  let currentResultFilename = null; // filename of the last processed result
  let stream = null;            // active MediaStream from the camera

  // ---- element refs -------------------------------------------------
  const statusEl = document.getElementById("status");

  const tabUpload = document.getElementById("tabUpload");
  const tabCamera = document.getElementById("tabCamera");
  const uploadPanel = document.getElementById("uploadPanel");
  const cameraPanel = document.getElementById("cameraPanel");

  const fileInput = document.getElementById("fileInput");
  const btnUpload = document.getElementById("btnUpload");

  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const btnStartCamera = document.getElementById("btnStartCamera");
  const btnCapture = document.getElementById("btnCapture");
  const btnStopCamera = document.getElementById("btnStopCamera");

  const originalBox = document.getElementById("originalBox");
  const processedBox = document.getElementById("processedBox");

  const operationSelect = document.getElementById("operationSelect");
  const controlsWrap = document.getElementById("controls");

  const thresholdRange = document.getElementById("thresholdRange");
  const thresholdVal = document.getElementById("thresholdVal");

  const brightnessRange = document.getElementById("brightnessRange");
  const brightnessVal = document.getElementById("brightnessVal");
  const contrastRange = document.getElementById("contrastRange");
  const contrastVal = document.getElementById("contrastVal");

  const ksizeRange = document.getElementById("ksizeRange");
  const ksizeVal = document.getElementById("ksizeVal");

  const sobelDirection = document.getElementById("sobelDirection");

  const cannyLowRange = document.getElementById("cannyLowRange");
  const cannyLowVal = document.getElementById("cannyLowVal");
  const cannyHighRange = document.getElementById("cannyHighRange");
  const cannyHighVal = document.getElementById("cannyHighVal");

  const formatSelect = document.getElementById("formatSelect");

  const btnProcess = document.getElementById("btnProcess");
  const btnReset = document.getElementById("btnReset");

  const btnDownloadJpg = document.getElementById("btnDownloadJpg");
  const btnDownloadPng = document.getElementById("btnDownloadPng");
  const btnDownloadBmp = document.getElementById("btnDownloadBmp");

  // ---- status helper --------------------------------------------------
  function showStatus(message, type = "info") {
    statusEl.textContent = message;
    statusEl.className = `status ${type}`;
  }

  function clearStatus() {
    statusEl.textContent = "";
    statusEl.className = "status";
  }

  // ---- safe fetch/json helper -----------------------------------------
  // Never blindly calls response.json(): checks status + content-type first.
  async function safeJson(response) {
    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      const text = await response.text();
      throw new Error(
        `Server returned an unexpected response (status ${response.status}). ` +
        `This usually means the server crashed or the route is wrong.`
      );
    }
    const data = await response.json();
    if (!response.ok && data.success === undefined) {
      throw new Error(data.error || `Request failed with status ${response.status}`);
    }
    return data;
  }

  // ---- tabs -------------------------------------------------------------
  tabUpload.addEventListener("click", () => {
    tabUpload.classList.add("active");
    tabCamera.classList.remove("active");
    uploadPanel.classList.remove("hidden");
    cameraPanel.classList.add("hidden");
    stopCamera();
  });

  tabCamera.addEventListener("click", () => {
    tabCamera.classList.add("active");
    tabUpload.classList.remove("active");
    cameraPanel.classList.remove("hidden");
    uploadPanel.classList.add("hidden");
  });

  // ---- upload from PC -----------------------------------------------
  btnUpload.addEventListener("click", () => fileInput.click());

  fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;

    const ext = file.name.split(".").pop().toLowerCase();
    if (!["jpg", "jpeg", "png", "bmp"].includes(ext)) {
      showStatus("Error: only JPG, JPEG, PNG or BMP files are allowed", "error");
      return;
    }

    showStatus("Uploading image...", "info");
    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("/upload", { method: "POST", body: formData });
      const data = await safeJson(response);

      if (!data.success) {
        showStatus(`Error: ${data.error}`, "error");
        return;
      }

      currentFilename = data.filename;
      setOriginalImage(data.image_url);
      clearProcessedImage();
      btnProcess.disabled = false;
      showStatus(data.message || "Image uploaded successfully", "success");
    } catch (err) {
      showStatus(`Error: ${err.message}`, "error");
    }
  });

  // ---- camera ---------------------------------------------------------
  btnStartCamera.addEventListener("click", async () => {
    // Feature-detect first: getUserMedia needs a secure context (https or
    // localhost/127.0.0.1) and browser support, and fails silently
    // otherwise if we don't check.
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showStatus(
        "Error: camera access isn't supported in this browser, or the page isn't loaded over HTTPS/localhost.",
        "error"
      );
      return;
    }

    btnStartCamera.disabled = true;
    showStatus("Requesting camera access...", "info");

    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      });
      video.srcObject = stream;

      // Some browsers won't start rendering frames just because the
      // `autoplay` attribute is set - explicitly kick off playback and
      // wait until the video actually has real dimensions before we let
      // the user hit "Capture" (otherwise videoWidth/videoHeight can
      // still be 0, producing a blank/broken captured frame).
      await video.play().catch(() => {
        /* some browsers throw if play() races with pause(); safe to ignore */
      });

      const ready = () =>
        new Promise((resolve) => {
          if (video.readyState >= 2 && video.videoWidth > 0) {
            resolve();
          } else {
            video.addEventListener("loadeddata", () => resolve(), { once: true });
          }
        });
      await ready();

      btnCapture.disabled = false;
      btnStopCamera.disabled = false;
      showStatus("Camera started", "success");
    } catch (err) {
      btnStartCamera.disabled = false;
      let msg = "Error: could not access the camera.";
      if (err && err.name === "NotAllowedError") {
        msg = "Error: camera permission was denied. Please allow camera access in your browser and try again.";
      } else if (err && err.name === "NotFoundError") {
        msg = "Error: no camera was found on this device.";
      } else if (err && err.name === "NotReadableError") {
        msg = "Error: the camera is already in use by another application.";
      }
      showStatus(msg, "error");
    }
  });

  btnCapture.addEventListener("click", () => {
    if (!stream) return;

    if (!video.videoWidth || !video.videoHeight) {
      showStatus("Error: camera feed isn't ready yet. Please wait a moment and try again.", "error");
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) {
        showStatus("Error: failed to capture frame from camera", "error");
        return;
      }

      showStatus("Uploading captured image...", "info");
      const formData = new FormData();
      formData.append("image", blob, "capture.jpg");

      try {
        const response = await fetch("/camera", { method: "POST", body: formData });
        const data = await safeJson(response);

        if (!data.success) {
          showStatus(`Error: ${data.error}`, "error");
          return;
        }

        currentFilename = data.filename;
        setOriginalImage(data.image_url);
        clearProcessedImage();
        btnProcess.disabled = false;
        showStatus(data.message || "Image captured", "success");
      } catch (err) {
        showStatus(`Error: ${err.message}`, "error");
      }
    }, "image/jpeg", 0.95);
  });

  btnStopCamera.addEventListener("click", stopCamera);

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      stream = null;
    }
    video.pause();
    video.srcObject = null;
    btnStartCamera.disabled = false;
    btnCapture.disabled = true;
    btnStopCamera.disabled = true;
  }

  // Release the camera if the user navigates away/closes the tab while
  // it's still running.
  window.addEventListener("beforeunload", stopCamera);

  // ---- image display helpers -----------------------------------------
  function setOriginalImage(url) {
    originalBox.innerHTML = `<img src="${url}?t=${Date.now()}" alt="Original image" />`;
  }

  function setProcessedImage(url) {
    processedBox.innerHTML = `<img src="${url}?t=${Date.now()}" alt="Processed image" />`;
  }

  function clearProcessedImage() {
    processedBox.innerHTML = `<span class="placeholder">No processed image yet</span>`;
    currentResultFilename = null;
    btnDownloadJpg.disabled = true;
    btnDownloadPng.disabled = true;
    btnDownloadBmp.disabled = true;
  }

  // ---- dynamic operation controls -------------------------------------
  const controlRows = Array.from(document.querySelectorAll(".control-row"));

  function updateVisibleControls() {
    const op = operationSelect.value;
    controlRows.forEach((row) => {
      const targets = row.dataset.for.split(",");
      row.classList.toggle("visible", targets.includes(op));
    });
  }

  operationSelect.addEventListener("change", updateVisibleControls);
  updateVisibleControls();

  thresholdRange.addEventListener("input", () => (thresholdVal.textContent = thresholdRange.value));
  brightnessRange.addEventListener("input", () => (brightnessVal.textContent = brightnessRange.value));
  contrastRange.addEventListener("input", () => {
    contrastVal.textContent = (contrastRange.value / 10).toFixed(1);
  });
  ksizeRange.addEventListener("input", () => (ksizeVal.textContent = ksizeRange.value));
  cannyLowRange.addEventListener("input", () => (cannyLowVal.textContent = cannyLowRange.value));
  cannyHighRange.addEventListener("input", () => (cannyHighVal.textContent = cannyHighRange.value));

  // ---- process ----------------------------------------------------------
  btnProcess.addEventListener("click", async () => {
    if (!currentFilename) {
      showStatus("Error: please upload or capture an image first", "error");
      return;
    }

    const operation = operationSelect.value;
    const payload = {
      filename: currentFilename,
      operation,
      threshold: thresholdRange.value,
      brightness: brightnessRange.value,
      contrast: (contrastRange.value / 10).toFixed(2),
      ksize: ksizeRange.value,
      direction: sobelDirection.value,
      low: cannyLowRange.value,
      high: cannyHighRange.value,
      format: formatSelect.value,
    };

    showStatus("Processing...", "info");
    btnProcess.disabled = true;

    try {
      const response = await fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await safeJson(response);

      if (!data.success) {
        showStatus(`Error: ${data.error}`, "error");
        return;
      }

      setProcessedImage(data.image_url);
      currentResultFilename = data.filename;
      btnDownloadJpg.disabled = false;
      btnDownloadPng.disabled = false;
      btnDownloadBmp.disabled = false;
      showStatus(data.message || "Processing completed", "success");
    } catch (err) {
      showStatus(`Error: ${err.message}`, "error");
    } finally {
      btnProcess.disabled = false;
    }
  });

  // ---- download -----------------------------------------------------
  function download(format) {
    if (!currentResultFilename) return;
    const url = `/download/${currentResultFilename}?format=${format}`;
    window.location.href = url;
    showStatus("Image saved successfully", "success");
  }

  btnDownloadJpg.addEventListener("click", () => download("jpg"));
  btnDownloadPng.addEventListener("click", () => download("png"));
  btnDownloadBmp.addEventListener("click", () => download("bmp"));

  // ---- reset ----------------------------------------------------------
  btnReset.addEventListener("click", () => {
    currentFilename = null;
    currentResultFilename = null;

    fileInput.value = "";
    originalBox.innerHTML = `<span class="placeholder">No image selected</span>`;
    clearProcessedImage();

    operationSelect.value = "load_display";
    updateVisibleControls();

    thresholdRange.value = 127; thresholdVal.textContent = "127";
    brightnessRange.value = 0; brightnessVal.textContent = "0";
    contrastRange.value = 10; contrastVal.textContent = "1.0";
    ksizeRange.value = 5; ksizeVal.textContent = "5";
    sobelDirection.value = "both";
    cannyLowRange.value = 100; cannyLowVal.textContent = "100";
    cannyHighRange.value = 200; cannyHighVal.textContent = "200";
    formatSelect.value = "jpg";

    btnProcess.disabled = true;
    stopCamera();
    clearStatus();
  });
})();
