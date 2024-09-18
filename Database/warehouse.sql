CREATE DATABASE warehouse;
USE warehouse;
CREATE TABLE tracking (
 id INT AUTO_INCREMENT PRIMARY KEY,           -- Unique identifier for each record
    uid VARCHAR(255) NOT NULL,                   -- RFID tag UID
    location VARCHAR(100) DEFAULT 'Unknown',     -- Optional: Location/zone where RFID was read
    entry_type ENUM('Entry', 'Exit') NOT NULL,   -- Entry or Exit event
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Timestamp of the scan
    INDEX (uid),                                 -- Indexing UID for faster queries
    INDEX (timestamp)                            -- Indexing timestamp for faster queries
);