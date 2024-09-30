// src/api.ts
import axios from "axios";

const API_BASE_URL = "http://localhost:3000/api/rfid";

// Get all RFID entries with optional filters
export const getRfidEntries = async (uid?: string, entryType?: string) => {
  const params = { uid, entry_type: entryType };
  const response = await axios.get(API_BASE_URL, { params });
  return response.data;
};

// Add new RFID entry
export const addRfidEntry = async (
  uid: string,
  entryType: string,
  location?: string
) => {
  const response = await axios.post(API_BASE_URL, {
    uid,
    entry_type: entryType,
    location,
  });
  return response.data;
};

// Update an RFID entry
export const updateRfidEntry = async (
  uid: string,
  entryType: string,
  location?: string
) => {
  const response = await axios.put(`${API_BASE_URL}/${uid}`, {
    entry_type: entryType,
    location,
  });
  return response.data;
};

// Delete an RFID entry
export const deleteRfidEntry = async (uid: string) => {
  const response = await axios.delete(`${API_BASE_URL}/${uid}`);
  return response.data;
};
