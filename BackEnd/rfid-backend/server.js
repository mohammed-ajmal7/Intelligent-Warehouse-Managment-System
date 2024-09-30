
const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql2");
const cors = require("cors");

// Create an Express app
const app = express();
app.use(cors());
app.use(bodyParser.json());

// MySQL database connection configuration
const db = mysql.createConnection({
  host: "localhost",       // Database server, usually 'localhost'
  user: "root",            // MySQL root user (replace if using a different user)
  password: "root",        // MySQL root password (replace with your password)
  database: "warehouse",   // The database name
});

// Connect to the MySQL database
db.connect((err) => {
  if (err) {
    console.error("Error connecting to MySQL:", err.message);
    return;
  }
  console.log("Connected to MySQL Database: warehouse");
});

// Basic route for the root URL
app.get("/", (req, res) => {
  res.send("Welcome to the RFID API!");
});

// Endpoint to receive RFID data (POST request)
app.post("/api/rfid", (req, res) => {
  const { uid, entry_type } = req.body;

  // Ensure UID and entry_type are provided
  if (!uid || entry_type !== "Entry") {
    console.log("Missing UID or invalid entry_type");
    return res.status(400).json({ message: "UID is required and entry_type must be 'Entry'" });
  }

  console.log("Received Data:", { uid, entry_type });

  // Check if the UID already exists in the database
  const checkQuery = "SELECT * FROM tracking WHERE uid = ?";
  
  db.query(checkQuery, [uid], (err, results) => {
    if (err) {
      console.error("Error checking UID:", err);
      return res.status(500).json({ message: "Error checking UID", error: err.message });
    }

    // If UID exists, return a message indicating it's already taken
    if (results.length > 0) {
      return res.status(409).json({ message: "Entry already taken for this UID" });
    }

    // If UID does not exist, insert the RFID data into the MySQL table
    const query = "INSERT INTO tracking (uid, location, entry_type) VALUES (?, ?, ?)";
    
    db.query(query, [uid, req.body.location || "Unknown", entry_type], (err, result) => {
      if (err) {
        console.error("Error inserting data into tracking table:", err);
        return res.status(500).json({ message: "Error inserting data", error: err.message });
      }

      console.log("Data inserted successfully with ID:", result.insertId);
      
      // Return success response
      res.status(201).json({ message: "Data inserted successfully", dataId: result.insertId, entry_type });
    });
  });
});

// New endpoint to retrieve all RFID tracking records with optional filters (GET request)
app.get("/api/rfid", (req, res) => {
  const { uid, entry_type } = req.query;
  let query = "SELECT * FROM tracking";
  let queryParams = [];

  // Adding filtering based on query parameters
  if (uid || entry_type) {
    query += " WHERE";
    if (uid) {
      query += " uid = ?";
      queryParams.push(uid);
    }
    if (entry_type) {
      if (queryParams.length > 0) query += " AND";
      query += " entry_type = ?";
      queryParams.push(entry_type);
    }
  }

  db.query(query, queryParams, (err, results) => {
    if (err) {
      return res.status(500).json({ message: "Error retrieving data", error: err.message });
    }
    res.status(200).json(results);
  });
});

// New endpoint to delete a record by UID (DELETE request)
app.delete("/api/rfid/:uid", (req, res) => {
  const uid = req.params.uid;

  const query = "DELETE FROM tracking WHERE uid = ?";
  db.query(query, [uid], (err, result) => {
    if (err) {
      console.error("Error deleting data:", err);
      return res.status(500).json({ message: "Error deleting data", error: err.message });
    }

    if (result.affectedRows === 0) {
      return res.status(404).json({ message: "Record not found" });
    }

    res.status(200).json({ message: "Record deleted successfully" });
  });
});

// New endpoint to update a record by UID (PUT request)
app.put("/api/rfid/:uid", (req, res) => {
  const uid = req.params.uid;
  const { location, entry_type } = req.body;

  const query = "UPDATE tracking SET location = ?, entry_type = ? WHERE uid = ?";
  db.query(query, [location || "Unknown", entry_type, uid], (err, result) => {
    if (err) {
      console.error("Error updating data:", err);
      return res.status(500).json({ message: "Error updating data", error: err.message });
    }

    if (result.affectedRows === 0) {
      return res.status(404).json({ message: "Record not found" });
    }

    res.status(200).json({ message: "Record updated successfully" });
  });
});

// Start the Express server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
