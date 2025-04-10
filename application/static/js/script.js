document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("video");
    const captureBtn = document.getElementById("capture");
    const uploadBtn = document.getElementById("upload");
    const fileInput = document.getElementById("fileInput");
    const resultText = document.getElementById("result");
    const binImage = document.getElementById("binImage");
    const snapshot = document.getElementById("snapshot"); // Optional image preview

    // Set canvas size
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    const canvasWidth = 224;
    const canvasHeight = 224;

    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    // Start Camera with rear-facing preference
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({
            video: { facingMode: "environment" } // Back camera
        })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (error) {
            console.log("Camera access denied or not available:", error);
        });
    }

    // Capture Image
    captureBtn.addEventListener("click", function () {
        // Draw the current video frame on the canvas
        context.drawImage(video, 0, 0, canvasWidth, canvasHeight);

        // Convert the canvas content to a Data URL
        const imageDataUrl = canvas.toDataURL("image/jpeg");

        // Show the captured image in an <img> element (optional)
        if (snapshot) {
            snapshot.src = imageDataUrl;
            snapshot.style.display = "block";
        }

        // Keep the camera stream live — do NOT stop it
        canvas.toBlob(sendImage, "image/jpeg");
    });

    // Handle File Upload
    uploadBtn.addEventListener("click", function () {
        const file = fileInput.files[0];
        if (file) {
            sendImage(file);
        }
    });

    // Send Image to Server for Prediction
    function sendImage(imageBlob) {
        const formData = new FormData();
        formData.append("file", imageBlob);

        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            resultText.textContent = data.class || "Error";

            // Display the correct bin image
            const className = data.class.replace(/ /g, "_");
            binImage.src = `/static/bins/${className}.png`;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }

    // Stop camera when leaving the page
    window.addEventListener("beforeunload", function () {
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
        }
    });
});
