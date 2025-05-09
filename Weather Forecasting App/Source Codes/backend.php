<?php
// Database connection (update the username and password)
$conn = new mysqli("localhost", "root", "", "weather_data");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the city from the POST request
    $city = $_POST['city'] ?? '';

    if (!empty($city)) {
        // Check if the city exists in the database
        $stmt = $conn->prepare("SELECT count FROM city_count WHERE city = ?");
        $stmt->bind_param("s", $city);
        $stmt->execute();
        $stmt->store_result();

        if ($stmt->num_rows > 0) {
            // City exists, update the count
            $stmt->bind_result($currentCount);
            $stmt->fetch();
            $newCount = $currentCount + 1;

            $update_stmt = $conn->prepare("UPDATE city_count SET count = ? WHERE city = ?");
            $update_stmt->bind_param("is", $newCount, $city);
            $update_stmt->execute();
            echo "City count updated.";
        } else {
            // City doesn't exist, insert it
            $insert_stmt = $conn->prepare("INSERT INTO city_count (city, count) VALUES (?, 1)");
            $insert_stmt->bind_param("s", $city);
            $insert_stmt->execute();
            echo "City inserted.";
        }
    } else {
        echo "No city provided.";
    }
}

$conn->close();
?>
