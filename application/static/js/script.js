document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("video");
    const captureBtn = document.getElementById("capture");
    const uploadBtn = document.getElementById("upload");
    const fileInput = document.getElementById("fileInput");
    const resultText = document.getElementById("result");
    const binImage = document.getElementById("binImage");  // Add this line for the image

    // Set canvas size (same as the video)
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    const canvasWidth = 224;
    const canvasHeight = 224;

    canvas.width = canvasWidth;
    canvas.height = canvasHeight;

    // Start Camera
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
            })
            .catch(function (error) {
                console.log("Camera access denied:", error);
            });
    }

    // Capture Image
    captureBtn.addEventListener("click", function () {
        // Draw the current video frame on the canvas
        context.drawImage(video, 0, 0, canvasWidth, canvasHeight);

        // Convert the canvas content to a Data URL (image)
        const imageDataUrl = canvas.toDataURL("image/jpeg");

        // Display the captured image as a snapshot on the video element
        video.src = imageDataUrl;  // Assign the captured image as a new source for the video element

        // Send the captured image to the server for prediction
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
            const className = data.class.replace(/ /g, "_");  // Make sure the class name format matches the file name
            binImage.src = `/static/bins/${className}.png`;  // Change the source to the relevant bin image
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
