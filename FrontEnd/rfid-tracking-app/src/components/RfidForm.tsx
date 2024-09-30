// src/components/RfidForm.tsx
import React, { useState } from "react";
import { addRfidEntry } from "../api";

const RfidForm: React.FC = () => {
  const [uid, setUid] = useState("");
  const [entryType, setEntryType] = useState("Entry");
  const [location, setLocation] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await addRfidEntry(uid, entryType, location);
      console.log("RFID Entry Added:", result);
      // Reset form
      setUid("");
      setLocation("");
    } catch (error) {
      console.error("Error adding RFID entry:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>UID:</label>
        <input value={uid} onChange={(e) => setUid(e.target.value)} required />
      </div>
      <div>
        <label>Entry Type:</label>
        <select
          value={entryType}
          onChange={(e) => setEntryType(e.target.value)}
        >
          <option value="Entry">Entry</option>
          <option value="Exit">Exit</option>
        </select>
      </div>
      <div>
        <label>Location:</label>
        <input value={location} onChange={(e) => setLocation(e.target.value)} />
      </div>
      <button type="submit">Add RFID Entry</button>
    </form>
  );
};

export default RfidForm;
