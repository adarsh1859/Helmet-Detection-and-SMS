<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    if (isset($_FILES["video"])) {
        $file = $_FILES["video"];
        if ($file["error"] === 0) {
            // Validate file extension, size, etc.
            move_uploaded_file($file["tmp_name"], "uploads/" . $file["name"]);
            echo "Video uploaded successfully!";
        } else {
            echo "Error uploading video";
        }
    }
}
?>