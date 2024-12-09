-- Create the warehouse database if it doesn't already exist
CREATE DATABASE warehouse;

-- Use the warehouse database
USE warehouse;
CREATE TABLE tracking (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- Unique ID for each scan record
    uid VARCHAR(255) NOT NULL,                  -- UID of the scanned RFID tag
    location VARCHAR(255) DEFAULT 'Unknown',    -- Location or zone of RFID scan
    entry_type ENUM('Entry', 'Exit') NOT NULL,  -- Type of scan (Entry or Exit)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp when the scan was recorded
    UNIQUE (uid, timestamp)                     -- Prevent duplicate scans at the same time
);
