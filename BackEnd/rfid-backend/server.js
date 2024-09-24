const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql2"); // mysql2 package that you installed
const cors = require("cors");

// Create an Express app
const app = express();
app.use(cors());
app.use(bodyParser.json());

// MySQL database connection configuration
const db = mysql.createConnection({
  host: "localhost", // Host where the database is running (usually localhost)
  user: "root", // MySQL root user (replace with your actual user if different)
  password: "Aju@2003", // Replace with your MySQL root password
  database: "warehouse", // The database you created in MySQL
});

// Connect to the MySQL database
db.connect((err) => {
  if (err) {
    console.error("Error connecting to MySQL:", err.message);
    return;
  }
  console.log("Connected to MySQL Database: warehouse");
});

// Endpoint to receive RFID data (POST request)
app.post("/api/rfid", (req, res) => {
  const { uid, location, entry_type } = req.body;

  // Ensure all required fields are provided
  if (!uid || !entry_type) {
    return res.status(400).json({ message: "UID and entry type are required" });
  }

  // Insert the RFID data into the MySQL table
  const query =
    "INSERT INTO tracking (uid, location, entry_type) VALUES (?, ?, ?)";
  db.query(query, [uid, location || "Unknown", entry_type], (err, result) => {
    if (err) {
      console.error("Error inserting data into tracking table:", err.message);
      return res.status(500).json({ message: "Error inserting data" });
    }

    // Return success response
    res
      .status(200)
      .json({ message: "Data inserted successfully", dataId: result.insertId });
  });
});

// Start the Express server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
