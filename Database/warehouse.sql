
CREATE DATABASE warehouse;
USE warehouse;

CREATE TABLE tracking (
    uid VARCHAR(255) NOT NULL PRIMARY KEY,        -- RFID tag UID as the primary key
    location VARCHAR(100) DEFAULT 'Unknown',      -- Optional: Location/zone where RFID was read
    entry_type ENUM('Entry', 'Exit') NOT NULL,    -- Entry or Exit event
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Timestamp of the scan
    INDEX (timestamp)                              -- Indexing timestamp for faster queries
);
