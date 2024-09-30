// src/components/RfidTable.tsx
import React, { useEffect, useState } from "react";
import { getRfidEntries, deleteRfidEntry, updateRfidEntry } from "../api";

const RfidTable: React.FC = () => {
  const [entries, setEntries] = useState<any[]>([]);

  useEffect(() => {
    const fetchEntries = async () => {
      const data = await getRfidEntries();
      setEntries(data);
    };
    fetchEntries();
  }, []);

  const handleDelete = async (uid: string) => {
    try {
      await deleteRfidEntry(uid);
      setEntries(entries.filter((entry) => entry.uid !== uid));
    } catch (error) {
      console.error("Error deleting entry:", error);
    }
  };

  return (
    <table>
      <thead>
        <tr>
          <th>UID</th>
          <th>Entry Type</th>
          <th>Location</th>
          <th>Timestamp</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {entries.map((entry) => (
          <tr key={entry.uid}>
            <td>{entry.uid}</td>
            <td>{entry.entry_type}</td>
            <td>{entry.location}</td>
            <td>{entry.timestamp}</td>
            <td>
              <button onClick={() => handleDelete(entry.uid)}>Delete</button>
              {/* You can add an "Edit" button and update functionality here */}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default RfidTable;
