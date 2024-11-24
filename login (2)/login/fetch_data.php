<?php
// Connect to your MySQL database
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "your_database_name";

$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// SQL query to fetch data
$sql = "SELECT * FROM your_table_name";
$result = mysqli_query($conn, $sql);

// Fetch data as an associative array
$data = mysqli_fetch_all($result, MYSQLI_ASSOC);

// Close the connection
mysqli_close($conn);
?>