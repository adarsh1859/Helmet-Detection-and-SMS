<?php
$folder = $_GET['motorcycle_license_plate-main/riders_pictures'];

// Security check (same as before)
if (strpos($folder, '..') !== false) {
    die('Invalid path');
}

$images = [];
$imageDir = realpath($folder); // Get absolute path for security

if (is_dir($imageDir)) {
    $scannedFiles = scandir($imageDir);
    foreach ($scannedFiles as $filename) {
        if (in_array(strtolower($filename), ['jpg', 'jpeg', 'png', 'gif'])) { // Check for valid image extensions
            $imagePath = "$folder/$filename";
            $images[] = [
                'src' => $imagePath,
                'alt' => 'Image from Report ' . str_replace('images/', '', $folder) // Generate alt text based on folder name
            ];
        }
    }
}

echo json_encode($images);
?>
