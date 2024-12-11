const express = require('express');
const app = express();
const mysql = require('mysql2');
const bodyParser = require('body-parser');

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Root route
app.get('/', (req, res) => {
  res.send('Hello, Warehouse Management System API!');
});

// POST route to add RFID data
app.post('/api/rfid', (req, res) => {
  const { uid, entry_type, location } = req.body;

  if (!uid || !entry_type || !location) {
    return res.status(400).json({ error: 'Missing required fields (uid, entry_type, or location)' });
  }

  console.log(`Received data: UID: ${uid}, Entry Type: ${entry_type}, Location: ${location}`);

  const query = 'INSERT INTO tracking (uid, location, entry_type) VALUES (?, ?, ?)';
  const values = [uid, location, entry_type];

  const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'warehouse',
  });

  db.connect((err) => {
    if (err) {
      console.error('Database connection error:', err);
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

// GET route to fetch all RFID data
app.get('/api/rfid', (req, res) => {
  const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'warehouse',
  });

  const query = 'SELECT * FROM tracking';

  db.connect((err) => {
    if (err) {
      console.error('Database connection error:', err);
      return res.status(500).send('Database connection error');
    }

    db.query(query, (err, results) => {
      if (err) {
        console.error('Error fetching data:', err);
        return res.status(500).send('Error fetching data');
      }

      res.status(200).json(results); // Send data as JSON
    });
  });
});

// Start the server
app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
