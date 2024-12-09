const express = require('express');
const app = express();
const mysql = require('mysql2');
const bodyParser = require('body-parser');

// Use body-parser middleware to parse JSON bodies
app.use(bodyParser.json());

// Define a root route
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

// Define the /api/rfid route to handle POST requests
app.post('/api/rfid', (req, res) => {
  const { uid, entry_type, location } = req.body;

  if (!uid || !entry_type || !location) {
    return res.status(400).json({ error: "Missing required fields (uid, entry_type, or location)" });
  }

  console.log(`Received data: UID: ${uid}, Entry Type: ${entry_type}, Location: ${location}`);

  // Insert the data into the database (example query)
  const query = 'INSERT INTO tracking (uid, location, entry_type) VALUES (?, ?, ?)';
  const values = [uid, location, entry_type];

  // Replace with your database connection details
  const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'warehouse'
  });

  db.connect((err) => {
    if (err) {
      console.error('Error connecting to the database:', err);
      return res.status(500).send('Database connection error');
    }

    db.query(query, values, (err, result) => {
      if (err) {
        console.error('Error inserting data:', err);
        return res.status(500).send('Error inserting data');
      }
      res.status(200).send('Data inserted successfully');
    });
  });
});

// Route to check the entry type (Entry or Exit) of a UID
app.post('/api/rfid/check-uid', (req, res) => {
  const { uid } = req.body;

  if (!uid) {
    return res.status(400).json({ error: "UID is required" });
  }

  // Query the database to check if the UID is already in the "tracking" table
  const query = 'SELECT entry_type FROM tracking WHERE uid = ? ORDER BY timestamp DESC LIMIT 1';
  
  const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'warehouse'
  });

  db.connect((err) => {
    if (err) {
      console.error('Error connecting to the database:', err);
      return res.status(500).send('Database connection error');
    }

    db.query(query, [uid], (err, result) => {
      if (err) {
        console.error('Error querying data:', err);
        return res.status(500).send('Error querying data');
      }

      if (result.length > 0) {
        // UID found, respond with the last entry type (Entry/Exit)
        return res.status(200).json({ entry_type: result[0].entry_type });
      } else {
        // If UID not found, assume the first scan is Entry
        return res.status(200).json({ entry_type: "Entry" });
      }
    });
  });
});

// Start the server on port 3000
app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
